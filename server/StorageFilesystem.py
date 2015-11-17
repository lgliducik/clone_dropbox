# coding: utf-8
import Storage from storage

class StorageFilesystem(Storage): 
    def __init__(self, folder):
        self.folder = folder
		
		
	def add_file(self, data_file, file_name):
        with open(os.path.join(self.folder, file_name), 'wb') as fd:
            fd.write(data_file.encode("utf8"))
    
	
	def delete_file(self, file_name):
        os.remove(os.path.join(self.folder, file_name))
		
		
    def get_list_of_files(self):
        current_content_files = os.listdir(os.path.join(os.getcwd(), self.folder))
		return current_content_files