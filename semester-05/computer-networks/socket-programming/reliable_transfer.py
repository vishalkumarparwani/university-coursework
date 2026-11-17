import argparse
import heapq
import random

TXTIME = 8000 / 2000000


def checksum(seq, data):
    return (seq + sum(data.encode())) % 65536


def makedata(seq, data):
    return {"seq": seq, "data": data, "sum": checksum(seq, data)}


def makeack(seq):
    return {"ack": seq, "sum": checksum(seq, "")}


def dataok(pkt):
    return pkt["sum"] == checksum(pkt["seq"], pkt["data"])


def ackok(pkt):
    return pkt["sum"] == checksum(pkt["ack"], "")


class Channel:
    def __init__(self, loss, corruption, delay, rtt, rng, verbose):
        self.loss = loss
        self.corruption = corruption
        self.delay = delay
        self.rtt = rtt
        self.rng = rng
        self.verbose = verbose
        self.queue = []
        self.count = 0
        self.now = 0.0
        self.lines = []
        self.lastarrival = {"DATA": 0.0, "ACK": 0.0}

    def log(self, text):
        line = f"[{self.now:8.3f}s] {text}"
        self.lines.append(line)
        if self.verbose:
            print(line)

    def send(self, kind, pkt):
        number = pkt["seq"] if kind == "DATA" else pkt["ack"]
        label = f"{kind} seq {number}"
        if self.rng.random() < self.loss:
            self.log(f"CHANNEL LOSS {label}")
            return
        if self.rng.random() < self.corruption:
            pkt = dict(pkt)
            if kind == "DATA":
                pkt["data"] = "#" + pkt["data"][1:]
            else:
                pkt["ack"] = pkt["ack"] + 1
            self.log(f"CHANNEL CORRUPTION {label}")
        extra = 0.0
        if self.rng.random() < self.delay:
            extra = self.rng.uniform(0.15, 0.65)
            self.log(f"CHANNEL DELAY {label} by {extra:.3f}s")
        travel = self.rtt / 2 + extra
        if kind == "DATA":
            travel += TXTIME
        arrival = max(self.now + travel, self.lastarrival[kind])
        self.lastarrival[kind] = arrival
        self.count += 1
        heapq.heappush(self.queue, (arrival, self.count, kind, pkt))

    def nexttime(self):
        if self.queue:
            return self.queue[0][0]
        return None

    def pop(self):
        time, order, kind, pkt = heapq.heappop(self.queue)
        return time, kind, pkt


class GBNSender:
    def __init__(self, total, window, space, timeout, channel):
        self.total = total
        self.N = window
        self.space = space
        self.timeout = timeout
        self.channel = channel
        self.base = 0
        self.nextseqnum = 0
        self.deadline = None
        self.sent = 0
        self.retrans = 0

    def done(self):
        return self.base >= self.total

    def nexttime(self):
        return self.deadline

    def transmit(self, n, again):
        self.sent += 1
        if again:
            self.retrans += 1
            self.channel.log(f"RETRANSMIT pkt {n} seq {n % self.space}")
        else:
            self.channel.log(f"SEND pkt {n} seq {n % self.space}")
        self.channel.send("DATA", makedata(n % self.space, f"data{n}"))

    def fill(self):
        while self.nextseqnum < self.total and self.nextseqnum < self.base + self.N:
            self.transmit(self.nextseqnum, False)
            if self.base == self.nextseqnum:
                self.deadline = self.channel.now + self.timeout
            self.nextseqnum += 1
        self.channel.log(f"GBN sender base={self.base} nextseqnum={self.nextseqnum}")

    def onack(self, ack):
        if not ackok(ack):
            self.channel.log("RECEIVE corrupted ACK, checksum fails, discard")
            return
        found = None
        for n in range(self.base, self.nextseqnum):
            if n % self.space == ack["ack"]:
                found = n
        if found is None:
            self.channel.log(f"RECEIVE old ACK seq {ack['ack']}, ignore")
            return
        self.channel.log(f"RECEIVE cumulative ACK {found}, packets {self.base} to {found} done")
        self.base = found + 1
        if self.base == self.nextseqnum:
            self.deadline = None
        else:
            self.deadline = self.channel.now + self.timeout
        self.fill()

    def ontimeout(self):
        self.channel.log(f"TIMEOUT on base {self.base}, resend all outstanding")
        self.deadline = self.channel.now + self.timeout
        for n in range(self.base, self.nextseqnum):
            self.transmit(n, True)


