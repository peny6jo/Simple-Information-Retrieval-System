import math
from utils import readDocument, printRank, relevanceFunc
from evaluationSystem import RR_RI_NR, Precision, Recobrado, Medida_F


def weightVector_tf(document):
    weightVector = {}
    max_freq = -1
    value = 0
    for item in document:
        if document[item] > max_freq:
            max_freq = document[item]
        weightVector[item] = document[item]
    for item in weightVector:
        weightVector[item] = weightVector[item]/max_freq
    return weightVector

def matrix_tf(documentList,documentsWords):
    matrix = []
    for item in documentList:
        row = weightVector_tf(item[1])
        matrix.append(row)
    return matrix

def weightVector_idf(documentList,documentsWords):
    weightVector = {}
    amountDocCollection = len(documentList)
    for item in documentsWords:
        weightVector[item] = math.log10(amountDocCollection/documentsWords[item])
    return weightVector

def documentWeight(url):
    documentsWords ,documentList = readDocument(url)
    tf = matrix_tf(documentList,documentsWords)
    idf = weightVector_idf(documentList, documentsWords)
    return makeMatrix(tf,idf,lambda x , y : x * y,documentList)

def makeMatrix(tf,idf,lambdaFunc,documentList=[]):
    matrix_w = []
    for i in range(len(tf)):
        temp = {}
        for j in idf:
            if tf[i].get(j) != None:
                term = tf[i][j]
                temp[j] = lambdaFunc(term,idf[j])
        if len(documentList) > 0:
            matrix_w.append((documentList[i][0],temp))
        else:
            matrix_w.append(temp)
    return matrix_w

def queryWeight(url,a=0.5):
    querysWords ,queryList = readDocument(url)
    tf = matrix_tf(queryList,querysWords)
    idf = weightVector_idf(queryList, querysWords)
    return makeMatrix(tf,idf, lambda x , y : y*((a + (1-a)*x)))

def similitud(vectorQuery,vectorDocument):
    numerador = 0
    normaQuery = 0
    normaDocument = 0
    for item in vectorQuery:
        if vectorDocument.get(item) != None:
            numerador += vectorQuery[item] * vectorDocument[item]
        normaQuery += vectorQuery[item]**2
    for item in vectorDocument:
        normaDocument += vectorDocument[item]**2
    if (math.sqrt(normaQuery) * math.sqrt(normaDocument)) == 0:
        return 0
    return numerador/(math.sqrt(normaQuery) * math.sqrt(normaDocument))

def rank(queryWeight,documentWeight):
    resultRank = []
    cquery = 0
    for item in queryWeight:
        cquery += 1
        temp = []
        if len(item) > 0:
            for element in documentWeight:
                if len(element[1]) == 0:
                    break
                sim = relevanceFunc(similitud(item,element[1]))
                if sim < 5:
                    temp.append((cquery,element[0],sim))
            temp.sort(key=lambda x:x[2])
        resultRank.append(temp)
    return resultRank

def main():

    # urlQuery = 'collections/CISI.QRY'
    # urlDocument = 'collections/CISI.ALL'
    # urlAnswers = 'collections/CISI.REL'

    urlQuery = "collections/cran.qry"
    urlDocument = "collections\cran.txt"
    urlAnswers = "collections/cranqrel"

    dw = documentWeight(urlDocument)
    qw = queryWeight(urlQuery)
    
    r = rank(qw,dw)
    
    printRank(r)
    print('Calculando metricas de evaluacion...')
    RR, RI, NR = RR_RI_NR(urlAnswers,r)

    precision = Precision(RR,RI)
    recobrado = Recobrado(RR,NR)

    print('Precision: ' + str(precision))
    print('Recobrado: ' + str(recobrado))

    mf = Medida_F(precision,recobrado)
    print('Medida_F(beta=1): ' + str(mf))

if __name__ == '__main__':
    main()