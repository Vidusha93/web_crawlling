import requests
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

print('Collecting Headlines....')

source = requests.get('http://www.koreatimes.co.kr/www2/index.asp').text

soup = BeautifulSoup(source, 'lxml')

text = ''

for headline in soup.find_all('div', class_='index_more_headline HD'):
    try:
        article_link = headline.a.attrs['href']
        source = requests.get("http://www.koreatimes.co.kr" + article_link).text
        soup = BeautifulSoup(source, 'lxml')

        article = soup.find('div', class_='view_article').text

        text += ' ' + article
        print('Geting Article From : http://www.koreatimes.co.kr' + article_link)
    except:
        print('Headline does not have link for article : ', headline.text)


tokens = word_tokenize(text)
tokens = [w.lower() for w in tokens]
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
words = [word for word in stripped if word.isalpha()]
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]

print('Total Words Collected : ', len(words))

words_dict = {}

for word in words:
    if word not in words_dict:
        words_dict[word] = 1
    else:
        words_dict[word] += 1

words_dict = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)

for x, y in words_dict:
    print(x + ' : ', y)
