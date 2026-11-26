import math
import random
import sys

sys.setrecursionlimit(20000)

comparisons = 0


def quicksort(a, pivot_rule):
    global comparisons
    if len(a) <= 1:
        return a
    if pivot_rule == "median":
        pivot = sorted(a)[len(a) // 2]
    else:
        pivot = a[0]
    k = a.index(pivot)
    rest = a[:k] + a[k + 1:]
    comparisons += len(rest)
    smaller = [x for x in rest if x < pivot]
    larger = [x for x in rest if x >= pivot]
    return quicksort(smaller, pivot_rule) + [pivot] + quicksort(larger, pivot_rule)


def run(a, rule):
    global comparisons
    comparisons = 0
    result = quicksort(a[:], rule)
    assert result == sorted(a)
    return comparisons


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter the input size n (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


if __name__ == "__main__":
    n = read_size()
    random_input = random.sample(range(1, 10 * n + 1), n)
    sorted_input = sorted(random_input)

    best = run(sorted_input, "median")
    worst = run(sorted_input, "first")
    average = run(random_input, "first")

    harmonic = sum(1 / k for k in range(1, n + 1))
    print(f"n = {n}")
    print(f"Best case  (median pivot)         : {best:>8} comparisons  (about n log2 n = {n * math.log2(n):.0f})")
    print(f"Worst case (first pivot, sorted)  : {worst:>8} comparisons  (n(n-1)/2 = {n * (n - 1) // 2})")
    print(f"Average    (first pivot, random)  : {average:>8} comparisons  "
          f"(expected 2(n+1)H(n) - 4n = {2 * (n + 1) * harmonic - 4 * n:.0f})")
