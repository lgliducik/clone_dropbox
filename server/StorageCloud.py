# coding: utf-8
import requests
import os
from Storage import Storage
import logging
import sys

STATUS_NO_CONTENT = 204
STATUS_FORBIDDEN = 403
MAX_LENGHT_BYTE = 1024

logger = logging.getLogger(__name__)
logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)


class TokenExpire(Exception):
    pass


def check_token(f):
    def inner(self, *args, **kwargs):
        if self.token is not None:
            try:
                return f(self, *args, **kwargs)
            except TokenExpire:
                pass
        self.auth_storage()
        return f(self, *args, **kwargs)
    return inner


class StorageCloud(Storage):
    def __init__(self):
        self.token = None
        self.storageurl = ''	
        self.is_auth = False
        logger.info('self.auth_storage %s', self.auth_storage())
        self.containername = self.get_containername()
    

    def request_cloud(self, method, *args, **kwargs):
        logger.info('request_cloud method = %s, args = %s', method, str(args) + str(kwargs))
        result = getattr(requests, method)(*args, **kwargs)
        logger.info('request_cloud: result.status_code %s', result.status_code)
        logger.info('request_cloud: requests.codes.ok %s', requests.codes.ok)
        if result.status_code != requests.codes.ok and result.status_code != 204:
            raise TokenExpire
        return result


    def add_file(self, data_file, file_name, size_of_file):
        #if size_of_file < MAX_LENGHT_BYTE:
        headers_token = {'X-Auth-Token':self.token, 'Content-Lenght':str(size_of_file)}
        #else:
        #    headers_token = {'X-Auth-Token':self.token, 'Transfer-Encoding':'chunked'}
        data = {'file': data_file}
        r_add_file = self.request_cloud("put", self.storageurl + str(self.containername) + '/' + file_name, headers=headers_token, data=data)
        return r_add_file.status_code
    
	
    def delete_file(self, file_name):
        r_get_file = self.request_cloud("delete", self.storageurl + '/' + self.containername + '/' + file_name, headers = {'X-Auth-Token': self.token})
        return r_get_file.status_code
    
	
    def get_list_of_files(self):
        r_list = self.request_cloud("get", self.storageurl + '/' + self.containername, headers = {'X-Auth-Token': self.token})
        print r_list.text
	    
	
    def get_containername(self):
        logger.info('get_containername: self.storageurl %s', self.storageurl)
        r_list = self.request_cloud("get", self.storageurl, headers = {'X-Auth-Token':self.token})
        self.containername = r_list.text
        logger.info('get_containername: self.containername %s', self.containername)
        return self.containername
    
	
    def auth_storage(self):
        login, password = '8730_db', 't4Iy0PvXnv'
        headers = {'X-Auth-User': login, 'X-Auth-Key': password}
        #r = requests.get("https://auth.selcdn.ru/" , headers = headers)
        r = self.request_cloud("get", "https://auth.selcdn.ru/", headers = headers)
        logger.info('auth_storage: r.status_code %s', r.status_code)
        self.token = r.headers['X-Auth-Token']
        logger.info('auth_storage: self.token %s', self.token)
        self.storageurl = r.headers['X-Storage-Url']
        logger.info('auth_storage: self.storageurl %s', self.storageurl)
        return r.status_code