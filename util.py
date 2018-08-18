#coding=utf-8
'''
Created on 2018-5-11
'''

import random
import os
import re
random_seed = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a', 'Z','Y','X','W','V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A']
def randomChar(len):
    return ''.join(random.sample(random_seed, len))


def scan_files(directory,prefix=None,postfix=None):
    files_list=[]

    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(special_file)
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(special_file)
            else:
                files_list.append(special_file)
                            
    return files_list

def scan_files_no_root(directory,prefix=None,postfix=None,slug=None):
    files_list=[]
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(slug,special_file))
            elif prefix:
                if special_file.startswith(prefix):                                    
                    files_list.append(os.path.join(slug,special_file))
            else:
                files_list.append(os.path.join(slug,special_file))
                            
    return files_list
