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

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTOR
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = ORM(app)
login_manager = LoginManager()
login_manager.init_app(app)
SESSION_EMAIL = "email"

@app.route("/", methods=['POST', 'GET', 'DELETE'])
@flask_login.login_required
def hello():
    if request.method == 'POST':
        add_files = request.get_json()
        file_data = add_files['data']
        file_name = add_files['filename']
        folder = os.path.join("D:\workproject\pyproject\clone_dropbox-master\clone_dropbox-master\server", db.user_folder(flask_login.current_user.id))
        with open(os.path.join(folder, file_name), 'wb') as fd:
            fd.write(file_data.encode("utf8"))
        logger.info('post method')
        logger.info('add new file %s', file_name)
        return "POST METHOD!"
    elif request.method == 'DELETE':
        delete_file = request.get_json()
        file_data = delete_file['filename']
        os.remove(os.path.join(db.user_folder(flask_login.current_user.id), file_data))
        logger.info('delete method')
        logger.info('delete file %s', file_data)
        return "DELETE METHOD!"
    return "hello!"

@app.route("/new_files")
@flask_login.login_required
def new_files():
    current_content_files = os.listdir(os.path.join(os.getcwd(), db.user_folder(flask_login.current_user.id)))
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
            logger.info('create new user email%s', email)
            db.create_new_user(email, password, folder)
            if not os.path.exists(os.path.join(os.getcwd(), folder)):
                os.mkdir(os.path.join(os.getcwd(), folder))
            user = db.User(email, password, folder)
            flask_login.login_user(user)
    return ""

if __name__ == "__main__":
    app.run(debug = True)