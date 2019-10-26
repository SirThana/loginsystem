from werkzeug import *
import pymysql
import time
from flask import *
from flask_wtf import *
import pdb

#TODO
#   1.  Clean up the code, remove uneccesary functions


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
            return str(result)

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
    res = make_response(render_template("/index.html"))
    #res.set_cookie("flavor", "Chocolate chip", max_age=10, expires=None, path=request.path,
            #domain=None, secure=False, httponly=False,  samesite=False)

    res.set_cookie("ID", ID)
    cookie = request.cookies #retrieve all cookies from user
    print("\n\n\n", "||||||||")
    print(cookie.get("ID")) #Get the cookie with a key of ID (cookies are dicts)
    print(" ||||||||")
    return res


@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.method == "POST":
        input = request.form #input from any form, as multi dict (key query for value)
        if input["query"] == "Test":
            x = 5 # << this would be a select query 
            return cookies(str(x)) #You can return cookie functionality without routing there!
        if input["query"] == '': #<< write logic if a query returns False || None
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
