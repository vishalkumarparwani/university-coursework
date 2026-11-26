import math

mults = 0


def power_dc(a, n):
    global mults
    if n == 1:
        return a
    left = power_dc(a, n // 2)
    right = power_dc(a, n - n // 2)
    mults += 1
    return left * right


def power_fast(a, n):
    global mults
    if n == 1:
        return a
    half = power_fast(a, n // 2)
    mults += 1
    result = half * half
    if n % 2 == 1:
        mults += 1
        result *= a
    return result


def power_brute(a, n):
    result = a
    count = 0
    for _ in range(n - 1):
        result *= a
        count += 1
    return result, count


def parse_number(token):
    try:
        return int(token)
    except ValueError:
        return float(token)


if __name__ == "__main__":
    while True:
        try:
            a = parse_number(input("Enter the base a: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    while True:
        try:
            n = int(input("Enter the exponent n (positive integer, use 10 or more for the project): "))
            if n >= 1:
                break
        except ValueError:
            pass
        print("The exponent must be a positive integer.")

    mults = 0
    r1 = power_dc(a, n)
    m1 = mults
    mults = 0
    r2 = power_fast(a, n)
    m2 = mults
    r3, m3 = power_brute(a, n)

    if isinstance(r3, int):
        assert r1 == r2 == r3 == a ** n
    else:
        assert math.isclose(r1, r3, rel_tol=1e-9) and math.isclose(r2, r3, rel_tol=1e-9)

    print(f"Result (divide and conquer)       : {r1}")
    print(f"Multiplications - divide & conquer: {m1} (= n - 1)")
    print(f"Multiplications - brute force     : {m3} (= n - 1)")
    print(f"Multiplications - repeated squaring: {m2} (<= 2*floor(log2 n) = {2 * (n.bit_length() - 1)})")
