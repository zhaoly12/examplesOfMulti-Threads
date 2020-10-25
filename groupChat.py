# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 16:58:26 2020

@author: 86156
"""

'''
create a online group chat use TCP and multi-threads
everyone in the group chat can share their thoughts with others
and all the words and its teller can be seen for every memebers in the group
'''

from socket import *
import threading
from concurrent.futures import ThreadPoolExecutor
import os

class Server():
    
    def __init__(self, *args, cpuCount = os.cpu_count()):
        self.ip = args[0]
        self.port = args[1]
        self.cpuCount = cpuCount
        self.clients = set()
        
    def __swapMessage(self, client, addr):
        client.send(('welcome').encode('UTF-8'))
        while True:
            message = client.recv(2048).decode('UTF-8') + ' from:' + addr.__repr__()
            print(message)
            if message == 'exit from:' + addr.__repr__():
                client.send('exit'.encode('UTF-8'))
                client.close()
                self.clients.discard(client)
                return
            else:
                for c in self.clients:
                    c.send(message.encode('UTF-8'))
    
    def __call__(self):
        self.server = socket(family = AF_INET, type = SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        with ThreadPoolExecutor(max_workers = self.cpuCount) as pool:
            # this server will never stop
            while True:
                client, addr = self.server.accept()
                self.clients.add(client)
                print('new client welcomed', addr)
                pool.submit(self.__swapMessage, client, addr)
        #self.server.close()
            
class Client():
    
    def __init__(self, *args):
        self.ip = args[0]
        self.port = args[1]
        
    def __messageFromServer(self):
        while True:
            message = self.client.recv(2048).decode('UTF-8')
            if message == 'exit':
                self.client.close()
                return
            else:
                print(message)
                
    def __messageToServer(self):
        while True:
            message = input()
            self.client.send(message.encode('UTF-8'))
            if message == 'exit':
                return       
        
    def __call__(self):
        self.client = socket(family = AF_INET, type = SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        readThread = threading.Thread(target = self.__messageFromServer)
        sendThread = threading.Thread(target = self.__messageToServer)
        readThread.start()
        sendThread.start()
        while True:
            if not(readThread.is_alive()) and not(sendThread.is_alive()):
                return
            
        
        
        