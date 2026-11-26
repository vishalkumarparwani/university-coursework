import random

INF = float("inf")


class Database:
    def __init__(self, values):
        self._v = sorted(values)
        self.queries = 0

    def query(self, k):
        self.queries += 1
        return self._v[k - 1]


def median_of_two(A, B, n):
    lo, hi = 0, n
    while True:
        i = (lo + hi) // 2
        j = n - i
        a_i = A.query(i) if i >= 1 else -INF
        a_i1 = A.query(i + 1) if i < n else INF
        b_j = B.query(j) if j >= 1 else -INF
        b_j1 = B.query(j + 1) if j < n else INF
        if a_i > b_j1:
            hi = i - 1
        elif b_j > a_i1:
            lo = i + 1
        else:
            return max(a_i, b_j)


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter n, the number of values in EACH database (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


def read_databases(n):
    mode = input("Type the values yourself (t) or generate them randomly (r)? [t/r]: ").strip().lower()
    if mode == "t":
        while True:
            try:
                a = [int(x) for x in input(f"Enter the {n} values of database A: ").split()]
                b = [int(x) for x in input(f"Enter the {n} values of database B: ").split()]
                if len(a) == n and len(b) == n and len(set(a + b)) == 2 * n:
                    return a, b
                print("Each database needs n values and all 2n values must be distinct.")
            except ValueError:
                print("Please enter valid integers only.")
    vals = random.sample(range(1, 100 * n + 1), 2 * n)
    return vals[:n], vals[n:]


if __name__ == "__main__":
    n = read_size()
    a_vals, b_vals = read_databases(n)
    A, B = Database(a_vals), Database(b_vals)
    print("Database A:", sorted(a_vals))
    print("Database B:", sorted(b_vals))
    med = median_of_two(A, B, n)
    assert med == sorted(a_vals + b_vals)[n - 1]
    print(f"Median (n-th smallest of the 2n values): {med}")
    print(f"Queries used: {A.queries + B.queries}   (n = {n}, 2n = {2 * n} values in total)")
