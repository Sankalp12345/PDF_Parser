import datetime
class Logger:
    def __init__(self, strLogPath):
        self.LogPath=strLogPath
        self.Level=0
        fileHandle=open(strLogPath,"w",encoding='utf-8')
        fileHandle.writelines(datetime.datetime.now().strftime("%d %b %Y") + "\n")
        fileHandle.writelines("==================================================" + "\n")
        fileHandle.close()

    def setLevel(self,iLevel):
        self.Level=iLevel

    def SetLogObj(self, strLabel="",iLevel=0,oObject=None):
        if self.Level==0 or self.Level==iLevel:
            fileHandle=open(self.LogPath,"a",encoding='utf-8')
            if strLabel!="":
                fileHandle.write(strLabel + "\n")
                fileHandle.write("==================================================" + "\n")
            else:
                fileHandle.write("\n")
            
            if oObject!=None: 
                fileHandle.write(str(oObject))
                fileHandle.write("\n ==================================================" + "\n")
            fileHandle.write("\n")
            fileHandle.close()

    def SetLog(self, strLabel,iLevel):
        if self.Level==0 or self.Level==iLevel:
            fileHandle=open(self.LogPath,"a",encoding='utf-8')
            fileHandle.write(strLabel + "\n")
            fileHandle.write("==================================================" + "\n")
            fileHandle.close()