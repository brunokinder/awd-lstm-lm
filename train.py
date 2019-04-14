import json
import requests
import bs4
import pickle
import data
import os

from sklearn.model_selection import train_test_split

def write_file(text, filename):
    with open(os.path.join("data/articles", filename), "w", encoding="utf-8") as f:
        for i in range(len(text)):
            f.write(text[i]['Description'])

def split_train():
    with open( "data/jm/train.pickle", "rb" ) as f:
        articles = pickle.load(f)
        
    train, test = train_test_split(articles, test_size=0.1)

    with open('data/jm/new_train.pickle', 'wb') as f:
        pickle.dump(train, f)

    with open('data/jm/test.pickle', 'wb') as f:
        pickle.dump(test, f)

def read_pickle(path, dest):
      
    with open(path, "rb" ) as f:
        train = pickle.load(f)

    text = ""
    for article in train:
        text += "\n".join([" ".join(sentence) for sentence in article.text])

    with open(dest, "w", encoding="utf-8" ) as f:
        f.write(text)


def json_to_text(path_pickle):

    with open(path_pickle, "rb" ) as f:
        articles = pickle.load(f)

    train, valid = train_test_split(articles, test_size=0.1)
    train, test = train_test_split(train, test_size=0.1)
    
    write_file(train, "train.txt")
    write_file(valid, "valid.txt")
    write_file(test, "test.txt")

def fetch():
    all_json = []
    step = 10000
    i = 0
    while i < 734328:
        response = requests.get(f'http://dev.newsplay.info/api/Values?startid={i}&endid={i + step}')
        i += step
        all_json.extend(response.json())
        print(len(all_json))

    with open('data/articles/articles.pickle', 'wb') as f:
        pickle.dump(all_json, f)


#read_pickle("data/jm/new_train.pickle", "data/jm/train.txt")
read_pickle("data/jm/test.pickle", "data/jm/test.txt")
read_pickle("data/jm/valid.pickle", "data/jm/valid.txt")
#json_to_text()