import util.FileManager as fm
# import FileManager as fm
import nltk as nl
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import spacy
import re
import util.Enumerator as enum
# import Enumerator as enum
import datetime

nlp = spacy.load("en_core_web_sm")
StopWords=nlp.Defaults.stop_words

# RedundantWords=set(stopwords.words('english'))


def TokenizeToSentences(SrcConent):
    lstSentences=sent_tokenize(SrcConent)
    return lstSentences

def TokenizeToWords(SrcLine):
    lstWords=word_tokenize(SrcLine)
    return lstWords

def GetPoSTags(lstTokenizedWords):
    lstTaggedWords=nl.pos_tag(lstTokenizedWords)
    return lstTaggedWords

def GetNamedEntities_old(Library,strContent):
    lstNamedEntities=nlp(strContent)
    lstNE=[]
    for Named in lstNamedEntities.ents:
        lstEntity=[Named.text,Named.label_]
        lstNE.append(lstEntity)
    return lstNE

def GetNamedEntities(strContent):
    lstNamedEntities=nlp(strContent)
    lstNE=[]
    for Named in lstNamedEntities.ents:
        lstEntity=[Named.text,Named.label_]
        lstNE.append(lstEntity)
    return lstNE

def GetFlattenedString(strOriginal):
    strOriginal=re.sub(r'[^a-zA-Z0-9_.\', ]', ' ', strOriginal)
    strOriginal=strOriginal.lower().strip()
    return strOriginal

def IsNoun(strMatchSentence):
    strMatchSentence=re.sub(r'[^a-zA-Z0-9]', ' ', strMatchSentence)
    lstMatchWords=TokenizeToWords(strMatchSentence)
    lstMatchTaggedWords=GetPoSTags(lstMatchWords)
    SentenceLength=len(lstMatchTaggedWords)
    NounList=[idx for idx,val in enumerate(lstMatchTaggedWords) if val[1]=='NNP' or val[1]=='NN' or val[1]=='NNS' or val[1]=='NNPS']
    NounCount=len(NounList)
    Result=False
    if(SentenceLength==NounCount):
        Result=True
    else:
        Result=False
    return Result

def GetEntityType(lstNamedEntities):
    if len(lstNamedEntities)>0:
        return str(lstNamedEntities[0][1])
    else:
        return "NULL"

def GetEducationEntity(strMatchSentence):
    EntityType="NA"
    for a in enum.lstEducationalEntities:
        if strMatchSentence.find(a)>=0:
            EntityType="Institute"
            break
    for a in enum.lstDegrees:
        if strMatchSentence.find(a)>=0:
            EntityType="Degree"
            break
    return EntityType

def IsValidYear(iYear):
    OldestYear=0
    CurrentYear=int(datetime.datetime.now().year)
    OldestYear=int(CurrentYear)-100
    if int(iYear)>int(OldestYear) and int(iYear)<=int(CurrentYear):
        return True
    else:
        return False

