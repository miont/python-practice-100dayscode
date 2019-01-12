import urllib.request
import sys
import feedparser
from typing import Iterable

# @dataclass  Available in 3.7 only
class Paper:
    ''' Class of data for a paper '''
    def __init__(self, 
        title:str,
        authors:str,
        publication_date:str,
        summary:str=''):

        self.title = title
        self.authors = authors
        self.publication_date = publication_date
        self.summary = summary

    def __repr__(self):
        return '{:s}. {:s}. {:s}'.format(self.authors, self.title, self.publication_date)

    def __str__(self):
        return self.__repr__()

def make_query(query_kwords:Iterable[str]=None, start:int=0, count:int=None):
    """
    Compose query string
    Args:
        query_kwords: query keywords
    """
    if query_kwords is None:
        return 'all'
    search_query = '+AND+'.join(map(lambda s: 'all:'+s, query_kwords))
    query = 'search_query={:s}&start={:d}'.format(search_query, start)
    if not count is None and count > 0:
        query += '&max_results={:d}'.format(count)
    return query

def parse_atom_feed(response:str):
    """
    Parse Atom feed response
    """
    try:
        feed = feedparser.parse(response)
    except Exception as e:
        print('Cant parse response: {:s}'.format(response))
        print(e)
        sys.exit(1)

    papers = []
    for entry in feed.entries:
        paper_info = {}
        paper_info['title'] = entry.title
        paper_info['authors'] = ', '.join(author.name for author in entry.authors)
        paper_info['publication_date'] = entry.published
        paper_info['summary'] = entry.summary

        papers.append(Paper(**paper_info))
    
    return papers

def fetch_arxiv_data(query_kwords:Iterable[str]=None, batch_size:int=50, verbose=False):
    """
    Query papers from arxiv containing keywords
    Args:
        query_kwords: keywords
        batch_size: how many collect at once
    """
    base_url = 'http://export.arxiv.org/api/query?'
    if verbose:
        print('Start fetching data from {:s}'.format(base_url))
    counter = 0
    while True:
        query = make_query(query_kwords, start=counter*batch_size, count=batch_size)
        request_url = base_url + query
        if verbose:
            print('Making request to {:s}'.format(request_url))
        with urllib.request.urlopen(request_url) as f:
            response = f.read()
            data = parse_atom_feed(response)
            if response is None:
                break
            counter += 1
            if verbose:
                print('Batch {:d}'.format(counter))
            yield data
    if verbose:
        print('Finish fetching data.')


def print_papers(papers:Iterable):
    print('\n'.join(map(str, papers)))

def main():
    k = 0
    max_pages = 10
    print('Start collecting data from arXiv')
    for data in fetch_arxiv_data(query_kwords=['biology'], batch_size=5):
        k += 1
        print('------------- Page {:d} -------------'.format(k))
        print_papers(data)
        if k>= max_pages:
            break
    print('We done!')

if __name__ == '__main__':
    main()

