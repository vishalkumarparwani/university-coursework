import random


def sort_and_count(a):
    if len(a) <= 1:
        return a[:], 0
    mid = len(a) // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])

    merged, i, j, inv_cross = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            inv_cross += len(left) - i
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + inv_cross


def brute_force(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


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
    sorted_a, count = sort_and_count(a)
    assert count == brute_force(a)
    print("Sorted array:", sorted_a)
    print("Number of inversions:", count)
