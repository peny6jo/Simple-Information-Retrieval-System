from nltk.tokenize import word_tokenize
import nltk
# nltk.download('punkt')
from pathlib import Path

''' 
RR: Relevant Recovery
RI: Irrelevant Recovery
NR: Non Recovery Relevant
NI: Non Recovery Irrelevant
doc: list with all the recovery documents sorted by ranking with their clasiffication

'''
def read_collection_answers(url_answers):
    # path = Path(f"./collections/{url_answers}")
    doc = open(url_answers,"r")
    lines = doc.readlines()
    doc.close()
    index_doc = 1
    temp2 = []
    recovered_answers :list[(int,int)] = []
    for line in lines :
        temp1 = word_tokenize(line)
        if int(temp1[0])==index_doc:
            temp2.append(( int(temp1[0]) ,int(temp1[1])))
        else:
            recovered_answers.append(temp2)
            temp2 = []
            index_doc = int(temp1[0])
            temp2.append(( int(temp1[0]) ,int(temp1[1])))
        
    return recovered_answers

def classification( recovered_list, total_of_documents,recovered_answers):
    """
    Calculate the number of documents in each classification
    recovered_list : list of tuples with query number, relevants recovered documents number and their ranks for each query
    recovered_answers : list of list of tuples of query number and document number recovered in the DB for each query

    """
    metrics_list = []
    for element in recovered_answers:
        RR = 0
        RI = 0
        NR = 0
        for item in element:
            query = recovered_list[item[0]-1]
            document_index = item[1]
            if len(query) !=0:
                for i in range(len(query)):
                    if query[i][1] == document_index:
                        RR += 1
                        break
                NR += 1
            else:
                NR = len(element)- RR
                break

     
        RI = len(recovered_list[item[0]-1]) - RR
        NI = total_of_documents - RR - RI - NR
        metrics_list.append((RR, RI, NR, NI))


    
    return metrics_list


def precision(RR, RI):   
    try:
        return RR/(RR+RI)
    except:
        return 0    

def r_precision(recovered_list, recovered_answers, n): 
    count = 0
    i = 0
    try:
        for item in recovered_list :
            if i == n: break
            temp = (item[0],item[1])
            if  item[3] and temp in recovered_answers: 
                count += 1
            i += 1
        return count/n
    except:
        return 0

def recall(RR, NR):   
    try:
        return RR/(RR + NR)
    except:
        return 0

def fallout(NI, RI):   
    try:
        return RI/(RI + NI)
    except:
        return 0

def r_fallout(recovered_list, n, RI, NI,recovered_answers): 
    count = 0
    i = 0
    for item in recovered_list :
        if i == n : break
        temp = (item[0],item[1])
        if item[3] and temp not in recovered_answers: 
            count += 1
        i += 1
    return count/ (RI + NI)


def f_measure(precision, recall, beta=1):
    try:
        return (1 + beta**2)/(1/precision + (beta**2)/recall)
    except:
        return 0

def f1_measure(precision, recall):
    try:
        return 2/(1/precision + 1/recall)
    except:
        return 0

