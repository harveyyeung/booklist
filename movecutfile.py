import os

path="C:/Users/yanghaowei/Desktop/testfloader"
targetpath="C:/Users/yanghaowei/Desktop/targetfloader"
def scan_files(directory,postfix=None):
    files_list=[]
    path=unicode(directory,'utf-8')
    for root, sub_dirs, files in os.walk(path):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    cutmove(root,special_file)
            else:
                cutmove(root,special_file)

def cutmove(root,special_file):
    if os.path.isfile(targetpath+"/"+special_file):
        os.remove(targetpath+"/"+special_file)
    os.rename(root+"/"+special_file,targetpath+"/"+special_file)

def runmian():
    if not os.path.isdir(targetpath):
        os.mkdir(targetpath)
    scan_files(path,".mobi")

runmian()    
           