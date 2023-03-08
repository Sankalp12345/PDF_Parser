from pdfminer.high_level import extract_pages
import pdfminer
from pdfminer.layout import LTTextContainer
ResumePath="D:/Users/Sankalp/Documents/Work/MyLearning/Python/Parser/AI_ML_TrainTest_DataSet/Product Manager/"
ResumeFile="Swarnima Bhosale.pdf"
path=ResumePath+ResumeFile
def Parse(path):
    TotalPages=0
    for page_layout in extract_pages(path):
        TotalPages=TotalPages+1
    DocLength=TotalPages
    for page_layout in extract_pages(path):
        print("Page Layout: "+str(page_layout))
        print("Page Height: "+str(page_layout.y1))
        TotalPages=TotalPages-1
        Offset=TotalPages*page_layout.y1
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                print(element.get_text())
                print("left="+str(element.x0) + " bottom=" + str(element.y0) + " right=" + str(element.x1) + " top="+str(element.y1))

                print("left="+str(element.x0) + " bottom=" + str(element.y0 + Offset) + " right=" + str(element.x1) + " top="+str(element.y1 + Offset))
    print(TotalPages)

Parse(path)