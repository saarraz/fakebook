import requests
import os
words = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'words.txt'), 'rb').read().decode('utf-8')

def has_wikipedia_article(word):
    res = requests.get('http://he.wikipedia.org/wiki/' + word)
    if res.status_code == 200:
        return len(res.content)
    return 0

def word_score(word, depth=0):
    stripped = word.replace('.', '').replace(',', '').replace('!', '').replace('-', '').replace(' ', '').replace('\n', '').replace(')', '').replace('(', '')
    if depth <= 1 and any(stripped.startswith(x) for x in ('ו', 'ה', 'ל', 'ב', 'ש')):
        for score, w in word_score(stripped[1:], depth + 1):
            yield score, w
    if depth <= 1 and any(stripped.endswith(x) for x in ('ות', 'ים')):
        for score, w in word_score(stripped[:-2], depth + 1):
            yield score, w
    if stripped in words:
        freq = words.index(stripped)
    else:
        freq = 1000
    freq /= 10000.
    wikilen = has_wikipedia_article(stripped)
    freq += min(wikilen / 70000., 1)
    yield freq, stripped
        
    
def get_topic(stream):
    scores = [x for w in stream.split(' ') for x in word_score(w)]
    best_words = sorted([s for s in scores if s])
    for freq, word in best_words[::-1]:
        return word
    raise ValueError('Couldn\'t determine topic')
    # return sorted(w for w in stream.split(' ') if w not in words)
    
if __name__ == '__main__':
    open('topic.txt', 'wb').write(get_topic(open('a.txt', 'rb').read().decode('utf-8')).encode('utf-8'))
    # open('topic.txt', 'wb').write(repr(get_topic(open('a.txt', 'rb').read().decode('utf-8'))).encode('utf-8'))
