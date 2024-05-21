from flask import Flask
from flask_pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import render_template
from flask import request, redirect, url_for, flash
import os
import pprint

app = Flask(__name__)

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
#CREATING COLLECTION user_collection under DATABASE user_data
user_collection = user_data.user_collection
#CREATING COLLECTION USER_CREDENTIALS under DATABASE user_data
user_credentials = user_data.user_credentials


#CREATING DATABASE JobData
JobData = client.JobData
#CREATING COLLECTION jobDetails under DATABASE JobData
jobDetails = JobData.jobDetails


#INSERT DOCUMENT USERDATA
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

#INSERT DOCUMENT jobDetails
def create_jobdetails_documents():
    # Role = ["SDE1", "Analyst", "Devops", "UI/UX" ]
    # location = ["Surat", "Delhi", "Singapore", "Minnesotta" ]

    Company  = ["Amazon", "facebook", "Flipkart", "Google", "Netflix", "Nike","coco-cola", "Uber", "Instagram", "Tata", "Linkedin", "Twitter"]
    Uploaded  = ["2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago" ]
    JobRole = ["senior web developer","senior web developer", "Graphic designer", "software engineer", "software engineer", "senior web developer",
                "senior web developer", "senior web developer", "senior web developer", "senior web developer", "senior web developer", "senior web developer"]
    Location  = [ "hyderabad, india"," pune, india"," hyderabad, india"," bengaluru, india", "hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"] 
    Salary  = [ "10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k","10k - 20k"  ]
    JobType = [ "part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time" ]
    Shift  = [ "day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift" ]


    docs = []

    for Company,Uploaded ,JobRole, Location, Salary ,JobType, Shift in zip(Company,Uploaded ,JobRole, Location, Salary ,JobType, Shift):
        doc = {"company" : Company, "date_uploaded" : Uploaded, "job_role" : JobRole, "job_location":Location, "salary": Salary, "job_type":JobType, "working_shift":Shift }
        docs.append(doc)

    jobDetails.insert_many(docs)

#CALLING FUNCTION TO INSERT User Data
# create_jobdetails_documents()

#USING PRETTYPRINT TO GET A CUSTOMIZED AND CLEAN OUTPUT 
printer = pprint.PrettyPrinter()

def display_UserData():
    users = jobDetails.find() #.find() method to find all the data in the user_data collection

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


#DELETING DOCUMENTS
def delete_method():
#     from bson.objectid import ObjectId #importing id of user object
#     _id = ObjectId(item_id)
#     jobDetails.delete_many({"_id":_id})

# delete_method("664ac557970500d9e284c9b0")
    field_name = "Job_Role"
    jobDetails.delete_many({field_name: {'$exists': True}})
# delete_method()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


### DISPLAYING TEST DATA
@app.route('/display')
def display_data():
    jobData = jobDetails.find()  # Fetch all documents from the collection

    return render_template('test.html', data=jobData, count = 0)

### TAKING TEST INPUT AND STORING ON MONGODB in register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get data from the form
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Insert data into MongoDB
        user_credentials.insert_one({"name": name, "email": email, "password": password })
    return render_template('register.html')

### USER AUTHENTICATION in login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists in MongoDB
        user1 = user_data.user_credentials.find_one({'email': email, 'password': password})

        if user1:
            return redirect(url_for('jobs'))
            # return "<h1>Pass</h1>"
        else:
            flash('Invalid credentials. Please try again.', 'error')
            # return "<h1>Fail</h1>"

    return render_template('login.html')

app.secret_key = "lorem"


if __name__ == '__main__':
    app.run(debug=True)

