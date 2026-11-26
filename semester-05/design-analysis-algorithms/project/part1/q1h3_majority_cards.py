import math
import random
from collections import Counter

tests = 0


class Cards:
    def __init__(self, accounts):
        self._acc = accounts

    def equivalent(self, i, j):
        global tests
        tests += 1
        return self._acc[i] == self._acc[j]


def majority(cards, idx):
    if len(idx) == 1:
        return idx[0]
    mid = len(idx) // 2
    candidates = [majority(cards, idx[:mid]), majority(cards, idx[mid:])]
    for cand in candidates:
        if cand is None:
            continue
        count = 1 + sum(1 for c in idx if c != cand and cards.equivalent(cand, c))
        if count > len(idx) / 2:
            return cand
    return None


def read_size(minimum=10):
    while True:
        try:
            n = int(input(f"Enter the number of cards n (at least {minimum}): "))
            if n >= minimum:
                return n
        except ValueError:
            pass
        print("Invalid size, please try again.")


def read_accounts(n):
    mode = input("Type the hidden account numbers yourself (t) or generate them randomly (r)? [t/r]: ").strip().lower()
    if mode == "t":
        while True:
            try:
                vals = [int(x) for x in input(
                    f"Enter {n} account numbers (cards with equal numbers are equivalent): ").split()]
                if len(vals) == n:
                    return vals
                print(f"You entered {len(vals)} values but {n} were expected.")
            except ValueError:
                print("Please enter valid integers only.")
    if random.random() < 0.5:
        big = n // 2 + 1 + random.randint(0, n // 4)
        accounts = [7] * big + [random.randint(100, 100 + n) for _ in range(n - big)]
        random.shuffle(accounts)
        return accounts
    return [random.randint(1, max(2, n // 2)) for _ in range(n)]


if __name__ == "__main__":
    n = read_size()
    accounts = read_accounts(n)
    print("Hidden account numbers (for checking only):", accounts)
    cards = Cards(accounts)
    tests = 0
    winner = majority(cards, list(range(n)))

    top_account, top_count = Counter(accounts).most_common(1)[0]
    assert (winner is not None) == (top_count > n / 2)

    if winner is None:
        print("No set of more than n/2 equivalent cards exists.")
    else:
        size = sum(1 for a in accounts if a == accounts[winner])
        print(f"YES: {size} of the {n} cards are equivalent (more than n/2 = {n / 2}).")
    print(f"Equivalence-tester calls: {tests}   (2 n log2 n = {2 * n * math.log2(n):.0f})")
