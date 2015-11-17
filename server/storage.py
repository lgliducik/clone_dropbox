# coding: utf-8
from abc import ABCMeta, abstractmethod

class Storage(metaclass=ABCMeta): 
    @abstractmethod
    def add_file(): 
        pass
    
    
    @abstractmethod
    def delete_file():
        pass
    
	
    @abstractmethod
    def get_list_of_files():
        pass