def GetDate(strMatchSentence):
    lstDates=strMatchSentence.split(" ")
    Month1=""
    Month2=""
    MonthNum1=0
    MonthNum2=0
    Year1=1900
    Year2=1900
    dictTenure={}
    BaseDate=datetime.datetime(1900,1,1)
    startYear=BaseDate
    EndYear=BaseDate
    if strMatchSentence=='2017':
        print(strMatchSentence)
    for datepart in lstDates:
        if datepart.isnumeric():
            if IsValidYear(datepart):
                if Year1==1900:
                    Year1=int(datepart)
                else:
                    Year2=int(datepart)

        for a in enum.lstMonth:
            if datepart.find(a)>=0:
                # dictMonth1=list(enum.dictMonth)
                if MonthNum1==0:
                    Month1=a
                    MonthNum1=enum.dictMonth.get(a)
                else:
                    Month2=a
                    MonthNum2=enum.dictMonth.get(a)
                break

    if Year1==1900 and Year2==1900:
        result="NotDate"
        startYear=BaseDate
        EndYear=BaseDate
    else:
        if Year1!=1900 and MonthNum1==0:
            MonthNum1=12
        if Year2!=1900 and MonthNum2==0:
            MonthNum2=12
        if Year1==1900:
            MonthNum1=1
        if Year2==1900:
            MonthNum2=1

    # print("Year1 = " + str(Year1) + "-" + str(MonthNum1))
    # print("Year2 = " + str(Year2) + "-" + str(MonthNum2))

    if Year1>1900 and int(MonthNum1)>0:
        startYear=datetime.datetime(int(Year1),int(MonthNum1),1)

    if Year2>1900 and int(MonthNum2)>0:
        EndYear=datetime.datetime(int(Year2),int(MonthNum2),1)
    
    if startYear!=BaseDate:
        dictTenure["StartYear"]=startYear
    if EndYear!=BaseDate:
        dictTenure["EndYear"]=EndYear
        
    return dictTenure
            
def CleanText(strText):
    strText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', strText)  # remove punctuations
    strText = re.sub(r'[^\x00-\x7f]',r' ', strText) # remove non-ascii characters
    strText = re.sub('\s+', ' ', strText)  # remove extra whitespace
    # strText = re.sub(r'[0-9]+', '', strText)  #remove numbers
    return strText.lower()
            
def CleanTextWOSpecialChars(strText):
    # strText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,;<=>?@[\]^_`{|}~"""), ' ', strText)  # remove punctuations
    strText = re.sub(r'[^\x00-\x7f]',r' ', strText) # remove non-ascii characters
    strText = re.sub('\s+', ' ', strText)  # remove extra whitespace
    # strText = re.sub(r'[0-9]+', '', strText)  #remove numbers
    return strText.lower()

def filterStopWords(strText):
    lst=[]
    lstWords=strText.split(" ")
    for word in lstWords:
        if word.lower() not in StopWords:
            lst.append(word)
    strText=" ".join(lst)
    return strText

def HasStopWords(strText):
    Result=False
    lst=[]
    lstWords=strText.split(" ")
    for word in lstWords:
        if word.lower()  in StopWords:
            Result=True
            continue
    return Result

def CrashDoubleSpaces(strText):
    while strText.find("  ")>=0:
        strText=strText.replace("  ", " ")
    return strText

def CapitalizeSkills(strText):
    strText=strText.strip().capitalize()
    return strText

def IsThisDate(strInput):
    Result=False
    Month=0
    Year=0

    if strInput!="":
        if strInput.isnumeric():
            if len(strInput)==4:
                Year=strInput
        elif " " in strInput:
            strInput = re.sub('\s+', ' ', strInput)
            lstInput=strInput.split(" ")
            for eachWord in lstInput:
                if eachWord.isnumeric():
                    if len(eachWord)==2 or len(eachWord)==4:
                        Year=eachWord
                elif eachWord.lower()[0:3] in enum.dictMonth:
                    Month=1
        elif "-" in strInput:
            strInput = re.sub('\s+', ' ', strInput)
            lstInput=strInput.split("-")
            for eachWord in lstInput:
                if eachWord.isnumeric():
                    if len(eachWord)==2 or len(eachWord)==4:
                        Year=eachWord
                elif eachWord.lower()[0:3] in enum.dictMonth:
                    Month=1
        elif "/" in strInput:
            strInput = re.sub('\s+', ' ', strInput)
            lstInput=strInput.split("/")
            for eachWord in lstInput:
                if eachWord.isnumeric():
                    if len(eachWord)==2 or len(eachWord)==4:
                        Year=eachWord
                elif eachWord.lower()[0:3] in enum.dictMonth:
                    Month=1
        elif "\\" in strInput:
            strInput = re.sub('\s+', '\\', strInput)
            lstInput=strInput.split("")
            for eachWord in lstInput:
                if eachWord.isnumeric():
                    if len(eachWord)==2 or len(eachWord)==4:
                        Year=eachWord
                elif eachWord.lower()[0:3] in enum.dictMonth:
                    Month=1
    if Month!=0 and Year!=0:
        Result=True
    
    return Result


