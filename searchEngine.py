import math
import numpy as np
from evaluationSystem import  precision, r_precision, recall, f_measure, f1_measure, fallout, r_fallout, classification, read_collection_answers
from collections_parser import read_collection, read_query, File
from elbowMethod import elbow_method
from sklearn.cluster import KMeans



def similarity_cos(vector_query,vector_document):
    """"
    Calculate the similarity of two documents or a document and a query with the cosene form
    vector_query: dictionary wich represent the  weight vector  of a query
    vector_document: dictionary wich represent the weight vector of a document

    """
    v_q= np.asarray(list(vector_query.values()))
    v_d= np.asarray(list(vector_document.values()))
    numerator = 0
    if (np.linalg.norm(v_q)==0 or np.linalg.norm(v_d)==0):
        return 0
    else:
        for term in vector_query:
            if vector_document.get(term) :
                numerator += vector_query[term] * vector_document[term] 

        result = numerator/(np.linalg.norm(v_q)*np.linalg.norm(v_d))
        return result


def relevance_func(value):
    """
    Calculate a relevance value or rank dependig on the similiraty

    """
    relevance = 0
    if value >= 0.5:
        relevance = 1
    elif value > 0.2 and value < 0.4:
        relevance = 2
    elif value > 0.1 and value <= 0.2:
        relevance = 3
    elif value >= 0.050 and value <= 0.1:
        relevance = 4
    else:
        relevance = 5
    return relevance


def tf(data, max_frequency):
    """ 
    Calculate the normalice frequency of each term in a document or query
    data : dictionary with each term and the frequency which appear in one document
    max_frequency : value of the term most frequent in the docuemnt

    """
    tf : dict[str:int] = {}
    for term in data:
        tf[term] = float(data[term] /max_frequency)
    return tf


def matrix_tf(documents_list  ):
    """
    Fill the normalice frequency of every document
    documents_list : list of Files

    """
    for doc in documents_list:
        row =  tf(doc.frequency, doc.maxFrequency)
        doc.normalizeFrequency = row.copy()
    return 


def idf(documents_term, total_of_documents):
    """
    Calculate the inverse document frequency of each term in the vocabulary
    documents_term (ni): dictionary with each term and the number of documents that contain it
    total_of_documents(N) : total of document in the DB 

    """
    idf : dict[str:int]= {}
    for term in documents_term:
        idf[term] =float(math.log10(total_of_documents/documents_term[term]))

    return idf


def weight( idf, lambda_func,documents_list, is_document):
    """
    Calculate the weight of each term in the document or query using the formula for Vectorial Model
    idf : dictionary with the inverse document frequency for each term
    lambda_fun : auxiliar function for calculate weights depending on it's a query or a document 
    documents_list : list of Files

    """
    for i in range(len(documents_list) ):
        temp = {}
        list = []
        tf = documents_list[i].normalizeFrequency

        for term in tf :
            if idf.get(term) != None :
                temp[term] = lambda_func(tf[term], idf[term])
        
        documents_list[i].weight = temp.copy()
        list.append(temp)

        

def query_weight(documents_term,total_of_documents, query_list, alpha=0.5):
    """
    Fill the vector weight of a query
    documents_term (ni): dictionary with each term and the number of documents that contain it
    total_of_documents(N) : total of document in the DB 
    query_list: list of Files
    alpha: smoothing term. By default 0.5

    """
    alpha=0.5
    matrix_tf(query_list)
    vector_idf = idf(documents_term, total_of_documents)
    return weight( vector_idf, lambda x, y: (alpha + (1 - alpha) * x) * y, query_list, False)


def document_weight(documents_term, total_of_documents, documents_list):
    """
    Fill the vector weight of a document
    documents_term (ni): dictionary with each term and the number of documents that contain it
    total_of_documents(N) : total of document in the DB 
    documents_list : list of Files
    """
    matrix_tf(documents_list)
    vector_idf = idf(documents_term, total_of_documents)
    return weight(vector_idf,lambda x, y: x * y, documents_list, True)  


def rank (query_list, documents_list):
    """
    Makes a list of tuples with the query number, document number, rank and a boolean value that indicates whether the document is relevant or not for each query
    query_list: list of File
    document_list : list of File

    """
    result_rank : list[list[tuple[int,int,int,bool]]]= []
    for query in query_list:
        temp: list[tuple[int,int,int,bool]] = []
        for doc in documents_list:
            rank = relevance_func(similarity_cos(query.weight, doc.weight))
            temp.append((query.indexNumber, doc.indexNumber, rank, True  if rank < 5 else False))
            
        temp.sort( key = lambda x : x[2])
        result_rank.append(temp) 
    return result_rank  


def k_means(weights, n=5):
    w = np.asarray(weights).reshape(-1,1)
    k_means =KMeans(n_clusters = n).fit(weights)
    return k_means.labels_


