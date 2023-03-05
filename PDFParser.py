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

ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Product Manager/"
ResumeFile="Abhijit_Tadke_APM_Paddle_Lift.pdf"
# SubjectResume = fm.ReadFile(ResumePath,ResumeFile)

oLog=log.Logger("D:/Users/Sankalp/Documents/Work/MyLearning/Python/PDF_Parser/DebugLog/Debug.log")
oLog.setLevel=0

def ExtractHeaderFonts(ResumePath,ResumeFile):
    # lstHeaderStyles=[["font","size","Recurrence"]]
    lstHeaderStyles=[]
    for page_layout in extract_pages(ResumePath + ResumeFile):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            lstFind=[]
                            lstFind=[x for x in lstHeaderStyles if x[0]==character.fontname and x[1]==character.size]
                            # print(len(lstFind))
                            if len(lstFind)>0:
                                lstHeaderStyles.remove(lstFind[0])
                                # print(lstFind[0][2])
                                lstFind[0][2]=int(lstFind[0][2])+1
                                lstHeaderStyles.append(lstFind[0])
                            else:
                                lstHeaderStyles.append([character.fontname,character.size,1])
        oLog.SetLogObj("",1,lmgr.Convert2DListToCSV(lstHeaderStyles))
        lstHeaderStyles=lmgr.SortList(lstHeaderStyles,1,True)
        i=1
        for eachRow in lstHeaderStyles:
            eachRow.append(str(i))
            i=i+1

        oLog.SetLogObj("",1,lmgr.Convert2DListToCSV(lstHeaderStyles))

def SetElementInSection(lstSectionList,oElement):
    x2=oElement.x1
    x1=oElement.x0
    x1Left=x1-10
    x1Right=x1+10
    lstElemList=[]
    print(x1)
    lstSection=[x for x in lstSectionList if x[0]>=x1Left and x[0]<=x1Right]
    # oLog.SetLogObj("a:",1,lstSection)
    # oLog.SetLogObj("b:",1,lstSectionList)
    # oLog.SetLogObj("c:",1,oElement)
    if len(lstSection)>0:
        # print(lstSection)
        lstSectionList.remove(lstSection[0])
        # oLog.SetLogObj("lstSection:",1,str(lstSection))
        ElemX1=lstSection[0][0]
        ElemX2=lstSection[0][1]
        lstElemList=lstSection[0][2]
        if x1>ElemX1:
            x1=ElemX1
        if x2<ElemX2:
            x2=ElemX2
        lstSection[0][0]=x1
        lstSection[0][1]=x2
        lstElemList.append(oElement)
        lstSection[0][2]=lstElemList
        
        lstSectionList.append(lstSection[0])
    else:
        lstElemList.append(oElement)
        # oLog.SetLogObj("d:",1,lstElemList)
        lstSection=[x1,x2,lstElemList]
        # print("New: " + str(lstSection))
        # oLog.SetLogObj("e:",1,lstSection)
        lstSectionList.append(lstSection)
        print("Naya Section")
    return lstSectionList

def ExtractPositions(ResumePath,ResumeFile):
    Coordinates="Bottom={} Up={} Top={} Down={} TEXT={}"
    lstRectangles=[]
    lstSections=[]
    lstControlTree=[]
    for page_layout in extract_pages(ResumePath+ResumeFile):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                lstControlTree=SetElementInSection(lstControlTree,element)
                # oLog.SetLogObj("Control Tree",1,str(lstControlTree))
                # lstSections
                # oLog.SetLogObj("",1,Coordinates.format(int(element.x0),int(element.y0),int(element.x1),int(element.y1),element.get_text()))
                # Sentence=element.get_text()
                # lstControlTree=[str(Sentence),str(element.x0),str(element.y0),str(element.x1),str(element.y1)]
                # oLog.SetLogObj("",1,str(lstControlTree))
    # a=json.loads(lstControlTree)
    for eachRow in lstControlTree:
        oLog.SetLogObj("",1,"Start: " + str(eachRow[0]) + " End: " + str(eachRow[1]))
        for each in eachRow[2]:
            oLog.SetLogObj("",1,str(each))
                    
                        

# ExtractHeaderFonts(ResumePath,ResumeFile)
ExtractPositions(ResumePath,ResumeFile)