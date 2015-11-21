# coding: utf-8
from abc import ABCMeta, abstractmethod

class Storage(object): 
    __metaclass__=ABCMeta
    @abstractmethod
    def add_file(self): 
        pass
    
    
    @abstractmethod
    def delete_file(self):
        pass
    
	
    @abstractmethod
    def get_list_of_files(self):
        pass


