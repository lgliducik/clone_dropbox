# coding: utf-8
import sqlite3 as lite
import requests
import os
import time
import sys
import hashlib
import logging
import argparse
from sqlalchemy import Column, String, Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
metadata = MetaData()
class File_my(Base):
    __tablename__ = 'list_of_file'
    path_name = Column(String(250), primary_key = True)
    time_mod = Column(String(250))
	
    def __init__(self, path_name, time_mod):
        self.path_name = path_name
        self.time_mod = time_mod
    def __repr__(self):
        return "<File_my('%s', '%s')>" % (self.path_name) % (self.time_mod)


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logging.log', level=logging.DEBUG)

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', default = './')
    parser.add_argument('-l', '--login', default = '')
    parser.add_argument('-p', '--password', default = '')
    return parser

def get_changes(root_folder, session):
    current_content = set(os.listdir(root_folder))
    old_files_new = []
    for row in session.query(File_my, File_my.path_name):
        old_files_new.append(row.path_name)
    session.commit()
    prev_content = set(i for i in old_files_new)
    session.commit()
    return add_new_files(current_content, prev_content)

def add_new_files(current_content, prev_content):
    return current_content - prev_content, (prev_content - current_content)

def add_new(folder, new_files, session, cookies):
    for new_file_name in new_files:
        print "add new"
        file_new = File_my(new_file_name, str(os.path.getmtime(os.path.join(folder, new_file_name))))
        session.add(file_new)
        session.commit()
        payload = {'filename':new_file_name,'data':open(os.path.join(folder, new_file_name), 'rb').read()}
        r = requests.post("https://radiant-reef-1251.herokuapp.com/" , json = payload, cookies = cookies)
        print r.text, 'status = ', r.status_code
        logger.info('add file %s', new_file_name)

def add_new_reload(folder, new_files, session, cookies):
    for new_file_name in new_files:
        session.query(File_my).filter(File_my.path_name == new_file_name).delete()
        session.commit()	
        file_new = File_my(new_file_name, str(os.path.getmtime(os.path.join(folder, new_file_name))))
        session.add(file_new)
        session.commit()
        payload = {'filename':new_file_name,'data':open(os.path.join(folder, new_file_name), 'rb').read()}
        r = requests.post("https://radiant-reef-1251.herokuapp.com/" , json = payload, cookies = cookies)
        print r.text, 'status = ', r.status_code
        logger.info('reload modified file %s', new_file_name)

def delete_files(removed_files, session, cookies):
    for delete_file_name in removed_files:
        session.query(File_my).filter(File_my.path_name == delete_file_name).delete()
        session.commit()
        payload = {'filename':delete_file_name}
        r = requests.delete("https://radiant-reef-1251.herokuapp.com/", json = payload, cookies = cookies)
        print r.text, 'status = ', r.status_code
        logger.info('delete file %s', delete_file_name)

def create_table():
    engine = create_engine('sqlite:///dropbox.db') 
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind = engine)
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()
    return session 

#def detete_files_from_client( delete_from_client,cookies):
#    for delete_file_name in delete_from_client:
#        payload = {'filename':delete_file_name}
#        r = requests.delete("http://127.0.0.1:5000/", json = payload, cookies = cookies)

#def get_files(session, cookies):
#    r = requests.get("http://127.0.0.1:5000/new_files", cookies = cookies)
    #print r.text, 'status = ', r.status_code, 'response', r.json()
#    return r.json()['file_list']

def get_changes_mod(root_folder, session):
    reload_to_server = []
    current_content = set(os.listdir(root_folder))
    current_content_time = set(str(os.path.getmtime(os.path.join(root_folder, i))) for i in current_content)
    
    #def fn(file_name):
    #    return str(os.path.getmtime(os.path.join(root_folder, file_name)))

    #gen = (fn(file_name) for file_name in current_content)
    #current_content_time = set()
    current_zip = zip(current_content, current_content_time)
    old_files_new = []
    old_files_new_time = []
    for row in session.query(File_my, File_my.path_name, File_my.time_mod):
        old_files_new.append(row.path_name)
        old_files_new_time.append(row.time_mod)
    session.commit()
    prev_content = set(i for i in old_files_new)
    prev_content_time = set(i for i in old_files_new_time)
    prev_zip = zip(prev_content, prev_content_time)
    session.commit()
    for d1 in current_zip:
        for d2 in prev_zip:
            if d1[0] == d2[0]:
                if d1[1] != d2[1]:
                    reload_to_server.append(d1[0])
    return  reload_to_server               
	
def main():
    session = create_table()
    parser = createParser()
    namespace = parser.parse_args()
    payload = {'login':namespace.login, 'password':namespace.password, 'folder': namespace.folder}
    r = requests.post("https://radiant-reef-1251.herokuapp.com/login", json = payload)
    logger.info('username %s, userpassword %s', namespace.login, namespace.password)
    if not os.path.exists(os.path.join(os.getcwd(), namespace.folder)):
        os.mkdir(os.path.join(os.getcwd(), namespace.folder))
        logger.info('create new folder %s', namespace.folder)
    while True:
        try:
            files_reload_to_server = get_changes_mod(namespace.folder, session)
            add_new_reload(namespace.folder, files_reload_to_server, session, r.cookies)
            new_files, removed_files = get_changes(namespace.folder, session)
            add_new(namespace.folder, new_files, session, r.cookies)
            delete_files(removed_files, session, r.cookies)
        except Exception:
            logger.exception('uncatch exception')
        time.sleep(1)


if __name__ == '__main__':
    main()