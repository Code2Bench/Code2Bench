

def combine_nums(a, b):
    # Implicitly makes assumptions about the order of operations and valid operations
    a = int(a)
    b = int(b)
    possible = [[a + b, f"{a}+{b}={a+b}"], [a * b, f"{a}*{b}={a*b}"]]
    if a <= b:
        possible.append([b - a, f"{b}-{a}={b-a}"])
        if a != 0 and b % a == 0:
            possible.append([b // a, f"{b}/{a}={round(b//a,0)}"])
    else:
        possible.append([a - b, f"{a}-{b}={a-b}"])
        if b != 0 and a % b == 0:
            possible.append([a // b, f"{a}/{b}={round(a//b,0)}"])
    return possible