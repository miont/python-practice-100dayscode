import re
import reprlib
import unittest

RE_WORD = re.compile('\w+')

class Sentence():
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence({:s})'.format(reprlib.repr(self.text))

    def __iter__(self):
        # for match in RE_WORD.finditer(self.text):
        #     yield match.group()
        return (match.group() for match in RE_WORD.finditer(self.text))


TEST_TEXT = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
               sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
               Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
               nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
               eprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
               Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
               deserunt mollit anim id est laborum'''


if __name__ == '__main__':
    s = Sentence(TEST_TEXT)
    print(iter(s))
    for w in s:
        print(w)