from werkzeug import *
from flask import *
import pymysql
import random
#-----------------
import time
import pdb

#TODO
#   1.  Clean up the code, remove uneccesary functions
#   2.  Make selectQuery returnn a dict instead, easier to parse data from that over a string |Done


#UPTOSPEED
#   I can now authenticate users, when they logged in succesfully, i write a cookie to their
#   web-storage, and to my database, i should write some logic that, after every action
#   that requires authentication (maybe looking up data in the database specific to a user)
#   read the cookie from the web-storage, read the cookie that matches web-storage[50] in my
#   database, if they both match, the user has proved itself in this websession to be who he says
#   he is. so look at he web-cookie[50], join that id with whatever data he wants to retrieve
#   from some abritrary data table with synchronised ID's || already proved that individual users
#   logging in, get different cookies, stored at their Users table

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
            result = cursor.fetchone() #returns a tuple, iterable much like a list
            return result

    except Exception as e:
        print(e)

#   --> Generate a string 255 characters long consisting of numbers between 0 and 9
#       at the 50th char, embeds the ID of the authenticated user, returns said cookie as string
def generateCookie(KEY):
    cookie = ""
    #random VALUE generator
    for i in range(1, 256):
        n = int(random.random()*10-1)
        cookie += str(n)

    #embed the ID of the user inside the cookie at the 50th char
    l = list(cookie)
    l[50] = str(KEY)
    cookie = "".join(l)
    return cookie

#   --> takes a database connection and a cookie, returns True if it worked out, False otherwise
#       Remember, cookies embed their user-ID at the 50th char, hence we don't need to tell
#       this function, for whom to store this cookie
def storeCookie(dbconnection, cookie):
    try:
        with dbconnection.cursor() as cursor:
            query = "UPDATE Users set Cookie=\'{}' WHERE ID=\'{}'"
            query = query.format(cookie, cookie[50]) #Write a cookie, for the user with ID of [50]
            cursor.execute(query)
            query = cursor.fetchone()
            dbconnection.commit()
            return True
    except Exception as e:
        print(e)
        return False

#   --> Takes a KEY and VALUE to store as cookie on the users-browser
#       Returns the cookie it stored in the user-browser
#       Useful because we can keep this cookie in memory and compare it every time against theirs
@app.route("/cookies")
def cookies(KEY, VALUE):
    res = make_response(render_template("index.html")) #preset, so we can mutate it and return
    #res.set_cookie("flavor", "Chocolate chip", max_age=10, expires=None, path=request.path,
            #domain=None, secure=False, httponly=False,  samesite=False)

    res.set_cookie(KEY, VALUE) #Set the cookie in the users browser
    cookie = request.cookies #retrieve all cookies from user
    return res, cookie


@app.route('/handle_data', methods=['POST'])
def handle_data():
    #input holds a |username| and |password| value, grab them as keys (input['username'])
    input = request.form 
    credentials = selectQuery(input['username'], "Firstname") #if exists, holds credentials

    #Logic to authenticate a User through firstname | passwordHash
    if credentials != None:
        if check_password_hash(credentials[6], input['password']) == True:
            cookie = generateCookie(credentials[0]) #Generate cookie, ID embedded
            dbconnection = initConnection('db1', 'password', 'db')
            x = storeCookie(dbconnection, cookie)
            print("\n\n\n",x)
            return cookies("ID",cookie) #You can return cookie functionality without routing there!
        else:
            flash('Bad Credentials')
            return redirect("/")

    elif credentials == None:
        flash('Bad Credentials')
        return redirect("/")


#   --> Home route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name='Home')

#   --> Main, run the application in debug mode
def main():
    app.run(host='192.168.1.11', debug=True)
main()
