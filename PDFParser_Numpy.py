import pdfminer as oPdf
import util.FileManager as fm
import util.Logger as log
import util.Language as ln
import util.Enumerator as enum
import util.ListManager as lmgr
import operator as op
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTCurve
import numpy as np
import math

# ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Unclassified/"
ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Product Manager/"
ResumeFile="Abhijit_Tadke_APM_Paddle_Lift.pdf"
# ResumeFile="Swarnima Bhosale.pdf"
# ResumeFile="Thomas-Sears.pdf"
# ResumeFile="Vignesh TM APM (1).pdf"
# ResumeFile="Nihal_Satam.pdf"
# ResumeFile="Aditya_Mishra.pdf"
# ResumeFile="Smit_Vora.pdf"
# SubjectResume = fm.ReadFile(ResumePath,ResumeFile)

oLog=log.Logger("D:/Users/Sankalp/Documents/Work/MyLearning/Python/PDF_Parser/DebugLog/Debug.log",0)
oLog.setLevel=5

# lstArray=np.array()
lstStyles=[]
lstDocStyle=[]

def FindHeaders(Resume):
    lstHeaderStyles=[]
    Section=""
    TotalPages=0
    for page_layout in extract_pages(Resume):
        TotalPages=TotalPages+1
    
    DocLength=TotalPages

    for page_layout in extract_pages(Resume):
        PageHeight=page_layout.y1
        TotalPages=TotalPages-1
        Offset=TotalPages*PageHeight
        oLog.SetLogObj("",10,str(page_layout))
        for element in page_layout:
            # print("element = "+ str(element))
            oLog.SetLogObj("Element:",10,str(element))
            if isinstance(element, LTTextContainer):
                # print("element.get_text = "+ str(element.get_text()))
                oLog.SetLogObj("Element:",10,str(element.get_text()))
                for text_line in element:
                    Section="-"
                    strText=ln.CleanText(element.get_text()).lower().strip()
                    # print("strText : " + strText)
                    if strText!="":
                        if strText in enum.lstSectionHeaders:
                            Section="IMP"
                        for character in text_line:
                            if isinstance(character, LTChar):
                                lstFind=[]
                                lstFind=[x for x in lstHeaderStyles if x[0]==character.fontname and x[1]==character.size]
                                
                                if len(lstFind)>0:
                                    lstHeaderStyles.remove(lstFind[0])
                                    lstFind[0][2]=int(lstFind[0][2])+1
                                    if Section=="IMP":
                                        lstFind[0][3]=Section
                                    lstHeaderStyles.append(lstFind[0])
                                else:
                                    lstHeaderStyles.append([character.fontname,character.size,1,Section])
        # oLog.SetLogObj("",1,lmgr.Convert2DListToCSV(lstHeaderStyles))
    lstHeaderStyles=lmgr.SortList(lstHeaderStyles,1,True)
    i=1
    for eachRow in lstHeaderStyles:
        eachRow.append(str(i))
        i=i+1

    oLog.SetLogObj("",1,lmgr.Convert2DListToCSV(lstHeaderStyles))
    return lstHeaderStyles

def renderResume(lstLayout):
    ResumeText=""
    for eachSection in lstDocStyle:
        oLog.SetLogObj("Final Rendition Section:",1,str(eachSection[0]))
        lstNodes=eachSection[5]
        lstNodes=sorted(lstNodes, key=lambda x: (x[1],-x[0]),reverse=True)
        for eachNode in lstNodes:
            # oLog.SetLogObj("Final RawNode:",1,str(eachNode))
            oLog.SetLogObj("",1,str(eachNode[6]))
            if eachNode[8]=="IMP":
                SectionName=""
                if str(eachNode[6]).lower().strip() in enum.lstSectionExp:
                    SectionName="EXP"
                elif str(eachNode[6]).lower().strip() in enum.lstSectionEdu:
                    SectionName="EDU"
                elif str(eachNode[6]).lower().strip() in enum.lstSectionSkills:
                    SectionName="SKL"

                ResumeText = ResumeText + "HEADER:" + SectionName + ": " + str(eachNode[6]) + "\n"
                # print(eachNode[8])
            else:
                ResumeText = ResumeText + str(eachNode[6]) + "\n"
    fm.SaveNewFile(ResumePath,ResumeText,ResumeFile.replace(".pdf",".txt"))

