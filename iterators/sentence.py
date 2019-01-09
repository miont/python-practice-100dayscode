import re
import reprlib
import unittest

RE_WORD = re.compile('\w+')

class Sentence():
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]
    
    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence({:s})'.format(reprlib.repr(self.text))

TEST_TEXT = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
               sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
               Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
               nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
               eprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
               Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
               deserunt mollit anim id est laborum'''


class SentenceTest(unittest.TestCase):
    def test_iter(self):
        s = Sentence(TEST_TEXT)
        iterator1 = iter(s)
        self.assertEqual(next(iterator1), 'Lorem')
        self.assertEqual(next(iterator1), 'ipsum')
        iterator2 = iter(s)
        self.assertEqual(next(iterator2), 'Lorem')

if __name__ == '__main__':
    s = Sentence(TEST_TEXT)
    print(s)

    for w in s:
        print(w)

    print(list(s))

    print('Iterators:')
    iterator1 = iter(s)
    print(next(iterator1))
    print(next(iterator1))
    iterator2 = iter(s)
    print(next(iterator2))

    unittest.main()

