#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup
import os.path


def download_file(url):
    '''
    http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    '''
    local_filename = 'episodes/%s-%s' % (
        url.split('/')[-2],
        url.split('/')[-1]
    )
    if not os.path.isfile(local_filename):
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    return local_filename


if __name__ == '__main__':
    root = 'http://talkpython.fm'
    response = requests.get('%s/episodes/all' % root)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find('table').find_all('a'):
        episode = requests.get('%s%s' % (root, link.attrs.get('href')))
        soup = BeautifulSoup(episode.text, 'html.parser')
        download_file(
            '%s%s' % (root, soup.find('a', 'subscribe-btn').attrs.get('href'))
        )