class GBNReceiver:
    def __init__(self, space, channel):
        self.space = space
        self.channel = channel
        self.expectedseqnum = 0
        self.lastack = None
        self.delivered = []

    def ondata(self, pkt):
        if not dataok(pkt):
            self.channel.log("RECEIVE corrupted DATA, checksum fails, discard")
            return
        if pkt["seq"] == self.expectedseqnum:
            self.channel.log(f"RECEIVE seq {pkt['seq']} in order, deliver")
            self.delivered.append(pkt["data"])
            self.lastack = self.expectedseqnum
            self.expectedseqnum = (self.expectedseqnum + 1) % self.space
            self.channel.log(f"SEND ACK {self.lastack}")
            self.channel.send("ACK", makeack(self.lastack))
        else:
            self.channel.log(f"RECEIVE seq {pkt['seq']} out of order, expected {self.expectedseqnum}, discard")
            if self.lastack is not None:
                self.channel.log(f"SEND repeat ACK {self.lastack}")
                self.channel.send("ACK", makeack(self.lastack))


class SRSender:
    def __init__(self, total, window, space, timeout, channel):
        self.total = total
        self.N = window
        self.space = space
        self.timeout = timeout
        self.channel = channel
        self.base = 0
        self.nextseqnum = 0
        self.acked = set()
        self.deadlines = {}
        self.sent = 0
        self.retrans = 0

    def done(self):
        return self.base >= self.total

    def nexttime(self):
        if self.deadlines:
            return min(self.deadlines.values())
        return None

    def transmit(self, n, again):
        self.sent += 1
        if again:
            self.retrans += 1
            self.channel.log(f"RETRANSMIT pkt {n} seq {n % self.space}")
        else:
            self.channel.log(f"SEND pkt {n} seq {n % self.space}")
        self.deadlines[n] = self.channel.now + self.timeout
        self.channel.send("DATA", makedata(n % self.space, f"data{n}"))

    def fill(self):
        while self.nextseqnum < self.total and self.nextseqnum < self.base + self.N:
            self.transmit(self.nextseqnum, False)
            self.nextseqnum += 1
        self.channel.log(f"SR sender base={self.base} nextseqnum={self.nextseqnum}")

    def onack(self, ack):
        if not ackok(ack):
            self.channel.log("RECEIVE corrupted ACK, checksum fails, discard")
            return
        found = None
        for n in range(self.base, self.nextseqnum):
            if n % self.space == ack["ack"]:
                found = n
        if found is None or found in self.acked:
            self.channel.log(f"RECEIVE duplicate or old ACK seq {ack['ack']}, ignore")
            return
        self.channel.log(f"RECEIVE individual ACK {found}")
        self.acked.add(found)
        del self.deadlines[found]
        while self.base in self.acked:
            self.base += 1
        self.fill()

    def ontimeout(self):
        now = self.channel.now
        for n in sorted(self.deadlines):
            if self.deadlines[n] <= now:
                self.channel.log(f"TIMEOUT on pkt {n}, resend only this one")
                self.transmit(n, True)


class SRReceiver:
    def __init__(self, window, space, channel):
        self.N = window
        self.space = space
        self.channel = channel
        self.rcvbase = 0
        self.buffer = {}
        self.delivered = []

    def ondata(self, pkt):
        if not dataok(pkt):
            self.channel.log("RECEIVE corrupted DATA, checksum fails, discard")
            return
        seq = pkt["seq"]
        if (seq - self.rcvbase) % self.space < self.N:
            if seq in self.buffer:
                self.channel.log(f"RECEIVE seq {seq} already buffered")
            elif seq == self.rcvbase:
                self.channel.log(f"RECEIVE seq {seq} at rcvbase")
            else:
                self.channel.log(f"RECEIVE seq {seq} early, buffer it, rcvbase={self.rcvbase}")
            self.buffer[seq] = pkt["data"]
            self.channel.log(f"SEND ACK {seq}")
            self.channel.send("ACK", makeack(seq))
            while self.rcvbase in self.buffer:
                self.channel.log(f"DELIVER seq {self.rcvbase} to application")
                self.delivered.append(self.buffer.pop(self.rcvbase))
                self.rcvbase = (self.rcvbase + 1) % self.space
        elif (self.rcvbase - seq) % self.space <= self.N:
            self.channel.log(f"RECEIVE old seq {seq}, ACK again")
            self.channel.send("ACK", makeack(seq))
        else:
            self.channel.log(f"RECEIVE seq {seq} outside window, discard")


