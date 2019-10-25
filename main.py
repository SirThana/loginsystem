from werkzeug import *
import pymysql
import time
from flask import *
from flask_wtf import *
import pdb

#TODO
#   1.  Clean up the code, remove uneccesary functions


#Default variables
app = Flask(__name__, static_folder="static")


#   --> return a database connection
def initConnection(user, password, db):
    try:
        dbconnection = pymysql.connect("localhost",user,password,db)
        return dbconnection
    except Exception as e:
        print(e)
        return False


def selectQuery(userName):
    dbconnection = initConnection('db1', 'password', 'db')
    query = "SELECT * FROM Users WHERE {}=\'{}'"
    field = 'FirstName'
    query = query.format(field,userName)
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return str(result)

    except Exception as e:
        print(e)


#   --> Generic queries, don't use this function
def queryDB(dbconnection, query):
    #Insert queries
    if query[:6] == "INSERT":
        try:
            with dbconnection.cursor() as cursor:
                cursor.execute(query)
                query = cursor.fetchone()
                dbconnection.commit()
                return query
        except Exception as e:
            print(e)
            return False


    else:
        try:
            with dbconnection.cursor() as cursor:
                cursor.execute(query)
                query = cursor.fetchall()
                return query;
        except Exception as e:
            print(e)
            return False

@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.method == "POST":
        query = request.form #query returns a multiDict, with a key of projectFilepath
        x = selectQuery(query['projectFilepath']) #Calling for the object at ^^^^^^^^ 
        x = x.strip()
        return render_template('handler.html', name='Handler', data=x)
    else: 
        return None



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name='Home')

def main():
    
    app.run(host='192.168.1.11', debug=True)

main()
