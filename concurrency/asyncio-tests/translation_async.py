from typing import Iterable
import time 
import asyncio
from googletrans import Translator

INPUT_FNAME = 'data/translation/newstext2013.de'

async def read_source_file(fname:str, max_lines:int):
    with open(fname) as f:
        content = f.readlines()

    print('lines read:', len(content))
    return content[:max_lines]

async def init_translator():
    return Translator()

async def translate(translator, sent:str, id:int):
    print(f'Task {id}: started')
    translated = translator.translate(sent, src='de', dest='en')
    print(f'Task {id} result: {translated}')
    print(f'Task {id}: finished')
    return translated

async def translate_all_sents(translator, sents:Iterable[str]):
    res = [None]*len(sents)
    for i,s in enumerate(sents):
        res[i] = asyncio.ensure_future(translate(translator, s, i+1))
    
    return await asyncio.gather(*res, return_exceptions=True)

async def main():
    sents = await read_source_file(INPUT_FNAME, max_lines=10)
    start = time.perf_counter()
    translated = await translate_all_sents(await init_translator(), sents)
    elapsed = time.perf_counter() - start
    print('*******************')
    print('Results:          *')
    print('*******************')
    for orig, tran in zip(sents, translated):
        print(f'Source: "{orig}"')
        print(f'Translated: "{tran}"')
        print('-----------------------------')
    print(f'Time consumed: {elapsed:.2f} sec')

if __name__ == '__main__':
    asyncio.run(main())