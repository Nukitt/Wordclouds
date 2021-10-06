import requests
import re
import string
from bs4 import BeautifulSoup

#crawling the webpage
def crawl(link):
    res = requests.get(link)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    extractlist = ['p',
                   'h1',
                   'h2',
                   'h3',
                   'h4',
                   'h5',
                   'h6',
                   'b',
                   'i',
                   'u']

    for t in text:
        if t.parent.name in extractlist:
            output += '{} '.format(t)   

    output= re.sub("\n"," ",output)
    return output

url = ['https://en.wikipedia.org/wiki/Basketball'
        ]

raw_data = ''
for link in url:
    raw_data += crawl(link)

#list of all the things to be removed from raw data obtained
num_sym_punct = [
    '1', '2', '3', '4', '5', '6', '8', '7', '9', '0', '-', '₹',
    ',', '.', '"', ':', ')', '(', '!', '?', '|', ';', "'", '$', '&',
    '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
    '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',
    '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', '“', '★', '”',
    '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾',
    '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', '▒', '：', '¼', '⊕', '▼',
    '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲',
    'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', '∙', '）', '↓', '、', '│', '（', '»',
    '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø',
    '¹', '≤', '‡', '√', '«', '»', '´', 'º', '¾', '¡', '§', '£', '₤']

def remove_extra(text,list):
    for extra in list:
        if extra in text:
            text = text.replace(extra, ' ')
    return text.strip()

processed_data = remove_extra(raw_data , num_sym_punct)

# Tokenisation

import nltk
from nltk.tokenize import word_tokenize


nltk.download('punkt')
word_tokens = nltk.word_tokenize(processed_data)

# POS Tagging

nltk.download('averaged_perceptron_tagger')
pos = nltk.pos_tag(word_tokens)

# Stopwords removal

nltk.download('stopwords')
from nltk.corpus import stopwords
tokens_without_stopwords = []
sr = stopwords.words('english')
sr.append('The')
sr.append('com')
sr.append('In')
sr.append('b')
sr.append('also')
sr.append('On')


for token in word_tokens:
    if token not in sr:
        tokens_without_stopwords.append(token)

#stemming

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stemmed = [stemmer.stem(word) for word in word_tokens]
# print(' '.join(stemmed))

#lemmatizing

nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(word) for word in word_tokens]

#Frequencies graphs
# import matplotlib.pyplot as plt

# FreqPro = nltk.FreqDist(word_tokens)
# plt.plot(FreqPro.keys(),FreqPro.values())
# plt.title('Frequency Distribution for processed data')
# plt.xlabel('Words')
# plt.ylabel('Count')
# plt.show()

FreqStop = nltk.FreqDist(tokens_without_stopwords)
# plt.plot(FreqStop.keys(),FreqStop.values())
# plt.title('Frequency Distribution for data with no stopwords') 
# plt.xlabel('Words')
# plt.ylabel('Count')
# plt.show()

# FreqStem = nltk.FreqDist(stemmed)
# plt.plot(FreqStem.keys(),FreqStem.values())
# plt.title('Frequency Distribution for stemmed data') 
# plt.xlabel('Words')
# plt.ylabel('Count')
# plt.show()

# FreqLem = nltk.FreqDist(lemmatized)
# plt.plot(FreqLem.keys(),FreqLem.values())
# plt.title('Frequency Distribution for lemmatized data') 
# plt.xlabel('Words')
# plt.ylabel('Count')
# plt.show()

# Output of frequency in descending order
for word,count in FreqStop.most_common(100):
    print(word + ' = ' + str(count))

# WordCloud
from wordcloud import WordCloud
words_to_disp = [word for word,freq in FreqStop.most_common(100)]
wc = WordCloud().generate(" ".join(words_to_disp))
wc.to_file("wordcloud_english_new.png")
