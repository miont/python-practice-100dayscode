class Source():
    def __init__(self, start=0, step=1, limit=1000):
        self.start = start
        self.val = start
        self.step = step
        self.limit = limit

    def increment(self):
        self.val += self.step
        if self.val > self.limit:
            raise StopIteration()

    def reset(self):
        self.val = self.start

    def __iter__(self):
        return SourceIterator(self)

    
class SourceIterator():
    def __init__(self, iterable):
        self.iterable = iterable

    def __next__(self):
        val = self.iterable.val
        self.iterable.increment()
        return val

if __name__ == '__main__':
    obj = Source(start=3, step=2, limit=10)
    print('Iterator in for loop')
    for i in obj:
        print(i)
    
    print('Explicit iterator usage:')
    obj.reset()
    iterator = iter(obj)
    while True:
        elem = next(iterator)
        print(elem)



