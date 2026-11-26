import random


def quickselect(a, k):
    while True:
        p = random.choice(a)
        lo = [x for x in a if x < p]
        hi = [x for x in a if x > p]
        equal = len(a) - len(lo) - len(hi)
        if k < len(lo):
            a = lo
        elif k < len(lo) + equal:
            return p
        else:
            k -= len(lo) + equal
            a = hi


def closest_pair(s):
    n = len(s)
    m = quickselect(s, (n - 1) // 2)
    s1 = [x for x in s if x <= m]
    s2 = [x for x in s if x > m]
    best = (min(s2) - max(s1), (max(s1), min(s2)))
    for half in (s1, s2):
        if len(half) >= 2:
            cand = closest_pair(half)
            if cand[0] < best[0]:
                best = cand
    return best


def brute_force(s):
    return min(abs(s[i] - s[j]) for i in range(len(s)) for j in range(i + 1, len(s)))


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter the input size n (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


def parse_number(token):
    try:
        return int(token)
    except ValueError:
        return float(token)


def read_values(n):
    mode = input("Type the values yourself (t) or generate them randomly (r)? [t/r]: ").strip().lower()
    if mode == "t":
        while True:
            try:
                vals = [parse_number(x) for x in input(f"Enter {n} numbers separated by spaces: ").split()]
                if len(vals) == n:
                    return vals
                print(f"You entered {len(vals)} values but {n} were expected.")
            except ValueError:
                print("Please enter valid numbers only.")
    return random.sample(range(1, 100 * n + 1), n)


if __name__ == "__main__":
    n = read_size()
    s = read_values(n)
    print("Numbers:", s)
    if len(set(s)) < len(s):
        dup = next(x for x in s if s.count(x) > 1)
        print(f"The set contains a repeated value ({dup}), so the smallest distance is 0.")
    else:
        dist, (x, y) = closest_pair(s)
        assert dist == brute_force(s)
        print(f"Closest pair: ({x}, {y}) with distance {dist}")