def ExtractEntities(ResumePath,ResumeFile):
    txtResume=fm.ReadFile(ResumePath,ResumeFile)
    lstResume=txtResume.split("\n")
    lstWorkEx=[]
    lstEdu=[]
    iSeqWorkEx=0
    WorkExStart=False
    EduStart=False
    WorkExText=""
    EduText=""
    for eachLine in lstResume:
        if eachLine.startswith("HEADER:"):
            if eachLine.startswith("HEADER:EXP:"):
                WorkExStart=True
                EduStart=False
            elif eachLine.startswith("HEADER:EDU:"):
                EduStart=True
                WorkExStart=False
            else:
                WorkExStart=False
                EduStart=False

        if WorkExStart:
            iSeqWorkEx=iSeqWorkEx+1
            WorkExText=eachLine.lower().strip()
            lstWorkExItem=[iSeqWorkEx,WorkExText]
            lstWorkEx.append(lstWorkExItem)
        if EduStart:
            iSeqEdu=iSeqWorkEx+1
            EduText=eachLine.lower().strip()
            lstEduItem=[iSeqEdu,EduText]
            lstEdu.append(lstEduItem)
    print("EXPERIENCE: " + str(lstWorkEx))
    print("EDUCATION: " + str(lstEdu))
    oLog.SetLogObj("EXPERIENCE: ",1,str(lstWorkEx))
    oLog.SetLogObj("EDUCATION: ",1,str(lstEdu))


def CleanEmptyNodes(lstLayout):
    lstLayoutWorkingCopy=lstLayout
    for eachSection in lstLayoutWorkingCopy.copy():
        # print(eachSection)
        lstNodes=eachSection[5]
        if len(lstNodes)==0:
            lstLayout.remove(eachSection)
    return lstLayout

def TransferChildNode(lstLayout,TextNode,FromSeq,ToSeq):
    FromNodeList=[x for x in lstLayout if x[0]==FromSeq]
    ToNodeList=[x for x in lstLayout if x[0]==ToSeq]
    NodeList=[]
    
    oLog.SetLogObj("lstLayout",6,str(lstLayout))
    oLog.SetLogObj("FromNodeList",6,str(FromNodeList))
    oLog.SetLogObj("ToNodeList",6,str(ToNodeList))

    if len(FromNodeList)==1 and len(ToNodeList)==1:
        NodeList=FromNodeList[0][5]
        NodeList.remove(TextNode)

        lstLayout.remove(FromNodeList[0])
        FromNodeList[0][5]=NodeList

        lstLayout.append(FromNodeList[0])
        oLog.SetLogObj("After From FromNodeList",6,str(FromNodeList))
        oLog.SetLogObj("After From lstLayout",6,str(lstLayout))

        # Remove entity from old list
        NodeList=ToNodeList[0][5]
        oLog.SetLogObj("ToNodeList: ",6,str(ToNodeList[0][5]))
        oLog.SetLogObj("To NodeList:",6,str(NodeList))
        oLog.SetLogObj("TextNode: ",7,str(TextNode))
        oLog.SetLogObj("ToNodeList: ",7,str(ToNodeList[0][1]) + str(ToNodeList[0][2]) + str(ToNodeList[0][3]) + str(ToNodeList[0][4]))
        lstLayout.remove(ToNodeList[0])
        NodeList.append(TextNode)
        oLog.SetLogObj("Post Removal of TextNode NodeList:",6,str(NodeList))

        ToNodeList[0][5]=NodeList
        lstLayout.append(ToNodeList[0])
        oLog.SetLogObj("After To lstLayout",6,str(lstLayout))

    return lstLayout


