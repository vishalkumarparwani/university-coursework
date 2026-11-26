import random


def best_trade(p, lo, hi):
    mid = (lo + hi) // 2
    candidates = []
    if mid > lo:
        candidates.append(best_trade(p, lo, mid))
    if hi > mid + 1:
        candidates.append(best_trade(p, mid + 1, hi))
    i = min(range(lo, mid + 1), key=lambda k: p[k])
    j = max(range(mid + 1, hi + 1), key=lambda k: p[k])
    candidates.append((p[j] - p[i], i, j))
    return max(candidates, key=lambda t: t[0])


def brute_force(p):
    return max(p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p)))


def parse_number(token):
    try:
        return int(token)
    except ValueError:
        return float(token)


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter the number of days n (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


def read_values(n):
    mode = input("Type the prices yourself (t) or generate them randomly (r)? [t/r]: ").strip().lower()
    if mode == "t":
        while True:
            try:
                vals = [parse_number(x) for x in input(f"Enter {n} prices separated by spaces: ").split()]
                if len(vals) == n:
                    return vals
                print(f"You entered {len(vals)} prices but {n} were expected.")
            except ValueError:
                print("Please enter valid numbers only.")
    return [random.randint(1, 100) for _ in range(n)]


if __name__ == "__main__":
    n = read_size()
    prices = read_values(n)
    print("Prices:", prices)
    profit, i, j = best_trade(prices, 0, n - 1)
    assert profit == brute_force(prices)
    if profit <= 0:
        print("There is no way to make money during these days.")
    else:
        print(f"Buy on day {i + 1} (price {prices[i]}), sell on day {j + 1} (price {prices[j]}), "
              f"profit per share = {profit}")
