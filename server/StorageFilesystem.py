# coding: utf-8
from Storage import Storage
import os

class StorageFilesystem(Storage): 
    def __init__(self, folder):
        self.folder = folder
		
		
    def add_file(self, data_file, file_name, size_of_file):
        with open(os.path.join("..",os.path.join("server", os.path.join(self.folder, file_name))), 'wb') as fd:
            fd.write(data_file.encode("utf8"))
    
	
    def delete_file(self, file_name):
        #os.remove(    os.path.join("..",os.path.join("server", os.path.join(self.folder, file_name)))             )
        print "delete file ", os.path.join("..",os.path.join("server", os.path.join(self.folder, file_name)))
        os.remove(os.path.join("..",os.path.join("server", os.path.join(self.folder, file_name))))
		
		
    def get_list_of_files(self):
        current_content_files = os.listdir(    os.path.join("..",os.path.join("server", os.path.join(os.getcwd(), self.folder) ))    )
        return current_content_files
     
    def set_folder(self, folder):
        self.folder = folder
	