def CalcConfidenceScore(lstNE,lnLine,ThresholdPercent):
    print("Line = " + lnLine + " List= " + str(lstNE))
    lnLine=CleanText(lnLine)
    lstLine=lnLine.split(" ")
    totWords=len(lstLine)
    neGPE=0
    neDATE=0
    dictNEs={
        "GPE":0,
        "DATE":0,
        "DESIG":0
    }
    for words in lstNE:
        MatchWordCount=0
        MatchWordCount=len(list(words[0].split(" ")))
        # print(MatchWordCount)
        if words[1] in dictNEs:
            dictNEs[words[1]]=dictNEs[words[1]]+MatchWordCount
        else:
            dictNEs[words[1]]=MatchWordCount
        # if words[1]=="GPE":
        #     dictNEs["GPE"]=dictNEs["GPE"]+MatchWordCount
        # if words[1]=="DATE":
        #     dictNEs["DATE"]=dictNEs["DATE"]+MatchWordCount

    dictScore={}
    oNE=""
    oScore=0
    dictScore=sorted(dictNEs.items(), key=lambda x:x[1],reverse=True)
    # print("dictScore : " + str(dictScore))
    for NE,Score in dictScore:
        oNE=NE
        oScore=Score
        break

    ConfScore=(oScore/int(totWords))*100
    # print("ConfScore=(" + str(oScore) + " / " + str(totWords) + " ) * 100 = " + str(ConfScore) )
    # print(ConfScore)

    if ConfScore>=ThresholdPercent:
        return str(oNE)
    else:
        return "Undecided"

def IsDesignation(strLine):
    if "-" in strLine:
        strLine=strLine[0:int(strLine.find("-"))].strip()
    else:
        strLine=strLine.strip()
    
    # print("Out lnLine 1.6 =" + str(strLine))
    lstRow=[]
    lstTable=[]
    
    dictDesignations={}
    strLine=CleanText(strLine)
    # print("Out lnLine 1.7 =" + str(strLine))
    lstLine=strLine.split(" ")
    for word in lstLine:
        if word in enum.lstDesignation:
            dictDesignations[word]="DESIG"
            lstRow.append(word)
            lstRow.append("DESIG")
            lstTable.append(lstRow)
    return lstTable,strLine

def IsEnum(strLine,lstEnum):
    # if "-" in strLine:
    #     strLine=strLine[0:int(strLine.find("-"))].strip()
    # else:
    strLine=strLine.strip()
    
    lstRow=[]
    lstTable=[]
    
    dictDesignations={}
    strLine=CleanText(strLine)
    lstLine=strLine.split(" ")
    for word in lstLine:
        if word in lstEnum:
            dictDesignations[word]="DESIG"
            lstRow.append(word)
            lstRow.append("EDUINST")
            lstTable.append(lstRow)
    return lstTable,strLine

def GetTenure(lnLine):
    lstTenure=[]
    # print("GetTenure:" + lnLine)
    if " to " in lnLine:
        # print("aat aala ka")
        lstTenure=lnLine.split(" to ")
        # print("lstTenure = " + str(lstTenure))
    else:
        lstTenure.append(lnLine)
    return lstTenure

def ExtractGrams(txtResume,ingrams):
    unigrams = ngrams(txtResume.split(), ingrams)
    return unigrams

def ConvertDictToList(dictInput):
    listConverted=[]
    listRow=[]
    # dictInput=dict(dictInput)
    # print(str(dictInput))
    # for i in dictInput:
    #     print(str(i))
    #     listRow.append(i[0])
    #     listRow.append(i[1])
    #     listConverted.append(listRow)
    # return listConverted