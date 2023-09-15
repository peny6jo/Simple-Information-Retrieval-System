import enum
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from logging import exception
from pathlib import Path


stop_words=set(stopwords.words('english'))


def regextokenizer(data):
    tokenizer=RegexpTokenizer(r'\w+')
    data=tokenizer.tokenize(data)
    return data

class File:

    def __init__(self) -> None:
        self.indexNumber: int = None
        self.title: str = ''
        self.author: str = ''
        self.info: str = ''
        self.work: str = ''
        self.frequency: dict[str:int]= {}
        self.normalizeFrequency : dict[str:int] = {}
        self.maxFrequency : int= 0
        self.weight: dict[str:int] = {} 

    def __str__(self) -> str:
        return f'****\n{self.indexNumber}:\n{self.title}\n{self.author}\n{self.info}\n{self.work}\n\n'


class Tag(enum.Enum):
    index = ".I"
    title = ".T"
    author = ".A"
    info = ".B"
    work = ".W"
    table = ".X"


def read_query(query: str):
    files: list[File] = []
    collection = File()
    collection.indexNumber = 1
    collection.work = query
    cleanData = [item for item in regextokenizer(query) if not item in stop_words]
    for word in cleanData:
        if word not in collection.frequency:
            collection.frequency[word] = 1
        else:
            collection.frequency[word] += 1
        
        if collection.maxFrequency < collection.frequency[word]:
            collection.maxFrequency = collection.frequency[word]
    
    files.append(collection)
    return  files
        
def read_collection(path):
    globalFrequency = {}
    globalMax = 0
    files: list[File] = []
   # path = Path(f"./collections/{path}") #esto estaba comentado
    currentTag: Tag = None
    tagList = [item.value for item in Tag]
    currentCollection: File = None
    with open(path, 'r') as collectionData:
        currentCollection: File = None
        i = 0
        for line in collectionData:
            i += 1
            if line == '':
                continue

            possibleTag = line[:2]
            # Recognizing text tags.
            if possibleTag in tagList:
                if possibleTag == Tag.index.value:
                    if currentTag is not None:
                        files.append(currentCollection)
                    
                    currentCollection = File()
                    try:
                        _index = int(line.split()[1])
                        currentCollection.indexNumber = _index
                    except:
                        raise Exception(f"Error matching index at line {i}.")
                
                elif possibleTag == Tag.title.value:
                    currentTag = Tag.title
                elif possibleTag == Tag.author.value:
                    currentTag = Tag.author
                elif possibleTag == Tag.info.value:
                    currentTag = Tag.info
                elif possibleTag == Tag.work.value:
                    currentTag = Tag.work
                elif possibleTag == Tag.table.value:
                    currentTag = Tag.table
                else:
                    raise Exception(f'Tag not matched at line {i}.')
                
                continue
            # Adding current taged text.
            else:
                if currentTag is None or currentTag.value not in tagList:
                    raise Exception(f'Attempt to parse untaged text at line {i}.')
                elif currentTag is Tag.table:
                    continue
                else:
                    cleanData = [item for item in regextokenizer(line) if not item in stop_words]
                    for word in cleanData:
                        if word in currentCollection.frequency:
                            currentCollection.frequency[word] += 1
                        else:                            
                            currentCollection.frequency[word] = 1
                            if word in globalFrequency:
                                globalFrequency[word] += 1
                            else:
                                globalFrequency[word] = 1
                            if globalFrequency[word] > globalMax:
                                globalMax = globalFrequency[word]
                        
                        if currentCollection.frequency[word] > currentCollection.maxFrequency:
                            currentCollection.maxFrequency = currentCollection.frequency[word]
                    if currentTag is Tag.author:
                        currentCollection.author += line
                    elif currentTag is Tag.title:
                        currentCollection.title += line
                    elif currentTag is Tag.info:
                        currentCollection.info += line
                    elif currentTag is Tag.work:
                        currentCollection.work += line
            
        if not (currentCollection is None):
            files.append(currentCollection)

    return (globalFrequency, files)


if __name__ == '__main__':
    pass