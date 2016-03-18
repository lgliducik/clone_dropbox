# coding: utf-8
import requests
import os
from Storage import Storage

STATUS_NO_CONTENT = 204
STATUS_FORBIDDEN = 403
MAX_LENGHT_BYTE = 1024


class StorageCloud(Storage):
    def __init__(self):
        self.token = ''
        self.storageurl = ''	
        self.is_auth = False
        self.containername = self.get_containername()
        print "!!!!!!!!!!!!!!!!!self.auth_storage = ", self.auth_storage('8730_db', 't4Iy0PvXnv')
    
	
    def add_file(self, data_file, file_name, size_of_file):
        print("!!!!!!!!!!add file cloud")
        if self.is_auth == True:
            if size_of_file < MAX_LENGHT_BYTE:
                headers_token = {'X-Auth-Token':self.token, 'Content-Lenght':str(size_of_file)}
            else:
                headers_token = {'X-Auth-Token':self.token, 'Transfer-Encoding':'chunked'}
            data = {'file': data_file}
            print "self.storageurl = ", self.storageurl
            print "self.containername = ", self.containername
            print "!!!!!!!!!!data = ", self.storageurl + str(self.containername) + '/' + file_name
            r_add_file = requests.put(self.storageurl + str(self.containername) + '/' + file_name, headers=headers_token, data=data)
            print "!!!!!!!!!!!!!!!!r_add_file = ", r_add_file
            print "!!!!!!!!!!!!!!!!!!!!r_add_file.status_code = ", r_add_file.status_code
            return r_add_file.status_code
        else: 
            return STATUS_FORBIDDEN
    
	
    def delete_file(self, file_name):
        if self.is_auth == True:
            r_get_file = requests.delete(self.storageurl + '/' + self.containername + '/' + file_name, headers = {'X-Auth-Token': self.token})
            return r_get_file.status_code
        else:
            return STATUS_FORBIDDEN
    
	
    def get_list_of_files(self):
        if self.is_auth == True:
            r_list = requests.get(self.storageurl + '/' + self.containername, headers = {'X-Auth-Token': self.token})
            print r_list.text
        else:
            return STATUS_FORBIDDEN
	    
	
    def get_containername(self):
        if self.is_auth == True:
            r_list = requests.get(self.storageurl, headers = {'X-Auth-Token':self.token})
            self.containername = r_list.text
            return self.containername
        else:
            return STATUS_FORBIDDEN
    
	
    def auth_storage(self, login, password):
        headers = {'X-Auth-User': login, 'X-Auth-Key': password}
        r = requests.get("https://auth.selcdn.ru/" , headers = headers)
        self.token = r.headers['X-Auth-Token']
        self.storageurl = r.headers['X-Storage-Url']
        if r.status_code == STATUS_NO_CONTENT:
            self.is_auth = True
        else:
            self.is_auth = False
        return r.status_code