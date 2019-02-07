def fibonacci():
    if not 'a' in locals():
        a = 0
    if not 'b' in locals():
        b = 1
    while True:
        yield a
        a, b = b, a + b

def print_numbers(n):
    for i, x in enumerate(fibonacci()):
        print(x)
        if i >=n:
            break

if __name__ == '__main__':
    print_numbers(20)