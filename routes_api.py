from routes import app

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