def simulate(protocol="gbn", packets=200, window=4, bits=3, loss=0.0,
             corruption=0.0, delay=0.0, timeout=1.0, seed=625, rtt=0.5,
             verbose=False):
    space = 2 ** bits
    if protocol not in ("gbn", "sr"):
        raise ValueError("protocol must be gbn or sr")
    if protocol == "gbn" and window >= space:
        raise ValueError("GBN window must be smaller than 2^k")
    if protocol == "sr" and window > space // 2:
        raise ValueError("SR window must be at most 2^k divided by 2")
    for p in (loss, corruption, delay):
        if not 0 <= p <= 1:
            raise ValueError("probabilities must be between 0 and 1")
    rng = random.Random(seed)
    channel = Channel(loss, corruption, delay, rtt, rng, verbose)
    if protocol == "gbn":
        sender = GBNSender(packets, window, space, timeout, channel)
        receiver = GBNReceiver(space, channel)
    else:
        sender = SRSender(packets, window, space, timeout, channel)
        receiver = SRReceiver(window, space, channel)
    channel.log(f"START {protocol.upper()} packets={packets} N={window} k={bits} seed={seed}")
    sender.fill()
    steps = 0
    while not sender.done():
        steps += 1
        if steps > 5000000:
            raise RuntimeError("too many steps, check the parameters")
        arrival = channel.nexttime()
        deadline = sender.nexttime()
        if arrival is None and deadline is None:
            raise RuntimeError("nothing left to happen but sender is not done")
        if deadline is None or (arrival is not None and arrival <= deadline):
            channel.now, kind, pkt = channel.pop()
            if kind == "DATA":
                receiver.ondata(pkt)
            else:
                sender.onack(pkt)
        else:
            channel.now = deadline
            sender.ontimeout()
    expected = [f"data{i}" for i in range(packets)]
    elapsed = channel.now
    channel.log(f"COMPLETE delivered={len(receiver.delivered)} sent={sender.sent} retransmissions={sender.retrans} time={elapsed:.3f}s")
    return {
        "protocol": protocol.upper(),
        "sent": sender.sent,
        "retrans": sender.retrans,
        "delivered": len(receiver.delivered),
        "inorder": receiver.delivered == expected,
        "time": elapsed,
        "throughput": len(receiver.delivered) / elapsed,
        "lines": channel.lines,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--protocol", choices=["gbn", "sr"], default="gbn")
    p.add_argument("--packets", type=int, default=200)
    p.add_argument("--window", type=int, default=4)
    p.add_argument("--bits", type=int, default=3)
    p.add_argument("--loss", type=float, default=0.0)
    p.add_argument("--corruption", type=float, default=0.0)
    p.add_argument("--delay", type=float, default=0.0)
    p.add_argument("--timeout", type=float, default=1.0)
    p.add_argument("--seed", type=int, default=625)
    p.add_argument("--rtt", type=float, default=0.5)
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--logfile", default="")
    a = p.parse_args()
    r = simulate(a.protocol, a.packets, a.window, a.bits, a.loss, a.corruption,
                 a.delay, a.timeout, a.seed, a.rtt, not a.quiet)
    print()
    print("SUMMARY")
    print("protocol:", r["protocol"])
    print("packets sent:", r["sent"])
    print("retransmissions:", r["retrans"])
    print("delivered:", r["delivered"])
    print("in order and correct:", r["inorder"])
    print(f"time: {r['time']:.3f} s")
    print(f"throughput: {r['throughput']:.3f} packets per second")
    if a.logfile:
        with open(a.logfile, "w") as f:
            f.write("\n".join(r["lines"]) + "\n")
        print("log saved to", a.logfile)


if __name__ == "__main__":
    main()


# cmds:
# python transfer.py --protocol gbn --packets 10 --window 4 --loss 0.1
# python transfer.py --protocol gbn --packets 10 --window 4 --loss 0.1 --corruption 0.1
