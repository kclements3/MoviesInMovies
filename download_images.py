import imdb
import requests
from bs4 import BeautifulSoup
import os
import pickle as pkl
from collections import Counter


Imdb = imdb.Cinemagoer()
f = open('titles_in_network.txt')
# search_confirm = ''

def letter_commonality(word1, word2):
    w1 = Counter(word1)
    w2 = Counter(word2)
    for letter, c in w1.items():
        if letter in w2.keys():
            w2[letter] -= w1[letter]

    return sum(w2.values())


def search(ia, movie_search):
    results = ia.search_movie(movie_search)
    counter = 0
    while len(results) == 0 and counter < 10:
        results = ia.search_movie(movie_search)
        counter += 1
        print(counter, movie_search)
    if len(results) > 0:
        for res in range(len(results)):
            title = results[res]['long imdb title']
            if 'cast' not in results[res].keys():
                ia.update(results[res], 'full credits')
            if 'cast' in results[res]:
                cast = results[res]['cast']
                print(title, cast[0]['name'], results[res]['kind'])
                if abs(letter_commonality(title, movie_search)) < 6:
                    found = 'y'
                else:
                    found = input("Does this match %s (y/n)?"%(movie_search))
                if found.lower() == 'y':
                    return results[res]
    print('No titles found, try again')
    return []

movie_nodes = pkl.load(open('map.pkl', 'rb'))
# lines = f.readlines()
lines = list(movie_nodes.keys())
rileyInd = lines.index('Riley (2011)')
# rileyInd = 1
for line in lines[rileyInd+1:]:
    title = line.rstrip('\n')
    if title not in os.listdir('images'):
        res = search(Imdb, title)
        if len(res) == 0:
            continue
        # counter = 0
        # while len(res) == 0 and counter < 10:
        #     res = search(Imdb, title)
        #     counter += 1
        #     print(counter, title)
        print('Entering {}, {} {} for {}'.format(res['title'], res['year'], res['kind'], line.strip('\n')))
        img_url = res['full-size cover url']
        response = requests.get(img_url)
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                raise ('No response for ' + img_url)
        except:
            print('Cant get '+title)
            continue

        meta = soup.find(id='meta')
        try:
            if title not in os.listdir('images'):
                imageFile = open(os.path.join('images', title),
                                 'wb')
                print('Downloading ' + title)
                for chunk in response.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
        except:
            print('No Image for ' + title)
            continue


