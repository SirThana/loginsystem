from werkzeug import *
import pymysql
import time
from flask import *
from flask_wtf import *
import pdb

#TODO
#   1.  Clean up the code, remove uneccesary functions
#   2.  Make selectQuery returnn a dict instead, easier to parse data from that over a string

#REMINDER
#   I left off at retrieving username and password from the fields, right now
#   i can get those values, when i read this, i should probably make some logic
#   that checks if the input of the user exists in the database, if so
#   check_hash_somethingsomething password against that of the database,
#   if both hashes are the same, we shouldd probably write a cookie to the user
#   after that we can let the user retrieve some data from the database and check
#   the cookie against the one held in memory, if they're the same, allow the user
#   to retrieve his data from the database << something like this, figure it out tomorrow def_handl

#Flask variables
app = Flask(__name__, static_folder="static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#   --> return a database connection
def initConnection(user, password, db):
    try:
        dbconnection = pymysql.connect("localhost",user,password,db)
        return dbconnection
    except Exception as e:
        print(e)
        return False

#   --> find a value in a field, in the fixed table Users return the result as a str
def selectQuery(value, field):
    dbconnection = initConnection('db1', 'password', 'db')
    query = "SELECT * FROM Users WHERE {}=\'{}'"
    query = query.format(field,value)
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return str(result) #make this return some kinda dict maybe ??

    except Exception as e:
        print(e)


#   --> Generic queries, don't use this function || It's crap
def queryDB(dbconnection, query):
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute(query)
            query = cursor.fetchone()
            dbconnection.commit()
            return query
    except Exception as e:
        print(e)
        return False


@app.route("/cookies")
def cookies(ID):
    res = make_response(render_template("/index.html")) #preset, so we can mutate it and return
    #res.set_cookie("flavor", "Chocolate chip", max_age=10, expires=None, path=request.path,
            #domain=None, secure=False, httponly=False,  samesite=False)

    res.set_cookie("ID", ID) #cookies are like dicts
    cookie = request.cookies #retrieve all cookies from user
    print(cookie.get("ID")) #Get the cookie with a key of ID (cookies are dicts)
    return res


@app.route('/handle_data', methods=['POST'])
def handle_data():
    #Retrieve values from forms here
    input = request.form #input from any form, as multi dict (key query for value)
    username = selectQuery(input['username'], "Firstname") #query username in the field Firstname
    passwordHash = generate_password_hash(input['password'])
    print("\n\n",username, password)

    if input['username'] == username:
        x = 5 # << this would be a select query 
        return cookies(str(x)) #You can return cookie functionality without routing there!
    if input["username"] == 'None': #<< write logic if a query returns False || None
        flash('Bad Credentials')
        return redirect("/")
    else:
        return render_template('index.html', name='Home')


#   --> Home route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name='Home')

def main():
    
    app.run(host='192.168.1.11', debug=True)

main()
