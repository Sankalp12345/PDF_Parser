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

ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Product Manager/"
ResumeFile="Abhijit_Tadke_APM_Paddle_Lift.pdf"
# SubjectResume = fm.ReadFile(ResumePath,ResumeFile)

oLog=log.Logger("D:/Users/Sankalp/Documents/Work/MyLearning/Python/PDF_Parser/DebugLog/Debug.log",0)
oLog.setLevel=5

# lstArray=np.array()
lstStyles=[]
lstDocStyle=[]

def FindHeaders(Resume):
    lstHeaderStyles=[]
    Section=""
    for page_layout in extract_pages(Resume):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    Section="-"
                    strText=ln.CleanText(element.get_text()).lower().strip()
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


def CreateTextNodes(element,iSeq):
    HLeft=element.x0
    VBottom=element.y0
    HRight=element.x1
    VTop=element.y1
    
    lstTextNodes=[]
    for text_line in element:
        prevFont=""
        prevSize=""
        fullString=""
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
        if fullString!="":
            HeaderType=[x for x in lstStyles if x[1]==prevSize and x[0]==prevFont]
            # print("New: "+str(HeaderType[0][4]))
            lstTextNode=[HLeft,VBottom,HRight,VTop,prevFont,prevSize,fullString,HeaderType[0][4],HeaderType[0][3],iSeq]
            lstTextNodes.append(lstTextNode)

    return lstTextNodes

def SetElementInSection(element,lstLayout):
    HLeft=element.x0
    VBottom=element.y0
    HRight=element.x1
    VTop=element.y1
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

        lstTextNodes=CreateTextNodes(element,lstSection[0][0])
        if len(lstTextNodes)>0:
            lstCurrenttextNodes=lstSection[0][5]
            for eachText in lstTextNodes:
                lstCurrenttextNodes.append(eachText)
            lstSection[0][5]=lstCurrenttextNodes

        lstLayout.append(lstSection[0])
    else:
        seq=len(lstLayout)
        lstTextNodes=CreateTextNodes(element,seq+1)
        lstSection=[seq+1,HLeft,VBottom,HRight,VTop,lstTextNodes]
        lstLayout.append(lstSection)

    return lstLayout

def GetSectionLayout(Resume):
    SectionSeq=0
    lstLayout=[]
    for page_layout in extract_pages(ResumePath+ResumeFile):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # oLog.SetLogObj("",1,element)
                lstLayout=SetElementInSection(element,lstLayout)
    
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
        print("hasHead="+str(hasHead))
        if not hasHead:
            lstHeaderless.append(eachSection[0])
            oLog.SetLogObj("eachSection[0]:",9,eachSection[0])
    return lstHeaderless

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
                    print(EligibleSections[0][0])
                    lstTransferChildMap=[eachNode,eachNode[9],EligibleSections[0][0]]
                    lstTransferNodes.append(lstTransferChildMap)
                elif len(EligibleSections)>1:
                    print("Almost " + str(len(EligibleSections)) + " eligible sections for " + str(eachNode))
                    oLog.SetLogObj("More than 1>",1,str(EligibleSections))

    oLog.SetLogObj("lstTransferNodes",6,str(lstTransferNodes))
    for eachChildNode in lstTransferNodes:
        lstLayout=TransferChildNode(lstLayout,eachChildNode[0],eachChildNode[1],eachChildNode[2])
    
    lstLayout=lmgr.SortList(lstLayout,0,False)
    return lstLayout
    # oLog.SetLogObj("Body:" + str(lstLayout))
                    
                # EligibleSections.remove()

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