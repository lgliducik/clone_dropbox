# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy

DB_CONNECTOR = 'sqlite:///users.db'


class ORM(object):

    def __init__(self, app):
        self.db = SQLAlchemy(app)

        class User(self.db.Model):
            __tablename__ = 'users'

            id = self.db.Column(self.db.Integer, primary_key=True)
            email = self.db.Column(self.db.String, unique=True)
            password = self.db.Column(self.db.String)
            folder = self.db.Column(self.db.String)
            authenticated = self.db.Column(self.db.Boolean, default=False)

            def __init__(self, email, password, folder):
                self.email = email
                self.password = password
                self.folder = folder

            def __repr__(self):
                return "<User('%s', '%s', '%s')>" % (self.email, self.password, self.folder)


            def is_active(self):
                return True
        		
            def is_anonymous(self):
                return False
        		
            def get_id(self):
                return self.email

        		
            def is_authenticated(self):
                return self.authenticated

        self.User = User
        self.db.create_all()
        
    def create_new_user(self, email, password, folder):
        user = self.User(email, password, folder)
        self.db.session.add(user)
        self.db.session.commit()

    def all_users(self):
        return self.User.query.all()

    def check_user(self, email, password):
        entry = self.User.query.filter_by(email=email, password=password).first()
        return not entry is None

    def get_user(self, email):
        return self.User.query.filter_by(email=email).first()
		
    def user_folder(self, id):
        folder_name = self.User.query.filter_by(id=id).first()
        return folder_name.folder
