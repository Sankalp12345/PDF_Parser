import pdfminer as oPdf
import util.FileManager as fm
import util.Logger as log
import util.Language as ln
import util.Enumerator as enum
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Product Manager/"
ResumeFile="Abhijit_Tadke_APM_Paddle_Lift.pdf"
# SubjectResume = fm.ReadFile(ResumePath,ResumeFile)

oLog=log.Logger("D:/Users/Sankalp/Documents/Work/MyLearning/Python/PDF_Parser/DebugLog/Debug.log")
oLog.setLevel=0
Coordinates="a={} b={} c={} d={} TEXT={}"
for page_layout in extract_pages(ResumePath+ResumeFile):
    for element in page_layout:
        # oLog.SetLogObj("",1,element)
        oLog.SetLogObj("",1,Coordinates.format(element.x0,element.x1,element.y0,element.y1,element))

        # if isinstance(element, LTTextContainer):
        #     for text_line in element:
        #         for character in text_line:
        #             if isinstance(character, LTChar):