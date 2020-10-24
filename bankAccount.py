# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 14:51:25 2020

@author: 86156
"""
'''
there is a bank account 
this bank account is shared between different people,
which means more than one person know the password and account
number of this account and can draw money from this account or
deposit money into this account
realize this account by python multi-threads
both drawing and depositing will change the balance, so no matter when,
there must be only one person and only one kind of procedure
'''

import threading
from concurrent.futures import ThreadPoolExecutor

class Account():
    def __init__(self, no, balance):
        self.no = no
        self._balance = balance
        self.lock = threading.RLock()
        
    def drawDeposit(self, amount, choice):
        self.lock.acquire()
        if choice == 'deposit':
            self._balance += amount
            print(amount, 'deposited! by', threading.current_thread().name)
            print('new balance: ', self._balance)
        elif self._balance < amount:
            print('balance not enough!, balance: ', self._balance)
        else:
            self._balance -= amount
            print(amount, 'drawed by', threading.current_thread().name)
            print('new balance:', self._balance)
        self.lock.release()
        
account = Account(12345, 0)
def draw(account, amount):
    account.drawDeposit(amount, 'draw')
def deposit(account, amount):
    account.drawDeposit(amount, 'deposit')
    
# the first way to create multi-threads
# define each thread and start them seperately
person0 = threading.Thread(target = deposit, args = (account, 20), name = 'C')
person0.start()
person0.join()
person1 = threading.Thread(target = draw, args = (account,10), name = 'A')
person2 = threading.Thread(target = draw, args = (account, 10), name = 'B')
person3 = threading.Thread(target = deposit, args = (account, 5), name = 'C')
person4 = threading.Thread(target = deposit, args = (account, 15), name = 'D')
person1.start()
person2.start()
person3.start()
person4.start()

# the second way to create multi-threads
# use concurrent.futures.ThreadPoolExecutor class and with...as expression to 
# use this as a thread pool
# the good point of with...as expression is that you don't need to use pool.shutdown()
# also it is faster to reuse a worker than to start a new thread
with ThreadPoolExecutor(max_workers = 8) as pool:
    for i in range(10):
        pool.submit(deposit, account,5)   
        pool.submit(draw, account, 10)
