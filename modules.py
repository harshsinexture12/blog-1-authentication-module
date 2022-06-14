from sqlalchemy import false
from blog import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate 


# Add Database 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/kblog"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

#initialize the database 
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #date_added = db.Column(db.DateTime, default=datetime.utcnow)
    full_name = db.Column(db.String(100), nullable=False)
    user_pic = db.Column(db.String(255), nullable=True)
    about_author  = db.Column(db.String(200), nullable=True)
    email  = db.Column(db.String(200), nullable=False)
    is_admin  = db.Column(db.String(10), nullable=False, default='False')
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(512), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"),nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_msg = db.Column(db.String(512), nullable=False)
    user_id =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"),nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id =  db.Column(db.Integer , db.ForeignKey('post.id', ondelete="cascade"),nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"),nullable=False)
    post_id =  db.Column(db.Integer , db.ForeignKey('post.id', ondelete="cascade"),nullable=False)


class Follower_Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"),nullable=False)
    follower_id =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"),nullable=False)
