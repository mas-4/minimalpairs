import requests
import json
import sys

word = None
with open('key.txt', 'rt') as f:
    key = f.read().strip()


URLFRONT = ''.join(['https://apifree.forvo.com/key/', key,
       '/format/json/action/word-pronunciations/word/'])
URLBACK = '/language/fr'

def getraw(word):
    """Helper function to compile a word url for the index."""
    url = ''.join([URLFRONT, word, URLBACK])
    resp = requests.get(url)
    return resp

# get the list of words
words = [line.rstrip() for line in open('uniquewords.txt')]
fileindex = [] # a list of dictionaries of words and corresponding file names

def failout():
    """A failsafe to save progress and avoid redownloading files or making
    unnecessary requests, within the limits of my request limit.
    """
    with open('filenames.json', 'w') as fout:
        json.dump(fileindex, fout)
    sys.exit(f'{len(fileindex)}')

for word in words:
    # try to get the index of the word
    worddict = {'word': word}
    try:
        raw = getraw(word)
        if not raw.ok:
            raise ValueError('url fail')
        idx = json.loads(raw.text)
    except:
        failout()

    # compile list of mp3 urls for word
    mp3_urls = []
    for item in idx['items']:
        if item['word'] == word:
            mp3_urls.append(item['pathmp3'])

    worddict['number'] = len(mp3_urls)
    worddict['filenames'] = []

    # download and save mp3's
    for i, url in enumerate(mp3_urls):
        try:
            mp3 = requests.get(url)
            if not mp3.ok:
                raise ValueError('url fail')
        except:
            failout()

        filename = f'files/{word}{i}.mp3'

        with open(filename, 'wb') as fout:
            fout.write(mp3.content)

        worddict['filenames'].append(filename)

    fileindex.append(worddict)

failout()
