from flask import request
from flask import render_template, make_response
from flask import redirect
from flask import jsonify
import bcrypt as bcrypt
import datetime

from models import db, User, Project, Files				# get db models

from main import app
from auth import *										#encode, decode, protected endpoint
								
# Meta - Deletes all users
@app.route('/users/clearDabatase')
def usersDelete():
	User.query.delete()
	try:
		db.session.commit()
		return 'Deletion OK'
	except:
		return 'Deletion Fail'
	return 'Deletion ambiguous'

# Meta - Deletes all Projects
@app.route('/projects/clearDatabase')
def projectsDelete():
	Projects.query.delete()
	try:
		db.session.commit()
		return 'Deletion OK'
	except:
		return 'Deletion Fail'
	return 'Deletion ambiguous'

# Meta - Deletes all users
@app.route('/files/clearDatabase')
def filesDelete():
	Files.query.delete()
	try:
		db.session.commit()
		return 'Deletion OK'
	except:
		return 'Deletion Fail'
	return 'Deletion ambiguous'

# Meta - Dump SQL into CSV File
@app.route('/dumpDatabase')
def dumpDatabase():
	users = User.query.all()
	projects = Project.query.all()
	files = Files.query.all()
	filename = 'Database.dump'
	with open(filename,'w') as f:
		f.write(str(users))
		f.write(str(projects))
		f.write(str(files))
	return 'Database dumped to file: '+filename

# Meta - Show all users
@app.route('/users')
def users():
	users = ['None']
	users = User.query.all()
	return render_template('users.html',data=users)

# Meta - Show all database information
@app.route('/showDatabase')
def showDatabase():
	users = User.query.all()
	projects = Project.query.all()
	files = Files.query.all()
	response = make_response(render_template('showDatabase.html',users=users,projects=projects,files=files))
	return response

# API ROUTES
@app.route('/api/users/clearDabatase')
def APIusersDelete():
	User.query.delete()
	try:
		db.session.commit()
		return jsonify(message='Deletion OK')
	except:
		return jsonify(message='Deletion Fail')
	return jsonify(message='Deletion ambiguous')

@app.route('/api/projects/clearDatabase')
def APIprojectsDelete():
	Projects.query.delete()
	try:
		db.session.commit()
		return jsonify(message='Deletion OK')
	except:
		return jsonify(message='Deletion Fail')
	return jsonify(message='Deletion ambiguous')

@app.route('/api/files/clearDatabase')
def APIfilesDelete():
	Files.query.delete()
	try:
		db.session.commit()
		return jsonify(message='Deletion OK')
	except:
		return jsonify(message='Deletion Fail')
	return jsonify(message='Deletion ambiguous')

@app.route('/api/users')
def APIusers():
	json = { 'users':[],'projects':[],'files':[]}
	users = User.query.all()
	for u in users:
		json['users'].append({
			'id' : u.id,
			'username' : u.username,
			'email' : u.email,
		})
	response = make_response(jsonify(json))
	return response

@app.route('/api/users/<int:id>')
def APIusersByID(id):
	json = { 'users':[],'projects':[],'files':[]}
	u = User.query.filter_by(id=id).first()
	if u is not None:
		json['users'].append({
			'id' : u.id,
			'username' : u.username,
			'email' : u.email,
		})
		response = make_response(jsonify(json))
		return response
	else:
		json = {'msg':'Cannot find this user id.', 'code':404}
		response = make_response(jsonify(json))
		response.status_code = 404
		return response


@app.route('/api/projects')
def APIprojects():
	json = { 'users':[],'projects':[],'files':[]}
	projects = Project.query.all()
	for p in projects:
		json['projects'].append({
			'id' : p.id,
			'name' : p.name,
			'user_id' : p.user_id,
		})
	response = make_response(jsonify(json))
	return response

@app.route('/api/files')
def APIfiles():
	json = { 'users':[],'projects':[],'files':[]}
	files = Files.query.all()
	for f in files:
		json['files'].append({
			'id' : f.id,
			'name' : f.name,
			'content' : f.content,
			'project_id' : f.project_id,
			'timestamp' : f.timestamp,			
		})
	response = make_response(jsonify(json))
	return response

@app.route('/api/showDatabase')
def APIshowDatabase():
	json = { 'users':[],'projects':[],'files':[]}
	users = User.query.all()
	for u in users:
		json['users'].append({
			'id' : u.id,
			'username' : u.username,
			'email' : u.email,
		})
	projects = Project.query.all()
	for p in projects:
		json['projects'].append({
			'id' : p.id,
			'name' : p.name,
			'user_id' : p.user_id,
		})
	files = Files.query.all()
	for f in files:
		json['files'].append({
			'id' : f.id,
			'name' : f.name,
			'content' : f.content,
			'project_id' : f.project_id,
			'timestamp' : f.timestamp,			
		})
	
	response = make_response(jsonify(json))
	return response


