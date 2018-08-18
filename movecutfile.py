import os
import mysqlspi
path="E:/over"
targetpath="E:/farmat"
results=mysqlspi.query_repeat()
def scan_files(directory,postfix=None):
    files_list=[]
    path=str(directory).encode("utf-8")
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            print(special_file)
            # if postfix:
            #     if special_file.endswith(postfix):
            #         cutmove(root,special_file)
            # else:
                # cutmove(root,special_file)
            titlestr=special_file    
            if(special_file.endswith('.azw')):
                titlestr=titlestr.replace(".azw","")
            elif(special_file.endswith('.azw3')):
                titlestr=titlestr.replace(".azw3","")
            elif(special_file.endswith('.epub')):
                titlestr=titlestr.replace(".epub","")
            elif(special_file.endswith('.mobi')):
                titlestr=titlestr.replace(".mobi","")
            for fileinfo in results:
                # print(titlestr)
                if(fileinfo['title']==titlestr):
                    print(titlestr)
                    cutmove(root,special_file)
                    break


def cutmove(root,special_file):
    if os.path.isfile(targetpath+"/"+special_file):
        os.remove(targetpath+"/"+special_file)
    os.rename(root+"/"+special_file,targetpath+"/"+special_file)

def runmian():
    if not os.path.isdir(targetpath):
        os.mkdir(targetpath)
    scan_files(path)

runmian()    
           