def CreateTextNodes(element,iSeq,Offset):
    HLeft=element.x0
    VBottom=element.y0 + Offset
    HRight=element.x1
    VTop=element.y1 + Offset
    
    lstTextNodes=[]
    for text_line in element:
        prevFont=""
        prevSize=""
        fullString=""
        if text_line!="":
            try:
                for character in text_line:
                    if isinstance(character, LTChar):
                        if prevFont==character.fontname and prevSize==character.size:
                            fullString=fullString + character.get_text()
                        else:
                            if fullString!="":
                                HeaderType=[x for x in lstStyles if x[1]==prevSize and x[0]==prevFont]
                                # print(HeaderType[0][4])
                                lstTextNode=[HLeft,VBottom,HRight,VTop,prevFont,prevSize,fullString,HeaderType[0][4],HeaderType[0][3],iSeq]
                                lstTextNodes.append(lstTextNode)
                            prevFont=character.fontname
                            prevSize=character.size
                            fullString=character.get_text()
            except Exception as e:
                print("CreateTextNodes: Error Suppressed:" + str(e))
        if fullString!="":
            # print("fullString="+fullString)
            # print("Size="+str(prevSize)+" Font="+str(prevFont))
            HeaderType=[x for x in lstStyles if x[1]==prevSize and x[0]==prevFont]
            if len(HeaderType)==0:
                HeaderType=[x for x in lstStyles if x[1]==math.ceil(prevSize) and x[0]==prevFont]
                if len(HeaderType)==0:
                    HeaderType=[x for x in lstStyles if x[1]==math.floor(prevSize) and x[0]==prevFont]
            # print("New: "+str(HeaderType))
            if len(HeaderType)>0:
                lstTextNode=[HLeft,VBottom,HRight,VTop,prevFont,prevSize,fullString,HeaderType[0][4],HeaderType[0][3],iSeq]
                lstTextNodes.append(lstTextNode)

    return lstTextNodes

def SetElementInSection(element,lstLayout,Offset):
    HLeft=element.x0
    VBottom=element.y0 + Offset
    HRight=element.x1
    VTop=element.y1 + Offset
    lMargin=HLeft-10
    RMargin=HLeft+10
    
    lstSection=[x for x in lstLayout if x[1]>=lMargin and x[1]<=RMargin]

    if len(lstSection)>0:
        lstLayout.remove(lstSection[0])

        if HLeft<lstSection[0][1]:
            lstSection[0][1]=HLeft
        if VBottom<lstSection[0][2]:
            lstSection[0][2]=VBottom
        if HRight>lstSection[0][3]:
            lstSection[0][3]=HRight
        if VTop>lstSection[0][4]:
            lstSection[0][4]=VTop
        # if lstSection[0][1]<HLeft:
        #     HLeft=lstSection[0][1]
        # if lstSection[0][2]<VBottom:
        #     VBottom=lstSection[0][2]
        # if lstSection[0][3]>HRight:
        #     HRight=lstSection[0][3]
        # if lstSection[0][4]>VTop:
        #     VTop=lstSection[0][4]

        lstTextNodes=CreateTextNodes(element,lstSection[0][0],Offset)
        if len(lstTextNodes)>0:
            lstCurrenttextNodes=lstSection[0][5]
            for eachText in lstTextNodes:
                lstCurrenttextNodes.append(eachText)
            lstSection[0][5]=lstCurrenttextNodes

        lstLayout.append(lstSection[0])
    else:
        seq=len(lstLayout)
        lstTextNodes=CreateTextNodes(element,seq+1,Offset)
        lstSection=[seq+1,HLeft,VBottom,HRight,VTop,lstTextNodes]
        lstLayout.append(lstSection)

    return lstLayout

def GetSectionLayout(Resume):
    SectionSeq=0
    lstLayout=[]
    TotalPages=0
    for page_layout in extract_pages(ResumePath+ResumeFile):
        TotalPages=TotalPages+1
    
    DocLength=TotalPages

    for page_layout in extract_pages(ResumePath+ResumeFile):
        TotalPages=TotalPages-1
        Offset=TotalPages*page_layout.y1
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # oLog.SetLogObj("",1,element)
                lstLayout=SetElementInSection(element,lstLayout,Offset)
    
    lstLayout=lmgr.SortList(lstLayout,0,False)
    for eachRow in lstLayout:
        oLog.SetLogObj("Section:",1,str(eachRow[0]) + " " + str(eachRow[1]) + " " + str(eachRow[2]) + " " + str(eachRow[3]) + " " + str(eachRow[4]))
        # oLog.SetLogObj("Section",1,eachRow[0])
        for eachOne in eachRow[5]:
            oLog.SetLogObj("",1,eachOne[6] + " " + str(eachOne[0]) + " " + str(eachOne[1]) + " " + str(eachOne[2]) + " " + str(eachOne[3]) + " " + str(eachOne[4]) + " " + str(eachOne[5]) + " " + str(eachOne[7]) + " " + str(eachOne[8]))
    # oLog.SetLogObj("",1,lmgr.Convert2DListToCSV(lstLayout))
    return lstLayout

