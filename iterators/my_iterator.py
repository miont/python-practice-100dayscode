import collections.abc as abc

class Source():
    def __init__(self, start=0, step=1, limit=1000):
        self.start = start
        self.val = start
        self.step = step
        self.limit = limit

    def increment(self):
        self.val += self.step

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
        if self.iterable.val > self.iterable.limit:
            raise StopIteration()
        return val

    def __iter__(self):
        return self

if __name__ == '__main__':
    obj = Source(start=3, step=2, limit=10)
    print('Iterator in for loop')
    for i in obj:
        print(i)
    
    print('Explicit iterator usage:')
    obj.reset()
    it = iter(obj)
    
    print('Iteration:')
    while True:
        try:
            print(next(it))
        except StopIteration:
            del it
            print('Stop iteration!')
            break
    
    print('Is iterable:', isinstance(obj, abc.Iterable))

    # Try to iterate not iterable object
    class C:
        def __init__(self):
            pass
        
    c = C()
    try:
        next(c)
    except TypeError as err:
        print('' + err.__class__.__name__ + ': ' + err.__str__())



