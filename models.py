
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

from sqlalchemy.orm import backref


db = SQLAlchemy()
class users(db.Model,UserMixin):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name  = db.Column(db.String(255))
    phone      = db.Column(db.String(255),unique=True)
    email      = db.Column(db.String(255),unique=True)
    password   = db.Column(db.String(255))
    IDnumber   = db.Column(db.String(255),unique=True)
    picture    = db.Column(db.Text)
    is_admin   = db.Column(db.Boolean,default=False)
    is_staff   = db.Column(db.Boolean,default=False)
    can_create = db.Column(db.Boolean,default=False)
    can_edit   = db.Column(db.Boolean,default=False)
    can_delete = db.Column(db.Boolean,default=False)
    program    = db.relationship('programme', backref='users', lazy=True)
    attend     = db.relationship('attendance', backref='users',lazy=True)
    visitors   = db.relationship('visitor',backref='users',lazy=True)

    def __repr__(self):
        return '<users %r>' % self.first_name+'' +self.last_name


class programme(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255))
    duration_from = db.Column(db.DateTime,nullable=False)
    duration_to   = db.Column(db.DateTime,nullable=False)   
    users_id      = db.Column(db.Integer,db.ForeignKey(users.id),nullable=False)  

class attendance(db.Model):
    id         = db.Column(db.Integer,primary_key=True)
    users_id   = db.Column(db.Integer,db.ForeignKey(users.id),nullable=False)
    timein     = db.Column(db.DateTime,default=datetime.now())
    timeout    = db.Column(db.DateTime,nullable=True)

class visitor(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name  = db.Column(db.String(255))
    phone      = db.Column(db.String(255))
    email      = db.Column(db.String(255))
    invitedDate = db.Column(db.String(100))
    timein     = db.Column(db.DateTime)
    timeout    = db.Column(db.DateTime,nullable=True)
    active  =   db.Column(db.Boolean,default=False)
    inviteCode = db.Column(db.String(255))
    invited_by = db.Column(db.Integer,db.ForeignKey(users.id),nullable=False)
    luggages   = db.relationship('luggage',backref='visitor',lazy=True)
   
class luggage (db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    item_name     = db.Column(db.String(255))
    visitors_id   = db.Column(db.Integer,db.ForeignKey(visitor.id),nullable=False)    
    date_logged   = db.Column(db.DateTime,default=datetime.now())      



class Articles(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(255))
    decription    = db.Column(db.Text)
    banner        = db.Column(db.Text)
    content       = db.Column(db.Text)