def GetHeaderlessSections(lstLayout):
    BigHeads=[x for x in lstStyles if x[4]=="1"]
    BigHeader=BigHeads[0][1]
    IMPHeaders=[x for x in lstStyles if x[3]=="IMP"]
    lstHeaderless=[]
    for eachSection in lstLayout:
        hasHead=False
        for eachNode in eachSection[5]:
            oLog.SetLogObj("eachNode:",9,eachNode)
            if eachNode[8]=="IMP":
                hasHead=True
                oLog.SetLogObj("eachNode[8]:",9,eachNode)
        # print("hasHead="+str(hasHead))
        if not hasHead:
            lstHeaderless.append(eachSection[0])
            oLog.SetLogObj("eachSection[0]:",9,eachSection[0])
    return lstHeaderless

def FindOrphanedNodes(lstLayout):
    pass

def RefineSectionLayout(lstLayout):
    # print(lstLayout)
    lstHeaderless=[]
    lstHeaderless=GetHeaderlessSections(lstLayout)
    lstTransferNodes=[]
    BigHeads=[x for x in lstStyles if x[4]=="1"]
    # print(BigHeads[0][1])
    BigHeader=BigHeads[0][1]
    IMPHeaders=[x for x in lstStyles if x[3]=="IMP"]
    IMPHead=[]
    for eachHead in IMPHeaders:
        # print("IMPHeaders: " + str(IMPHeaders))
        IMPHead.append(str(eachHead[1]) + ":" + str(eachHead[0]))

    for eachSection in lstLayout:
        hasHead=False
        for eachNode in eachSection[5]:
            # print(eachNode[5])
            # print(eachNode[4])
            if eachNode[8]=="IMP":
                hasHead=True
        if not hasHead:
            for eachNode in eachSection[5]:
                oLog.SetLogObj("KEY:",1, str(eachNode[0]) + " " + str(eachNode[1]) + " " + str(eachNode[6]) + " " + str(eachNode[9]))
                EligibleSections=[x for x in lstLayout if x[1]<=eachNode[0] and x[3]>=eachNode[0] and x[2]<=eachNode[1] and x[4]>=eachNode[1] and x[0]!=eachNode[9] and x[0] not in lstHeaderless]
                oLog.SetLogObj("EligibleSections: ",1,str(EligibleSections))
                if len(EligibleSections)==1:
                    # print(EligibleSections[0][0])
                    lstTransferChildMap=[eachNode,eachNode[9],EligibleSections[0][0]]
                    lstTransferNodes.append(lstTransferChildMap)
                elif len(EligibleSections)>1:
                    # print("Almost " + str(len(EligibleSections)) + " eligible sections for " + str(eachNode))
                    oLog.SetLogObj("More than 1>",1,str(EligibleSections))

    oLog.SetLogObj("lstTransferNodes",6,str(lstTransferNodes))
    for eachChildNode in lstTransferNodes:
        lstLayout=TransferChildNode(lstLayout,eachChildNode[0],eachChildNode[1],eachChildNode[2])
    
    lstLayout=lmgr.SortList(lstLayout,0,False)
    return lstLayout
    # oLog.SetLogObj("Body:" + str(lstLayout))
                    
                # EligibleSections.remove()

def ContainsDate(lstWords):
    i=0
    Result=False
    lstWords=ln.CleanText(lstWords).strip().lower()
    lstWords=lstWords.split(" ")

    for eachWord in lstWords:
        eachWord1=ln.CleanText(eachWord.strip().lower())

        if eachWord1 in enum.lstMonthNames:
            Result=True
            break
        if eachWord1.isnumeric():
            if len(eachWord1)==4:
                Result=True
                break
            if len(eachWord1)==2:
                if i>1:
                    if lstWords[i-1].isnumeric() and (len(lstWords[i-1])==4 or len(lstWords[i-1])==2):
                        Result=True
                        break
                if i<len(lstWords)-1:
                    eachWord2=ln.CleanText(lstWords[i+1]).strip().lower()
                    if eachWord2.isnumeric() and (len(eachWord2)==4 or len(eachWord2)==2):
                        Result=True
                        break

        i=i+1
    return Result

