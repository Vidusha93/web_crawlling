import requests
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tqdm import tqdm

newsCategoryUrl = ['http://www.koreatimes.co.kr/www/sublist_129_', 'http://www.koreatimes.co.kr/www/sublist_602_', 'http://www.koreatimes.co.kr/www/sublist_398_']
print("www.koreatimes.co.kr Web Crawlling")
soupList = []
pbar = tqdm(newsCategoryUrl, leave=False)
for url in pbar:
    for i in range(1, 4):
        fullUrl = url + str(i) + '.html'
        pbar.set_description(fullUrl)
        source = requests.get(fullUrl).text
        soup = BeautifulSoup(source, 'lxml')
        soupList.append(soup)

text = ''
gotArtical = 0
for soup in soupList:
    category = soup.find('div' , class_='sub_TT subTT').a.text
    headlineBar = tqdm(soup.find_all('div', class_='list_article_headline HD'), leave=False)
    for headline in headlineBar:
        try:
            article_link = headline.a.attrs['href']
            headlineBar.set_description("Getting Artical frome " + category + " ")
            source = requests.get("http://www.koreatimes.co.kr" + article_link).text
            soup = BeautifulSoup(source, 'lxml')
            article = soup.find('div', class_='view_article').text
            text += ' ' + article
        except:
            gotArtical += 1
print(gotArtical, " Headlines does not have link for Artical!")
print(" ")

tokens = word_tokenize(text)
tokens = [w.lower() for w in tokens]
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
words = [word for word in stripped if word.isalpha()]
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]
porter = PorterStemmer()
stemmed = [porter.stem(word) for word in words]

print('Total Words Collected : ', len(words))

words_dict = {}

for word in stemmed:
    if word not in words_dict:
        words_dict[word] = 1
    else:
        words_dict[word] += 1

words_dict = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)


print(words_dict[:10])