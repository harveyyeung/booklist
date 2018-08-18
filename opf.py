
import os
from lxml import etree
import json
import util
LIBRARY_DIR = os.path.abspath('.') + os.sep

RECOVER_PARSER = etree.XMLParser(recover=True, no_network=True)
NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
}


class Book(object):

    def __init__(self, book_id=None):
        if book_id:
            self.open(book_id)

    def fromstring(self, raw, parser=RECOVER_PARSER):
        return etree.fromstring(raw, parser=parser)

    def read_doc_props(self, raw):

        root = self.fromstring(raw)
        try:
            self.title =''
            self.title = root.xpath('//dc:title', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            self.title =''
        try:
            # self.author = root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']})[0].text
            self.authors=[]
            for author in root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']}):
                self.authors.append(author.text)
            # self.author=json.dumps(authors, encoding='UTF-8', ensure_ascii=False)
            self.authors=str(json.dumps(self.authors, encoding='UTF-8', ensure_ascii=False))
        except  BaseException:
            pass
            # self.authors=str([])
        try:
            self.publisher=''
            self.publisher = root.xpath('//dc:publisher', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            self.publisher=''
        try:
            self.description =''
            self.description = root.xpath('//dc:description', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            self.description =''
        try:
            # self.subjects= {subject.text for subject in root.xpath('//dc:subject', namespaces={'dc': NAMESPACES['dc']})}
            # print self.subjects
            self.subjects=[]
            subjects = root.xpath('//dc:subject', namespaces={'dc': NAMESPACES['dc']})
            for subject in subjects:
                self.subjects.append(subject.text)
            self.subjects = str(json.dumps(self.subjects, encoding='UTF-8', ensure_ascii=False))
        except BaseException:
            self.subjects=str([])                          
        try:
            identifiers = root.xpath('//dc:description', namespaces={'dc': NAMESPACES['dc']})
            self.isbn=''
            self.mobiasin=''
            for item in identifiers:
                scheme = None
                for xkey in item.attrib.keys():
                    if xkey.endswith('scheme'):
                        scheme = item.get(xkey)
                if(scheme and scheme.lower() == 'isbn'):
                    self.isbn=item.text
                elif(scheme and scheme.lower() == 'mobi-asin'):
                    self.mobiasin=item.text
        except BaseException:
            pass                               

    def open(self,path):
        oebps_content = open(str(path),"rb").read()
        self.read_doc_props(oebps_content)

import time 
import mysqlspi
if __name__ == '__main__':

    t = time.time()
    uuid = int(t)
    #
    filelist = util.scan_files('E:/opf',postfix='.opf')
    for file in filelist:
        uuid+=1
        book = Book("E:/opf/"+file)
        jpgurl=file.replace('.opf', '.jpg')
        # print(file)
        # for i,j in vars(book).items():
        #     try:
        #         print(i)
        #         print(j)
        #     except UnicodeError as u:
        #         continue
        bookinfo ={
          'uuid':uuid,
          'title':book.title,
          'author':book.authors,
          'isbn10':book.isbn,
          'isbn16':book.mobiasin,
          'author_info':'',
          'publisher':book.publisher, 
          'summary':book.description, 
          'dbaltid':'', 
          'grade':'', 
          'cotegoryid':'', 
          'image':str(uuid),
          'createtime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
          'status':1
        }
        print(book.authors)

        flag = mysqlspi.insert_bookinfo(bookinfo)
        try:
            if flag:
                os.rename('E:/opf/'+jpgurl,'E:/opf/'+str(uuid)+'.jpg')
        except BaseException:
            pass        
        print(uuid)
        # result = json.dumps(book.subjects)
        # for i,j in vars(book).items():
        #     try:
        #         print(i)
        #         print(j)
        #     except UnicodeError as u:
        #         continue
    # book = Book('‪E:/farmat/做最有价值的经理人.opf')
    # book = Book('‪E:/farmat/做最有价值的经理人.opf')
    # print book.title
    # print book.subjects
    # result = json.dumps(book.subjects, encoding='UTF-8', ensure_ascii=False)
    # print result
    # print book.publisher
    # for i,j in vars(book).items():
    #     try:
    #         print(i)
    #         print(j)
    #     except UnicodeError as u:
    #         continue