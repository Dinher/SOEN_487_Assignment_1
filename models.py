from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Book(db.Model):
	title=db.Column(db.String(80),unique=True,nullable=False,primary_key=True)
	def __repr__(self):
		return "<Title: {}>".format(self.title)

class User(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	username = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)

	def __repr__(self):
		return "<User {}: {} {} {}".format(self.id, self.username, self.email, self.password)

class Project(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	def __repr__(self):
		return "<Project {}: {} {}".format(self.id, self.name, self.user_id)

class Files(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	timestamp = db.Column(db.String(20), nullable=False)
	content = db.Column(db.Text)
	def __repr__(self):
		return "<User {}: {} {} {}".format(self.id, self.name, self.timestamp, self.content)