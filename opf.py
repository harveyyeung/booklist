#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lxml import etree
import json
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
            self.title = root.xpath('//dc:title', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            pass
        try:
            # self.author = root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']})[0].text
            self.authors=[]
            for author in root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']}):
                self.authors.append(author.text)
            # self.author=json.dumps(authors, encoding='UTF-8', ensure_ascii=False)
            self.authors=json.dumps(self.authors, encoding='UTF-8', ensure_ascii=False)
        except  Exception,err:
            print err
        try:
            self.publisher = root.xpath('//dc:publisher', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            pass
        try:
            self.description = root.xpath('//dc:description', namespaces={'dc': NAMESPACES['dc']})[0].text
        except BaseException:
            pass
        try:
            # self.subjects= {subject.text for subject in root.xpath('//dc:subject', namespaces={'dc': NAMESPACES['dc']})}
            # print self.subjects
            self.subjects=[]
            subjects = root.xpath('//dc:subject', namespaces={'dc': NAMESPACES['dc']})
            for subject in subjects:
                self.subjects.append(subject.text)
            self.subjects = json.dumps(self.subjects, encoding='UTF-8', ensure_ascii=False)   
        except BaseException:
            pass                               
        try:
            identifiers = root.xpath('//dc:description', namespaces={'dc': NAMESPACES['dc']})
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
        oebps_content = open(path,"rb").read()
        self.read_doc_props(oebps_content)

   
if __name__ == '__main__':
   
    book = Book(unicode('C:/Users/yanghaowei/Desktop/targetfloader/metadata.opf','utf-8'))
    # print book.title
    # print book.subjects
    result = json.dumps(book.subjects, encoding='UTF-8', ensure_ascii=False)
    # print result
    # print book.publisher
    for i,j in vars(book).items():
        try:
            print i
            print j
        except UnicodeError as u:
            continue