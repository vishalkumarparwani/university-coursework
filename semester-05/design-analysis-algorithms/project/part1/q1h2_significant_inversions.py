import random


def sort_and_count(a):
    if len(a) <= 1:
        return a[:], 0
    mid = len(a) // 2
    left, c_left = sort_and_count(a[:mid])
    right, c_right = sort_and_count(a[mid:])

    cross, p = 0, 0
    for x in left:
        while p < len(right) and 2 * right[p] < x:
            p += 1
        cross += p

    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, c_left + c_right + cross


def brute_force(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > 2 * a[j])


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
                vals = [int(x) for x in input(f"Enter {n} integers separated by spaces: ").split()]
                if len(vals) == n:
                    return vals
                print(f"You entered {len(vals)} values but {n} were expected.")
            except ValueError:
                print("Please enter valid integers only.")
    return random.sample(range(1, 10 * n + 1), n)


if __name__ == "__main__":
    n = read_size()
    a = read_values(n)
    print("Sequence:", a)
    _, count = sort_and_count(a)
    assert count == brute_force(a)
    print("Number of significant inversions (a_i > 2*a_j, i < j):", count)
