from werkzeug import *
from flask import *
import pymysql
import random
import time
#-----------------

#TODO
#   1.  Clean up the code, remove uneccesary functions
#   2.  Make selectQuery returnn a dict instead, easier to parse data from that over a string |Done

#UPTOSPEED
#   Code up a download function, that downloads something if a user is authenticated
#   Just a prove of concept, so i can extend on this later

#Flask variables
app = Flask(__name__, static_folder="static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/downloadFile', methods=['POST'])
def downloadFile():
    x = authenticateUser()
    print(x)
    if x[1] == True:
        path = "./supersecretdata.txt"
        return send_file(path, as_attachment=True)
    else:
        return redirect("/")


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
#       if expire is set to 0, set a cookie to expire immediately, anything other than 0, session
@app.route("/cookies")
def writeCookie(KEY, VALUE):
    res = make_response(redirect("/"))
    res.set_cookie(str(KEY), VALUE) #Set the cookie in the users browser
    return res #Route back to the home page


#   --> Authenticate a user by comparing their cookie, against the one in the database.
#       If they match, return True, and their ID. We can use the ID to find any other data that
#       Belongs to the user
def authenticateUser():
    try: #On first sessions, cookie isn't stored yet, catch exceptions
        remoteCookie = request.cookies
        dbCookie = selectQuery('ID', remoteCookie['ID'][50]) #select * from Users ID == cookie[50]
    except Exception as e:
        return "Not Logged in", False #Don't ask, don't tell
    
    #dbCookie = selectQuery('ID', remoteCookie['ID'][50])
    if remoteCookie['ID'] == dbCookie[5]: #Compare remote to db cookie
        print("AUTHENTICATED USER AT: ", time.time(), " || ", remoteCookie['ID'][50] )
        credentials = selectQuery("ID", remoteCookie['ID'][50])
        returnMe = "Logged in as: {} {}".format(credentials[1], credentials[2])
        return returnMe, True
    
    return "Not Logged in", False #Don't ask, don't tell
    

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
            storeCookie(dbconnection, cookie)
            return writeCookie("ID",cookie) #write cookie, without routing
        else:
            flash('Bad Credentials')
            return redirect("/")

    else:
        flash('Bad Credentials')
        return redirect("/")

@app.route('/logout', methods=['POST'])
def logout():
    response = Response()
    response.delete_cookie("ID"), render_template('index.html', name='Home')
    return response


#   --> Home route
@app.route('/')
@app.route('/index')
def index():
    state = authenticateUser()
    flash(state[0])
    return render_template('index.html', name='Home')

#   --> Main, run the application in debug mode
def main():

    app.run(host='192.168.1.11', debug=True)


main()
