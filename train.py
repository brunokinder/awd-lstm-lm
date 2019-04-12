import json
import requests
import bs4
import pickle
import data
import os

from sklearn.model_selection import train_test_split
#response = requests.get('http://dev.newsplay.info/api/Values?startid=734327&endid=734327')
#response = requests.get('https://www.google.com/search?q=On+ne+pourra+pas+reprocher+aux+S%C3%A9nateurs+de+ne+pas+se+sentir+comme+les+n%C3%A9glig%C3%A9s+dans+leur+s%C3%A9rie+de+premier+tour+face+au+Tricolore.&oq=On+ne+pourra+pas+reprocher+aux+S%C3%A9nateurs+de+ne+pas+se+sentir+comme+les+n%C3%A9glig%C3%A9s+dans+leur+s%C3%A9rie+de+premier+tour+face+au+Tricolore')

#soup = bs4.BeautifulSoup(response.content)
#href = soup.find('h3').find('a').get('href')
#print(href)

def write_file(text, filename):
    with open(os.path.join("data/articles", filename), "w", encoding="utf-8") as f:
        for i in range(len(text)):
            f.write(text[i]['Description'])

def get_training_and_testing_sets(file_list):
    split = 0.7
    shuffle(file_list)
    split_index = floor(len(file_list) * split)
    training = file_list[:split_index]
    testing = file_list[split_index:]
    return training, testing

def read_pickle():
      
      with open( "data/jm/train.pickle", "rb" ) as f:
        train = pickle.load(f)
    
      with open( "data/jm/valid.pickle", "rb" ) as f:
        valid = pickle.load(f)

      print(len(train))
      print(len(valid))



def json_to_text():

    with open( "data/articles/articles.pickle", "rb" ) as f:
        articles = pickle.load(f)

   # corpus = data.Corpus()

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


#read_pickle()
json_to_text()