def ContainsCompany(lstWords):
    i=0
    Result=False
    lstWords=lstWords.split(" ")
    
    for eachWord in lstWords:
        eachWord1=eachWord.strip().lower()
        if eachWord1 in enum.lstCompanyName:
            Result=True
            break

    for eachWord in lstWords:
        eachWord1=ln.CleanText(eachWord).strip().lower()
        if eachWord1 in enum.lstCompanyName:
            Result=True
            break
    return Result

def ContainsUniversity(lstWords):
    i=0
    Result=False
    lstWords=lstWords.split(" ")
    for eachWord in lstWords:
        eachWord1=eachWord.strip().lower()
        if eachWord1 in enum.lstEducationalEntities:
            Result=True
            break

    for eachWord in lstWords:
        eachWord1=ln.CleanText(eachWord).strip().lower()
        if eachWord1 in enum.lstEducationalEntities:
            Result=True
            break
    return Result

def ContainsDegree(lstWords):
    i=0
    Result=False
    lstWords=lstWords.split(" ")
    for eachWord in lstWords:
        eachWord1=eachWord.strip().lower()
        if eachWord1 in enum.lstDegrees:
            Result=True
            break
    for eachWord in lstWords:
        eachWord1=ln.CleanText(eachWord).strip().lower()
        if eachWord1 in enum.lstDegrees:
            Result=True
            break
    return Result

def ContainsDesignation(lstWords):
    i=0
    Result=False
    lstWords=lstWords.split(" ")
    for eachWord in lstWords:
        eachWord1=eachWord.strip().lower()
        if eachWord1 in enum.lstDesignation:
            if i<len(lstWords)-1:
                eachWord2=ln.CleanText(lstWords[i+1]).strip().lower()
                if eachWord2 in enum.lstDesignation:
                    Result=True
                    break
        i=i+1
    return Result


def ExtractNamedEntities(ResumePath,ResumeFile):
    Resume=fm.ReadFile(ResumePath,ResumeFile)
    lstResumeBase=[]
    i=1
    lstResume=Resume.split("\n")
    for eachSentence in lstResume:
        HasName=False
        HasCompany=False
        HasDesignation=False
        HasDate=False
        HasUniversity=False
        HasDegree=False
        if ContainsDate(eachSentence):
            HasDate=True
        if ContainsCompany(eachSentence):
            HasCompany=True
        if ContainsUniversity(eachSentence):
            HasUniversity=True
        if ContainsDegree(eachSentence):
            HasDegree=True
        if ContainsDesignation(eachSentence):
            HasDesignation=True
    
        lstSentence=[i,eachSentence,HasName,HasCompany,HasDesignation,HasDate,HasUniversity,HasDegree]

        lstResumeBase.append(lstSentence)
        i=i+1
    # print(lstResumeBase)
    oLog.SetLogObj("NER",15,lmgr.Convert2DListToCSV(lstResumeBase))

Resume=ResumePath+ResumeFile
lstStyles=FindHeaders(Resume)
lstDocStyle=GetSectionLayout(Resume)
oLog.SetLogObj("Primitive Body:",1,str(lstDocStyle))

GetHeaderlessSections(lstDocStyle)

lstDocStyle=RefineSectionLayout(lstDocStyle)
oLog.SetLogObj("Unclean Body:",1,str(lstDocStyle))

lstDocStyle=CleanEmptyNodes(lstDocStyle)
oLog.SetLogObj("Body:",1,str(lstDocStyle))

lstDocStyle=RefineSectionLayout(lstDocStyle)
oLog.SetLogObj("Unclean Body:",1,str(lstDocStyle))

lstDocStyle=CleanEmptyNodes(lstDocStyle)
oLog.SetLogObj("Body:",1,str(lstDocStyle))

for eachSection in lstDocStyle:
    oLog.SetLogObj("Section:",1,str(eachSection[0]))
    for eachNode in eachSection[5]:
        oLog.SetLogObj("RawNode:",1,str(eachNode))
        oLog.SetLogObj("Node:",1,str(eachNode[6]))

renderResume(lstDocStyle)

ExtractEntities(ResumePath,ResumeFile.replace(".pdf",".txt"))

ExtractNamedEntities(ResumePath,ResumeFile.replace(".pdf",".txt"))