# Clientside Routes
@app.route("/")
def home():
	return render_template('homepage.html')

@app.route('/login',methods=["GET","POST"])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()		
		# user in DB
		if user:
			hashed_password = user.password
			# Correct password
			if bcrypt.checkpw(password.encode('utf-8'),hashed_password):
				
				# give user new token
				auth_token = encode_auth_token(user.id)
				response = make_response(redirect('/projects'))
				response.set_cookie('token',auth_token)
				return response
			else:
				error = 'Incorrect Password'
				return render_template('login.html',title="Login",error=error)
		else:
			error = 'Incorrect Username/password'
			return render_template('login.html',title="Login",error=error)
	else:
		return render_template('login.html',title="Login")

@app.route('/logout',methods=["GET"])
def logout():
	response = make_response(redirect('/'))
	# give user invalid token
	response.set_cookie('token','')
	return response

@app.route('/signup',methods=["POST"])
def signup():
	if request.form:		
		username = request.form.get('username')
		password = request.form.get('password')
		password_confirm = request.form.get('password-confirm')
		email = request.form.get('email')

		check_username = User.query.filter_by(username=username).first()
		check_email = User.query.filter_by(email=email).first()
		error = None

		# check matching passwords
		if password != password_confirm:
			error = 'Passwords do not match'
			return render_template('login.html',title='Login', error=error)
		
		# add user
		elif not check_username and not check_email:
			# secure password
			hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
			new_user = User(username=username, password=hashed_password, email=email)
			
			db.session.add(new_user)
			try:
				db.session.commit()
			except:			
				error = 'Error in registering user'
				return make_response(render_template('login.html',title='Login',error=error))
			
			# give new user a token 
			user = User.query.filter_by(username=username).first()
			auth_token = encode_auth_token(user.id)
			
			response = make_response(redirect('/projects'))
			response.set_cookie('token',auth_token)
			return response
		
		# names/email already in DB
		else:
			print('Username or email is already used')
			error = 'Username or email is used'
			return render_template('login.html',title='Projects', error=error)
	
	return render_template('login.html',title='Projects', error=error)
		
# Displays all User projects
@app.route('/projects',methods=["GET","POST"])
@protected_endpoint
def projects(auth):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		# display current projects
		if request.method == 'GET':			
			user = User.query.filter_by(id=client_id).first()
			projects = Project.query.filter_by(user_id=user.id).all()
			response = make_response(render_template('projects.html',title=user.username,username=user.username,projects=projects))
			return response

		# add new project
		elif request.method == 'POST':
			project_name = request.form.get('project_name')
			user = User.query.filter_by(id=client_id).first()

			# only add project to appropriate client id from token
			if Project.query.filter_by(user_id=client_id,name=project_name).first() is None:
				new_project = Project(user_id=user.id,name=project_name)
				db.session.add(new_project)
				try:
					db.session.commit()
				except sqlalchemy.exc.SQLAlchemyError as e:
					print(e)
					error = 'Cannot register project'
					return make_response(render_template('/projects',title='Projects',error=error))
				
				# return new list of projects
				projects = Project.query.filter_by(user_id=user.id).all()
				response = make_response(render_template('projects.html',title=user.username,username=user.username,projects=projects))
				return response
			else:
				error = 'Project name already in use'
				return make_response(render_template('projects.html',title='Projects',error=error))
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response

