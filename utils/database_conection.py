# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 08:12:32 2020

@author: phyos
"""
import sqlite3

class DatabaseConection:
    def __init__(self, host):
        self.connection = None
        self.host = host
    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection
        
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb or exc_type or exc_type:
            self.connection.close()
        self.connection.commit()
        self.connection.close()