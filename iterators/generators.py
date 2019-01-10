from collections.abc import Iterable, Iterator

def gen(n:int=10):
    for i in range(n):
        yield i

if __name__ == '__main__':
    print(gen)
    print(gen())
    print(gen.__sizeof__())
    print(gen().__sizeof__())
    g = gen(3)
    print(isinstance(g, Iterator))
    print(next(g))
    print(next(g))
    print(next(g))