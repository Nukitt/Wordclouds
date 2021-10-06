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

url = ['https://hi.wikipedia.org/wiki/%E0%A4%97%E0%A5%8D%E0%A4%B2%E0%A5%87%E0%A4%B6%E0%A4%BF%E0%A4%AF%E0%A4%B0_%E0%A4%A8%E0%A5%87%E0%A4%B6%E0%A4%A8%E0%A4%B2_%E0%A4%AA%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%95'
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
    '¹', '≤', '‡', '√', '«', '»', '´', 'º', '¾', '¡', '§', '£', '₤', '।']

#removing the english letters that might occur in the articles

eng_lowletters = list(string.ascii_lowercase)
eng_upletters = list(string.ascii_uppercase)

def remove_extra(text,list):
    for extra in list:
        if extra in text:
            text = text.replace(extra, ' ')
    return text.strip()

processed_data_1 = remove_extra(raw_data , num_sym_punct)
processed_data_2 = remove_extra(processed_data_1 , eng_lowletters)
processed_data = remove_extra(processed_data_2 , eng_upletters)

#setting up nltk

import nltk
from nltk.tokenize import word_tokenize

#tokenization

nltk.download('punkt')
word_tokens = nltk.word_tokenize(processed_data)

#POS tagging

nltk.download('universal_tagset')
pos = nltk.pos_tag(word_tokens)

# Stopwords removal

nltk.download('stopwords')
from nltk.corpus import stopwords
tokens_without_stopwords = []
sr = stopwords.words('hindi')

for token in word_tokens:
    if token not in sr:
        tokens_without_stopwords.append(token)

#stemming

def stem(word):
    suffixes = {
        1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],  
        2: [u"तृ",u"ान",u"ैत",u"ने",u"ाऊ",u"ाव",u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"नी",u"ना",u"ते",u"ीं",u"ती",
            u"ता",u"ाँ",u"ां",u"ों",u"ें",u"ीय",u"ति",u"या", u"पन", u"पा",u"ित",u"ीन",u"लु",u"यत",u"वट",u"लू"],     
        3: [u"ेरा",u"त्व",u"नीय",u"ौनी",u"ौवल",u"ौती",u"ौता",u"ापा",u"वास",u"हास",u"काल",u"पान",u"न्त",u"ौना",u"सार",u"पोश",u"नाक",
            u"ियल",u"ैया", u"ौटी",u"ावा",u"ाहट",u"िया",u"हार", u"ाकर", u"ाइए", u"ाईं", u"ाया", u"ेगी", u"वान", u"बीन",
            u"ेगा", u"ोगी", u"ोगे", u"ाने", u"ाना", u"ाते", u"ाती", u"ाता", u"तीं", u"ाओं", u"ाएं", u"ुओं", u"ुएं", u"ुआं",u"कला",u"िमा",u"कार",
            u"गार", u"दान",u"खोर"],     
        4: [u"ावास",u"कलाप",u"हारा",u"तव्य",u"वैया", u"वाला", u"ाएगी", u"ाएगा", u"ाओगी", u"ाओगे", 
            u"एंगी", u"ेंगी", u"एंगे", u"ेंगे", u"ूंगी", u"ूंगा", u"ातीं", u"नाओं", u"नाएं", u"ताओं", u"ताएं", u"ियाँ", u"ियों", u"ियां",
            u"त्वा",u"तव्य",u"कल्प",u"िष्ठ",u"जादा",u"क्कड़"],     
        5: [u"ाएंगी", u"ाएंगे", u"ाऊंगी", u"ाऊंगा", u"ाइयाँ", u"ाइयों", u"ाइयां", u"अक्कड़",u"तव्य:",u"निष्ठ"],}
    for L in 5, 4, 3, 2, 1:
	    if len(word) > L + 1:
		    for suf in suffixes[L]:
			    if word.endswith(suf):
				    return word[:-L]
    return word
stemmed = [stem(word) for word in word_tokens]

#lemmatizing

def lemma(word):
	suffixes = {
    1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
    2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],
    3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
    4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
    5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"],}
	for L in 5, 4, 3, 2, 1:
	    if len(word) > L + 1:
		    for suf in suffixes[L]:
			    if word.endswith(suf):
				    return word[:-L]
	return word
lemmatized = [lemma(word) for word in word_tokens]

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
for word,count in FreqStop.most_common(50):
    print(word + ' = ' + str(count))

# WordCloud
from wordcloud import WordCloud
words_to_disp = [word for word,count in FreqStop.most_common(50)]
wc = WordCloud(font_path='Lohit-Devanagari.ttf',regexp=r"[\u0900-\u097F]+",height=400,width=800).generate(" ".join(words_to_disp))
wc.to_file("wordcloud_hin_new.png")