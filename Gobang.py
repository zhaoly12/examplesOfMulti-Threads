# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:49:24 2020

@author: 86156
"""

'''
monitor two people 
they are playing gobang
'''

import random
import threading

class Gobang():
    
    def __init__(self, size = 10):
        self.size = size
        self.Num = list(range(self.size * self.size))
        self.positions = []
        for i in range(size):
            self.positions.append([1])
            for j in range(size-1):
                self.positions[i].append(1)
        self.cond = threading.Condition()
        self.flag = 0
        
    def __win(self, value):
        for i in range(self.size):
            try:
                start = self.positions[i].index(value)
            except:
                break
            j = start
            while j <= self.size-5:
                count = 0
                for s in range(j, self.size-4):
                    if self.positions[i][s] == value:
                        j = s
                        count += 1
                        break
                if count == 0:
                    break
                for e in range(j+1, j+5):
                    if self.positions[i][e] != value:
                        j = e
                        break
                    else:
                        count += 1
                if count == 5:
                    return True
        return False
    
    def __full(self):
        for line in self.positions:
            if 1 in line:
                return False
        return True
    
    def show(self):
        for i in range(self.size):
            print(self.positions[i])
        print('______________________________________')
    
    def __white(self):
        if self.__full():
            print('draw')
            return True
        self.cond.acquire()
        while self.flag != 0:
            #print('waiting for black')
            self.cond.wait()
        num = random.choice(self.Num)
        x = num // self.size
        y = num % self.size
        self.positions[x][y] = 0
        self.Num.remove(num)
        print('white put a chess piece at: ', x, ',', y)
        self.show()
        self.flag = 1
        self.cond.notify_all()
        self.cond.release()
        if self.__win(0):
            print('white won!')
            return True
        return False
        
    def __black(self):
        if self.__full():
            print('draw')
            return True
        self.cond.acquire()
        while self.flag != 1:
            #print('waiting for white')
            self.cond.wait()
        num = random.choice(self.Num)
        x = num // self.size
        y = num % self.size
        self.positions[x][y] = -1
        self.Num.remove(num)
        print('black put a chess piece at: ', x, ',', y)
        self.show()
        self.flag = 0
        self.cond.notify_all()
        self.cond.release()
        if self.__win(-1):
            print('black won!')
            return True
        return False

# in sequence
go = Gobang()
while True:
    if go._Gobang__white():
        break
    if go._Gobang__black():
        break

# multi-threads mode
go = Gobang()
for i in range(50):             
    threading.Thread(target = go._Gobang__black).start()
for i in range(50):
    threading.Thread(target = go._Gobang__white).start()  