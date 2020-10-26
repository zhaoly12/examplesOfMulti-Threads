# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:52:40 2020

@author: 86156
"""

'''
Create a downloader using multi-threads
this downloader get url and target file from the user
and download resource got from the url into the target file
if 'pause' is set or there is something wrong with the network
when restarted, the downloader can download the rest part 
'''

import urllib
import os
from concurrent.futures import ThreadPoolExecutor 

class DownLoader:
    
    def __init__(self, targetFile = r'C:\Users\86156\Desktop\python.gif', 
                 url = 'https://static.easyicon.net/preview/54/540419.gif'):
        self.req = urllib.request.Request(url, method = 'GET')
        self.file = targetFile
        origin = urllib.request.urlopen(self.req)
        self.totalSize = int(dict(origin.headers).get('Content-Length',0))
        origin.close()
        self.__memory = None # memorize the pointer of every thread
        self.__completeRate = 0
        
    def __handle(self, *args):
        start = args[0]
        end = args[1]
        if start >= end:
            return start
        pointer = start
        target = open(self.file, 'rb+', True)
        try:
            origin = urllib.request.urlopen(self.req)
            for i in range(start):
                origin.read(1)
            target.seek(start)
            while pointer < end:
                c = origin.read(1024)
                target.write(c)
                pointer += len(c)
                self.__completeRate += (len(c) / self.totalSize)*100
                print(self.__completeRate, '% completed.')
            origin.close()
        finally:
            target.close()
            return pointer
        
    def __call__(self):
        workerNum = os.cpu_count()//2
        size =  self.totalSize // workerNum + 1
        with ThreadPoolExecutor(max_workers = workerNum) as pool:
            if self.__memory == None:
                starts = [i*size for i in range(workerNum)]
            else:
                starts = self.__memory
            futures = []
            for i in range(workerNum):
                futures.append(pool.submit(self.__handle, starts[i], \
                                           min((i+1)*size, self.totalSize)))
  
            for i in range(workerNum):
                while futures[i].running():
                    pass
            pointers = []
            for i in range(workerNum):
                pointers.append(futures[i].result())
        self.__memory = list(pointers)        
        
    