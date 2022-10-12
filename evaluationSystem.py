from utils import turnLineToWords
import pathlib

def RR_RI_NR(url,recuperados):
    recuperadosList = recuperadosColeccion(url)
    recuperadosRelevantes = 0
    recuperadosIrrelevantes = 0
    for item in recuperados:
        for element in item:
            temp = (element[0],element[1])
            try:
                recuperadosList.remove(temp)
                recuperadosRelevantes += 1
            except:
                recuperadosIrrelevantes += 1
    noRecuperadosRelevantes = len(recuperadosList)
    return recuperadosRelevantes,recuperadosIrrelevantes, noRecuperadosRelevantes

def recuperadosColeccion(url):
    cwd = pathlib.Path(url).absolute()
    url = str(cwd) 
    doc = open(url,"r")
    lines = doc.readlines()
    doc.close()
    recuperadosList = []
    for item in lines:
        temp = turnLineToWords(item)
        temp = list(temp.items())
        recuperadosList.append((int(temp[0][0]),int(temp[1][0])))
    return recuperadosList

        
def Precision(RR,RI):
    return RR/(RR+RI)

def Recobrado(RR,NR):
    return RR/(RR+NR)

def Medida_F(precision,recobrado,beta=1):
    return (1 + beta**2)/(1/precision + (beta**2)/recobrado)

def Medida_F1(precision,recobrado):
    return 2/(1/precision + 1/recobrado)