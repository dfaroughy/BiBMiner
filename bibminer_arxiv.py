import urllib.request
import requests
import urllib3
import ssl
import sys
import json
import random
import feedparser

def fetch(url):
    with urllib.request.urlopen(url, context=ssl.SSLContext()) as response:
        http=response.read()
        http=http.decode('utf-8')
        return http

def get_arxiv(eprint):
    arxiv=fetch('http://export.arxiv.org/api/query?search_query={}'.format(eprint))
    arxiv=feedparser.parse(arxiv).entries[0]
    print('Title: {}\n'.format(arxiv.title))
    for author in arxiv.authors: print('       '+author.name)
    print('\nAbstract:', arxiv.summary)
    try: print('doi:', arxiv.arxiv_doi)
    except AttributeError:
        pass
    print(arxiv.id)


key='hep-ph/9605326'
key='10.1103/PhysRevLett.77.5172'
key='1905.08498'

get_arxiv(key)