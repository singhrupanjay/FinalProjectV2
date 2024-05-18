from flask import Flask
from flask_pymongo import MongoClient
from flask import render_template
from flask import request

import os
import pprint


connection_string = f"mongodb+srv://Admin:jobmanchpassword130524@jobmanchcluster.vittg4t.mongodb.net/?retryWrites=true&w=majority&appName=JobManchCluster"
client = MongoClient(connection_string)

dbs = client.list_database_names()
print(dbs)

test_db = client.ProjectJobManch


def insert_job_data():
    collection = test_db.Jobdata
    test_document = {
        "name" : "first"
    }

    inserted_id = collection.insert_one(test_document)
    print(inserted_id)

# insert_job_data()


#CREATING DATABASE user_data
user_data = client.user_data

#CREATING COLLECTION user_collection 
user_collection = user_data.user_collection

#INSERT DOCUMENT
def create_documents():
    first_name = ["jonh", "Raj", "Tim", "Seline" ]
    last_name = ["doe", "sharma", "templeton", "kyle" ]

    docs = []

    for first_name, last_name in zip(first_name,last_name):
        doc = {"first_name" : first_name, "last_name":last_name}
        docs.append(doc)

    user_collection.insert_many(docs)

#CALLING FUNCTION TO INSERT User Data
# create_documents()

#USING PRETTYPRINT TO GET A CUSTOMIZED AND CLEAN OUTPUT 
printer = pprint.PrettyPrinter()

def display_UserData():
    users = user_collection.find() #.find() method to find all the data in the user_data collection

    for user in users:
        printer.pprint(user)

# display_UserData()

#SEARCH FOR A SPECIFIC DATA IN DATABASE
def find_data():
    data = user_collection.find({"first_name":"jonh"})
    printer.pprint(list(data))

# find_data()

#UPDATING DATA
def updateDataById(user_id):
    from bson.objectid import ObjectId #importing id of user object
    _id = ObjectId(user_id)

    # allUpdates = {
    #     "$set": {"new_field":True}, #adding new field
    #     "$set": {"salary":"$4000"}, #adding new field
    #     "$inc":{"age":0.5}, # to increase age by 1 we use 0.5
    #     "$rename":{"first_name":"first", "last_name":"last"} #changing field name 
    # }

    # user_collection.update_one({"_id":_id}, allUpdates)

    #REMOVE FIELD OR DATA FROM COLLECTION
    user_collection.update_one({"_id":_id},{"$unset": {"age":""}})


# updateDataById("664729fca6ad3f4688e6d424")



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

### DISPLAYING TEST DATA
@app.route('/display')
def display_data():
    data = user_collection.find({})  # Fetch all documents from the collection
    return render_template('test.html', data=data)

### TAKING TEST INPUT AND STORING ON MONGODB
@app.route("/login", methods=["GET", "POST"])
def logging():
    if request.method == "POST":
        # Get data from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Insert data into MongoDB
        user_collection.insert_one({"email": email, "password": password})
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)

