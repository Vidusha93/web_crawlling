import requests
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

newsCategoryUrl = ['http://www.koreatimes.co.kr/www/sublist_129_', 'http://www.koreatimes.co.kr/www/sublist_602_', 'http://www.koreatimes.co.kr/www/sublist_398_']

soupList = []

for url in newsCategoryUrl:
    for i in range(1, 4):
        fullUrl = url + str(i) + '.html'
        print('Collecting Page from URL : ' + fullUrl)
        source = requests.get(fullUrl).text
        soup = BeautifulSoup(source, 'lxml')
        soupList.append(soup)

text = ''

for soup in soupList:
    print('Collecting Headlines From : ' + soup.find('div' , class_='sub_TT subTT').a.text + ' Category')
    for headline in soup.find_all('div', class_='list_article_headline HD'):
        try:
            article_link = headline.a.attrs['href']
            print('Geting Article From : http://www.koreatimes.co.kr' + article_link)
            source = requests.get("http://www.koreatimes.co.kr" + article_link).text
            soup = BeautifulSoup(source, 'lxml')
            article = soup.find('div', class_='view_article').text
            text += ' ' + article
        except:
            print('Headline does not have link for article : ', headline.text)


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