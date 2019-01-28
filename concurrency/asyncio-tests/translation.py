from typing import Iterable
import time
from googletrans import Translator


INPUT_FNAME = 'data/translation/newstext2013.de'

def read_source_file(fname:str, max_lines:int):
    with open(fname) as f:
        content = f.readlines()

    print('lines read:', len(content))
    return content[:max_lines]

def init_translator():
    return Translator()

def translate_all_sents(translator, sents:Iterable[str]):
    res = [None]*len(sents)
    for i,s in enumerate(sents):
        res[i] = translator.translate(s, src='de', dest='en').text
    return res

def main():
    sents = read_source_file(INPUT_FNAME, max_lines=100)
    start = time.perf_counter()
    translated = translate_all_sents(init_translator(), sents)
    elapsed = time.perf_counter() - start
    print('Results:')
    for orig, tran in zip(sents, translated):
        print(f'Source: "{orig}"')
        print(f'Result: "{tran}"')
        print('-----------------------------')
    print(f'Time consumed: {elapsed:.2f} sec')

if __name__ == '__main__':
    main()