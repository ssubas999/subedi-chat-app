# models.py
import os, flask_sqlalchemy, app


# app.app = app modules app variable
# app.app.config['SQLALCHEMY_DATABASE_URI']  = os.getenv('DATABASE_URL')
app.app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://ssubas999:1Maryland1@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app.app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(25))
    user_message = db.Column(db.String(500))
    user_image = db.Column(db.String(500))
    
    def __init__(self, name, message, image):
        self.user_name = name
        self.user_message = message
        self.user_image = image
        
    def __repr__(self):
        # return '<Message user_name: %s>' % self.user_name
        return "{'user_name':'%s', 'user_message':'%s', 'user_image':'%s'}" % (self.user_name, self.user_message, self.user_image)