# Displays all Project files
@app.route('/projects/<int:project_id>',methods=["GET"])
@protected_endpoint
def single_project(auth,project_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		if Project.query.filter_by(id=project_id,user_id=client_id).first() is not None:
			project = Project.query.filter_by(id=project_id,user_id=client_id).first() 
			files = Files.query.filter_by(project_id=project_id).all()		
			response = make_response(render_template('files.html',title=project.name,project=project,files=files))
			return response
		else:
			error = 'Client not authorized to view project'
			return make_response(render_template('projects.html',title='Projects',error=error))
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response	

# Delete Project
@app.route('/projects/delete/<int:project_id>',methods=["GET"])
@protected_endpoint
def delete_project(auth,project_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		if Project.query.filter_by(id=project_id,user_id=client_id):
			
			# remove project
			Project.query.filter_by(id=project_id).delete()
			try:
				db.session.commit()
			except:
				error = 'Cannot Delete Project'
				return make_response(render_template('edit.html',title='Projects',error=error,project=''))

			response = make_response(redirect('/projects'))
			return response
		else:
			error = 'Error: Cannot add to project not owned by client'
			response =  make_response(render_template('files.html',title='Projects',error=error))
			return response
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response		

# Adds file to DB
@app.route('/files/<int:project_id>',methods=["POST"])
@protected_endpoint
def add_file(auth,project_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		file_name = request.form.get('file_name')
		file_content = request.form.get('file_content')
		# project_id = request.form.get('project_id')	# hidden field, use URL instead
		 
		# user owns project
		if Project.query.filter_by(id=project_id,user_id=client_id):

			# check if filename is free
			if Files.query.filter_by(project_id=project_id,name=file_name).first() is None:
				timestamp = datetime.datetime.now()
				new_file = Files(project_id=project_id,name=file_name,timestamp=timestamp,content=file_content)
				db.session.add(new_file)
				try:
					db.session.commit()
				except:
					error = 'Cannot register file'
					return make_response(render_template('files.html',title='Projects',error=error,project=''))

				# show update
				files = Files.query.filter_by(project_id=project_id).all()
				project = Project.query.filter_by(id=project_id).first()
				response = make_response(render_template('files.html',title=project.name,files=files,project=project))
				return response
			else:
				error = 'File name already in use'
				return make_response(render_template('files.html',title='Projects',error=error))
		else:
			error = 'Error: Cannot add to project not owned by client'
			return make_response(render_template('files.html',title='Projects',error=error))
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response		

# Edit file
@app.route('/projects/<int:project_id>/<int:file_id>',methods=["GET"])
@protected_endpoint
def edit_file(auth,project_id,file_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']

		# does client own file
		if Project.query.filter_by(id=project_id,user_id=client_id):
			files = Files.query.filter_by(project_id=project_id).all()
			edit_file = {}
			for f in range(len(files)):
				if files[f].id == file_id:
					edit_file = files[f]
			project = Project.query.filter_by(id=project_id).first()
			response = make_response(render_template('edit.html',title='Edit File',project=project,files=files,edit_file=edit_file))
			return response
		else:
			error = 'Error: Cannot add to project not owned by client'
			response =  make_response(render_template('files.html',title='Projects',error=error))
			return response
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response		

# Update file
@app.route('/files/update/<int:project_id>/<int:file_id>',methods=["POST"])
@protected_endpoint
def update_file(auth,project_id,file_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		file_name = request.form.get('file_name')
		file_content = request.form.get('file_content')

		# does client own file
		if Project.query.filter_by(id=project_id,user_id=client_id):
			# update file
			update_file = Files.query.filter_by(id=file_id).first()
			update_file.name = file_name
			update_file.content = file_content
			update_file.timestamp = datetime.datetime.now()

			try:
				db.session.commit()
			except:
				error = 'Cannot Update File'
				return make_response(render_template('edit.html',title='Projects',error=error,project=''))

			response = make_response(redirect('/projects/'+str(project_id)+'/'+str(file_id)))
			return response
		else:
			error = 'Error: Cannot add to project not owned by client'
			response =  make_response(render_template('files.html',title='Projects',error=error))
			return response
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response		

# Delete File
@app.route('/files/delete/<int:project_id>/<int:file_id>',methods=["GET"])
@protected_endpoint
def delete_file(auth,project_id,file_id):
	if 'payload' in auth:
		client_id = auth['payload']['sub']

		#does client own file
		if Project.query.filter_by(id=project_id,user_id=client_id):
			# delete file 
			Files.query.filter_by(id=file_id).delete()

			try:
				db.session.commit()
			except:
				error = 'Cannot Delete File'
				return make_response(render_template('edit.html',title='Projects',error=error,project=''))

			files = Files.query.filter_by(project_id=project_id).all()
			project = Project.query.filter_by(id=project_id).first()
			response = make_response(redirect('/projects/'+str(project_id)))
			return response
		else:
			error = 'Error: Cannot add to project not owned by client'
			response =  make_response(render_template('files.html',title='Projects',error=error))
			return response
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response		

# Authentication endpoint - not used - token given at login
# https://medium.com/@riken.mehta/full-stack-tutorial-3-flask-jwt-e759d2ee5727
# https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
@app.route("/oauth",methods=["POST"])
def oauth():
	if request.method == 'POST' and request.form:
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()
		hashed_password = user.password

		if user and bcrypt.checkpw(password.encode('utf-8'),hashed_password):		
			# give user new token
			auth_token = encode_auth_token(user.id)				
			return jsonify({'token':auth_token.decode('ascii')}),200
	else:
		return render_template('homepage.html',title='NO AUTH')

@app.errorhandler(404)
def page_not_found(e):
	response = make_response(render_template('404.html'))
	response.status_code = 404
	return response

@app.errorhandler(500)
def internal_error(e):
	response = make_response(render_template('error.html',error="500 Internal Server Error"))
	response.status_code = 500
	return response