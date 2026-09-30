def messy(a, b, c):
    """A deliberately complicated function."""
    if a > 0 and b > 0:
        for i in range(a):
            if i % 2 == 0 or i % 3 == 0:
                while b > 0:
                    b -= 1
                    if c:
                        print(i)
            elif i > 10:
                print("big")
    else:
        try:
            print(a / b)
        except ZeroDivisionError:
            print("error")
        if a < 0:
            print("negative")
    return a