def query_expansion(recovered_list, documents_list):
    """
    Choose an initial centroid for use kMeans algorithm
    one_relevant : list with one relevant document for each query
    groups : list with the classification groups for each document
    weights :list with weights of each document
    closer :list with the documents(File) belonging to the same group of the most relevant document 
    """
    one_relevant : list[tuple[int,dict[str,int],int]] = []  #list with one relevant document for each query
    groups = []                                             #numpy object
    weights = []
    closer :list[File]= []

    for i in range(len(recovered_list)):
        if len(recovered_list[i]) !=0:
            one_relevant.append(recovered_list[i][0])
            documents_list.insert(0,recovered_list[i][0])
        else:
            one_relevant.append(None) 
    
   
    for i in range(len(documents_list)):
        if i >300:break
        all_w = np.array(list(documents_list[i].weight.values()))
        w = all_w [ :10]
        weights.append(w)
        i += 1

    groups = k_means(weights,7)
    #elbow_method(weights,50,100)  
    
    for i in range(len(one_relevant)):
        temp =[]
        if one_relevant[i] !=None:
                index_of_document = one_relevant[i]
                number_of_group =  groups[i]
                for j in range(int(np.size(groups))):
                    n = int(np.size(groups))
                    if groups[j] == number_of_group:
                        temp.append(documents_list[j])
        else:
            temp.append([])

        closer.append(temp)

    return closer

def query_expansion_with_feedback(documents_list, c1):
    """ 
    Used kMeans algorithm whit a relevant document choose for the user like initial centroid 
    c1: relevant document choose by the user
    
    """
    recovered_list = [[c1]]
    return query_expansion(recovered_list, documents_list) 

def main(url_documents, url_query, url_answers, alpha=None, query=None, n=10):
    """
    documents_term (ni): dictionary with each term and the number of documents that contain it
    total_of_documents(N) : total of document in the DB 
    documents_list : list of Files
    query_list : list of Files
    
    """
    documents_term, documents_list = read_collection(url_documents)
    total_of_documents = len(documents_list)

    document_weight(documents_term, total_of_documents ,documents_list)
    query_list = []
    if query != None:
        query_list = read_query(query)
    else:
        query_list = read_collection(url_query)[1] 
    
    query_weight(documents_term, total_of_documents, query_list, alpha)

    rank_list :list[list[tuple[int,int,int,bool]]]= rank (query_list, documents_list)  
    query_rr_rank : list[list[tuple[int,int,int]]] = []  # list with query number, relevants recovered documents number and their ranks for each query
    recovered_relevants :list[list[File]] = []  #list with the relevants recovered documents for each query
    recovered_relevants :list[list[File]] = []  #list with the documents(File) belonging to the same group of the most relevant document 
    for q in rank_list:
        temp1 = []
        temp2 = []
        for element in q:
                if element[3]:
                    # print(str(element[0]) + ' ' + str(element[1]) + ' ' + str(element[2]))
                    temp1.append((element[0],element[1],element[2]))  #Esto me sirve por si tengo q imprimir
                    temp2.append(documents_list[element[1]-1])
        query_rr_rank.append(temp1)
        recovered_relevants.append(temp2)

    closer = query_expansion_with_feedback(documents_list, documents_list[0])
    #query_expansion(recovered_relevants,documents_list) 

    #Metrics
    if query ==None:  
        recovered_answers = read_collection_answers(url_answers) # list of tupes query number and document number recovered in the DB
        c = classification( query_rr_rank, total_of_documents, recovered_answers)
        metrics =[]
        media = [0,0,0,0,0,0,0]
        for i in range(len(c)):
                RR, RI, NR, NI = c[i]
                p = precision(RR, RI)
                r_p = r_precision(rank_list[i], recovered_answers[i],n)
                r =  recall(RR, NR)
                f = fallout(NI, RI)
                r_f = r_fallout(rank_list[i], n, RI, NI,recovered_answers[i])
                fm = f_measure(p, r, beta=1)
                f1_m = f1_measure(p, r)
                if i <=50:
                    media[0] += p
                    media[1] += r
                    media[2] += f
                    media[3] += fm
                    media[4] += f1_m
                    media[5] += r_p
                    media[6] += r_f
                metrics.append((round(p,4),round(r,4),round(f,4),round(fm,4),round(f1_m,4), round(r_p,4), round(r_f,4)))

        print(f"{url_documents}\n Precision:{media[0]/50}\n Recall:{media[1]/50}\n Fallout:{media[2]/50}\n F Measure:{media[3]/50}\n F1 Measure:{media[4]/50}\n R_precision:{media[5]/50}\n R_Fallout::{media[6]/50}\n ")
        i=1
        print(f"        P        R        F       FM       F1   RP    RF")
        for q in metrics:
            print(f"query{i}  {q[0]}  {q[1]}   {q[2]}   {q[3]}   {q[4]}   {q[5]}   {q[6]}")
            i+=1
        return recovered_relevants, metrics

       
    for q in recovered_relevants:
        for doc in q:
            print(doc)
        
    return rank_list, documents_list, documents_term, recovered_relevants

if __name__ == '__main__':
    query = "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."
    main('./collections/CISI.ALL','./collections/CISI.QRY','./collections/CISI.REL', None, None)
