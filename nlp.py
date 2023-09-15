<<<<<<< HEAD
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pathlib


#tokens = word_tokenize(data)  #puedo usar esta forma o la de regular tokenizer

def regextokenizer(data):
    tokenizer=RegexpTokenizer(r'\w+')
    data=tokenizer.tokenize(data)
    return data

def remove_stopwords(data):  
    stop_words=set(stopwords.words('english'))
    new_data=[i for i in data if not i in stop_words]
    return new_data


def tokenizer_stemming(data): 
    stemmer=PorterStemmer()
    tokenizer=RegexpTokenizer(r'\w+')
    tokens=tokenizer.tokenize(data)
    new_data=""
    for i in tokens:
        new_data += " "+stemmer.stem(i)
    return new_data


def lemmatization(data):
    lemmatizer=WordNetLemmatizer()
    new_data=[]
    for word in data:
        new_data.append(lemmatizer.lemmatize(word))
    return new_data

# #Convertir numeros en palabras
# from num2words import num2words
# def convert_numbers(k):
#     for i in range(len(k)):
#         try:
#             k[i] = num2words(int(k[i]))
#         except:
#             pass
#     return k


def read(url):
    cwd = pathlib.Path(url).absolute()
    url = str(cwd)
=======
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pathlib


#tokens = word_tokenize(data)  #puedo usar esta forma o la de regular tokenizer

def regextokenizer(data):
    tokenizer=RegexpTokenizer(r'\w+')
    data=tokenizer.tokenize(data)
    return data

def remove_stopwords(data):  
    stop_words=set(stopwords.words('english'))
    new_data=[i for i in data if not i in stop_words]
    return new_data


def tokenizer_stemming(data): 
    stemmer=PorterStemmer()
    tokenizer=RegexpTokenizer(r'\w+')
    tokens=tokenizer.tokenize(data)
    new_data=""
    for i in tokens:
        new_data += " "+stemmer.stem(i)
    return new_data


def lemmatization(data):
    lemmatizer=WordNetLemmatizer()
    new_data=[]
    for word in data:
        new_data.append(lemmatizer.lemmatize(word))
    return new_data

# #Convertir numeros en palabras
# from num2words import num2words
# def convert_numbers(k):
#     for i in range(len(k)):
#         try:
#             k[i] = num2words(int(k[i]))
#         except:
#             pass
#     return k


def read(url):
    cwd = pathlib.Path(url).absolute()
    url = str(cwd)
>>>>>>> 8cf5136e226be24e505ffb3950831c09a38b0572
    