import random

comparisons = 0


def minmax(a, left, right):
    global comparisons
    if left == right:
        return a[left], a[left]
    if right == left + 1:
        comparisons += 1
        if a[left] < a[right]:
            return a[left], a[right]
        return a[right], a[left]
    mid = (left + right) // 2
    min1, max1 = minmax(a, left, mid)
    min2, max2 = minmax(a, mid + 1, right)
    comparisons += 2
    return (min1 if min1 < min2 else min2), (max1 if max1 > max2 else max2)


def brute_force(a):
    count = 0
    lo = hi = a[0]
    for x in a[1:]:
        count += 1
        if x < lo:
            lo = x
    for x in a[1:]:
        count += 1
        if x > hi:
            hi = x
    return lo, hi, count


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
    return [random.randint(-1000, 1000) for _ in range(n)]


if __name__ == "__main__":
    n = read_size()
    a = read_values(n)
    print("Array:", a)

    comparisons = 0
    smallest, largest = minmax(a, 0, n - 1)
    lo, hi, bf_count = brute_force(a)
    assert (smallest, largest) == (lo, hi) == (min(a), max(a))

    print("Minimum:", smallest)
    print("Maximum:", largest)
    print(f"Comparisons - divide and conquer: {comparisons}")
    print(f"Comparisons - brute force       : {bf_count} (= 2n - 2)")
    if n & (n - 1) == 0:
        print(f"Formula 3n/2 - 2 for n = 2^k    : {3 * n // 2 - 2}")
