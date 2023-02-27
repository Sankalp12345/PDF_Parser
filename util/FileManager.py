import os

def listFolders(path):
    folderList=[]
    fileList=listFiles(path)
    for folder in fileList:
        if os.path.isdir(path+"/"+folder):
            folderList.append(folder)
            # print(folder)
    return folderList

def listFiles(path):
    fileList = []
    for file in os.listdir(path):
        fileList.append(file)
    return fileList

def listFilewithExtension(path, strExtension):
    fileList = []
    for file in os.listdir(path):
        if file.endswith("." + strExtension):
            fileList.append(file)
    return fileList

def ReadFile(path, filename):
    content=open(path + filename,"r",encoding='utf-8')
    FileContent=content.read()
    return FileContent

def SaveNewFile(path, content, filename):
    print("path=",path)
    print("filename=",filename)
    newFile=open(path + "/" + filename,"w", encoding="utf-8")
    newFile.write(str(content))
    newFile.close()

def AppendToFile(path, content, filename):
    if content!=None:
        newFile=open(path + "/" + filename,"a", encoding="utf-8")
        newFile.write(str(content))
        newFile.close()