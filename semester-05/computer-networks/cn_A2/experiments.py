import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from transfer import simulate

SEED = 625

scenarios = [
    ("A reliable", dict(loss=0.0, corruption=0.0, delay=0.0)),
    ("B loss 0.10", dict(loss=0.10, corruption=0.0, delay=0.0)),
    ("C mixed", dict(loss=0.05, corruption=0.05, delay=0.10)),
]


def main():
    rows = []
    for name, cfg in scenarios:
        for protocol in ("gbn", "sr"):
            r = simulate(protocol, 200, 4, 3, seed=SEED, **cfg)
            rows.append([name, r["protocol"], r["sent"], r["retrans"],
                         r["delivered"], round(r["time"], 2), round(r["throughput"], 3)])

    header = ["Scenario", "Protocol", "Transmitted", "Retransmissions",
              "Delivered", "Time s", "Throughput pps"]
    print(" | ".join(header))
    for row in rows:
        print(" | ".join(str(x) for x in row))

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    names = [s[0] for s in scenarios]
    gbn = [r for r in rows if r[1] == "GBN"]
    sr = [r for r in rows if r[1] == "SR"]
    x = range(len(names))

    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
    left.bar([i - 0.2 for i in x], [r[3] for r in gbn], 0.4, label="GBN")
    left.bar([i + 0.2 for i in x], [r[3] for r in sr], 0.4, label="SR")
    left.set_xticks(list(x))
    left.set_xticklabels(names)
    left.set_ylabel("Retransmissions")
    left.set_title("Retransmissions")
    left.legend()

    right.bar([i - 0.2 for i in x], [r[6] for r in gbn], 0.4, label="GBN")
    right.bar([i + 0.2 for i in x], [r[6] for r in sr], 0.4, label="SR")
    right.set_xticks(list(x))
    right.set_xticklabels(names)
    right.set_ylabel("Packets per second")
    right.set_title("Throughput")
    right.legend()

    fig.suptitle("GBN vs SR, 200 packets, N = 4, k = 3, seed 625")
    fig.tight_layout()
    fig.savefig("gbn_vs_sr.png", dpi=150)
    print("saved results.csv and gbn_vs_sr.png")


if __name__ == "__main__":
    main()
