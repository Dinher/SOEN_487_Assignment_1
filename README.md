## SOEN 487 Assignment 1 
### Code Repository 
Code Repository is a simple web application which leverages RESTFUL stateless protocol and html forms to create a repository for files for programming projects.

#### Installation:
With the repository on the local system, activate a virtual environment 
```
c:/.../code_repositiory/
>> pip -m venv venv
>> cd venv/Scripts/
>> activate
```

Install the dependencies
```
c:/.../code_repository/
>>pip install -r requirements.txt
```

Run the application via python
`python main.py`

or by Flask
```
>>set FLASK_APP=main.py
>>flask run
```

#### Authentication
Given a logged in user and their user id, JWT will output a token which is given to the user as a cookie thus may be seen in the browser's cookies with a single key of :
```
{
	'token': 'some_random_characters'
}
```
This cookie is then given to the server upon each request to validate and maintain the user's session. The cookie has a duration of `10 minutes` before the server requires the user to log in.

#### Endpoints
Functional
- `/api/users/clearDatabase`
- `/api/projects/clearDatabase`
- `/api/files/clearDatabase`
- `/api/users` - JSON dump of User table
- `/api/projects` - JSON dump of Project table
- `/api/files` - JSON dump of Files table
- `/api/showDatabase` - JSON output of entire DB
- `/dumpDatabase` - prints database file
- `/showDatabase` - HTML database output

Routes
- `/`
- `/login`
- `/signup`
- `/logout`
- `/projects`
- `/projects/<id>`
- `/projects/delete/<proj_id>`
- `/projects/<proj_id>/<file_id>`
- `/files`
- `/files/delete/<proj_id>/<file_id>`
- `/files/update/<file_id>`

#### Reference and resources
1.https://stackoverflow.com/questions/34495632/how-to-implement-login-required-decorator-in-flask
2.https://steelkiwi.com/blog/jwt-authorization-python-part-1-practise/
3.https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
4.https://realpython.com/token-based-authentication-with-flask/
5.https://medium.com/@riken.mehta/full-stack-tutorial-3-flask-jwt-e759d2ee5727
6.https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
