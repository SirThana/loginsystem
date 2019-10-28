from werkzeug import *
from flask import *
import pymysql
import random
import threading
#-----------------
import time
import pdb

#TODO
#   1.  Clean up the code, remove uneccesary functions
#   2.  Make selectQuery returnn a dict instead, easier to parse data from that over a string |Done


#UPTOSPEED
#   I can authenticate users by reading their cookies in the global session_variables
#   This was fun and all but really bad practice and has no use other then to look cool
#   Should probably write some logic where if a user wants to do an authenticated action,
#   check their cookie against the one in the database, if true >> gett their data
#   so basically recreate the authenticate function that is now retarded :-)



#Flask variables
app = Flask(__name__, static_folder="static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
global session_variables
session_variables = []

#   --> return a database connection
def initConnection(user, password, db):
    try:
        dbconnection = pymysql.connect("localhost",user,password,db)
        return dbconnection
    except Exception as e:
        print(e)
        return False

#   --> find a value in a field, in the fixed table Users return the result as a str
def selectQuery(field, value):
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
        n = int(random.random()*10-1) #fix this to be chars later
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
def writeCookie(KEY, VALUE):
    res = make_response(redirect("/"))
    #res.set_cookie("flavor", "Chocolate chip", max_age=10, expires=None, path=request.path,
            #domain=None, secure=False, httponly=False,  samesite=False)

    res.set_cookie(KEY, VALUE) #Set the cookie in the users browser
    #Write the cookie ID and VALUE to the session variables for thread to read
    session_variables.append(VALUE[50])
    session_variables.append(VALUE)
    return res #Route back to the home page


#   --> Reads the cookie that's stored in the session_variable, compares it to the one
#       in the database, if they match, user is authenticated
#       ||NOTE Not very secure, if the user deletes their cookie AKA logs out,
#       The session variable won't be updated, they'll be out of sync and this function
#       will still report AUTHENTICATED, could solve this by making a logout buttonn
#       That calls for a function to remove the values in session_variables
#       Reason for this workaround is the fact that threads can't access session based objects
#       Such as the cookie.requests
def authenticateUser():
    while True:
        if len(session_variables) > 0:
            dbresult = selectQuery("ID", session_variables[0])
            if session_variables[1] == dbresult[5]:
                print("AUTHENTICATED", time.time())
            time.sleep(3)
   

@app.route('/handle_data', methods=['POST'])
def handle_data():
    #input holds a |username| and |password| value, grab them as keys (input['username'])
    input = request.form
    credentials = selectQuery('Firstname', input['username']) #if exists, holds credentials

    #Logic to authenticate a User through firstname | passwordHash
    if credentials != None:
        if check_password_hash(credentials[6], input['password']) == True:
            cookie = generateCookie(credentials[0]) #Generate cookie, ID embedded
            dbconnection = initConnection('db1', 'password', 'db')
            x = storeCookie(dbconnection, cookie)
            return writeCookie("ID",cookie) #You can return cookie functionality without routing
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
    #   --> Runs authenticateUser in a thread in the background
    thread_Auth = threading.Thread(target=authenticateUser, args=())
    thread_Auth.daemon = True
    thread_Auth.start()


    app.run(host='192.168.1.11', debug=True)


main()
