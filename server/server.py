# coding: utf-8
from flask import Flask, request, jsonify
import os
import sys
import logging
app = Flask(__name__)
download_folder = "./download/"

from database import DB_CONNECTOR, ORM
from flask.ext.login import LoginManager
import flask.ext.login as flask_login
import argparse
from Storage import Storage
from StorageFilesystem import StorageFilesystem
from StorageCloud import StorageCloud

logger = logging.getLogger(__name__)
#logging.basicConfig(filename='logging.log', level=logging.DEBUG)
logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTOR
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
logger.info('create db')
db = ORM(app)
logger.info('created db')
login_manager = LoginManager()
logger.info('created login manager')
login_manager.init_app(app)
logger.info('init app')

SESSION_EMAIL = "email"

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', default = 'server')
    return parser

@app.route("/", methods=['POST', 'GET', 'DELETE'])
@flask_login.login_required
def hello():
    logger.info('hello')
    if request.method == 'POST':
        add_files = request.get_json()
        file_data = add_files['data']
        file_name = add_files['filename']
        size_file = add_files['size_file']
        
        if save_data == "cloud":
            storage = StorageCloud()
            logger.info('cloud')
        else:
            storage = StorageFilesystem(db.user_folder(flask_login.current_user.id))
            logger.info('filesystem')
        print "file_name = ", file_name 
        storage.add_file( file_data, file_name, size_file)
        logger.info('post method')
        logger.info('add new file %s', file_name)
        return "POST METHOD!"
    elif request.method == 'DELETE':
        logger.info('delete')
        delete_file = request.get_json()
        file_name = delete_file['filename']
        print "I want delete file_name = ", file_name
        if save_data == "cloud":
            storage = StorageCloud()
            logger.info('cloud')
        else:
            storage = StorageFilesystem(db.user_folder(flask_login.current_user.id))
            logger.info('filesystem')
		
        storage.delete_file(file_name)
        #os.remove(os.path.join(db.user_folder(flask_login.current_user.id), file_name))
        
        logger.info('delete method')
        logger.info('delete file %s', file_name)
        return "DELETE METHOD!"
    return "hello!"

@app.route("/new_files")
@flask_login.login_required
def new_files():
    print "new files" 
    #current_content_files = os.listdir(os.path.join(os.getcwd(), db.user_folder(flask_login.current_user.id)))
    current_content_files = storage.get_list_of_files()
    return jsonify(file_list = current_content_files)

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id)

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        entry_client = request.get_json()
        email = entry_client['login']
        password = entry_client['password']
        folder = entry_client['folder']
        if db.check_user(email, password):
            logger.info('user email %s', email)
            user = db.User(email, password, folder)
            if not os.path.exists(os.path.join(os.getcwd(), folder)):
                os.mkdir(os.path.join(os.getcwd(), folder))
            flask_login.login_user(user)
        else:
            logger.info('create new user email %s', email)
            db.create_new_user(email, password, folder)
            if not os.path.exists(os.path.join(os.getcwd(), folder)):
                os.mkdir(os.path.join(os.getcwd(), folder))
            #import pdb
            #pdb.set_trace()
            user = db.User(email, password, folder)
            flask_login.login_user(user)
    return ""
	

def install_server():
    parser = createParser()
    namespace = parser.parse_args()
    global save_data
    save_data = namespace.save
    logger.info('storage type %s', save_data)  
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
 
if __name__ == "__main__":
    install_server()