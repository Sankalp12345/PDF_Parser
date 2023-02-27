import operator as op

def SortList(lstInput,SortKey,SortReverse):
    lstInput=sorted(lstInput,key=lambda l:l[SortKey],reverse=SortReverse)
    return lstInput

# def ConvertDictToList(dictInput):

def loadCSVtoDict(strInput,iKey,iValue):
    dictCSV={}
    lstLines=strInput.split("\n")
    for eachLine in lstLines:
        words=eachLine.split(",")
        # print("words: " + str(words))
        dictCSV[words[iKey]]=words[iValue]
    return dictCSV

def ConvertCSVToList(strInput):
    lstTargetFile=[]
    lstSentences=strInput.split("\n")
    for eachSentence in lstSentences:
        lstWords=eachSentence.split(",")
        lstTargetFile.append(lstWords)
    return lstTargetFile

def ConvertDictToCSV(dictInput):
    CSVString=""
    for eachKey in dictInput:
        CSVString=CSVString + str(eachKey) + "," + str(dictInput[eachKey]) + "\n"
    return CSVString

def Convert2DListToCSV(lstInput):
    CSVString=""
    for eachRow in lstInput:
        CSVRow=""
        for eachColumn in eachRow:
            if CSVRow=="":
                CSVRow=str(eachColumn)
            else:
                CSVRow=CSVRow + "," + str(eachColumn)
        
        if CSVString=="":
            CSVString=str(CSVRow)
        else:
            CSVString=CSVString + "\n" + str(CSVRow)
    return CSVString