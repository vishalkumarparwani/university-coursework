import random

reads = 0


def peak(a, lo, hi):
    global reads
    if lo == hi:
        return lo
    mid = (lo + hi) // 2
    reads += 2
    if a[mid] < a[mid + 1]:
        return peak(a, mid + 1, hi)
    return peak(a, lo, mid)


def is_unimodal(a):
    p = a.index(max(a))
    return all(a[i] < a[i + 1] for i in range(p)) and all(a[i] > a[i + 1] for i in range(p, len(a) - 1))


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter the input size n (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


def read_values(n):
    mode = input("Type the values yourself (t) or generate them randomly (r)? [t/r]: ").strip().lower()
    if mode == "t":
        while True:
            try:
                vals = [int(x) for x in input(f"Enter {n} distinct integers forming a unimodal sequence: ").split()]
                if len(vals) == n and is_unimodal(vals):
                    return vals
                print("The input must have exactly n values and rise to a peak, then fall.")
            except ValueError:
                print("Please enter valid integers only.")
    vals = sorted(random.sample(range(1, 10 * n + 1), n))
    top = vals.pop()
    left, right = [], []
    for v in vals:
        (left if random.random() < 0.5 else right).append(v)
    return sorted(left) + [top] + sorted(right, reverse=True)


if __name__ == "__main__":
    n = read_size()
    a = read_values(n)
    print("Array:", a)
    reads = 0
    p = peak(a, 0, n - 1)
    assert a[p] == max(a)
    print(f"Peak entry: {a[p]} at position {p + 1} (1-indexed)")
    print(f"Array entries read: {reads}   (n = {n}, entries read stay O(log n))")
