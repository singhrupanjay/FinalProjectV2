from flask import Flask
from flask_pymongo import MongoClient
# from flask_pymongo import PyMongo
from flask import render_template
from flask import request, redirect, url_for, session
import pprint

app = Flask(__name__)

connection_string = f"mongodb+srv://Admin:jobmanchpassword130524@jobmanchcluster.vittg4t.mongodb.net/?retryWrites=true&w=majority&appName=JobManchCluster"
client = MongoClient(connection_string)


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


#DASHBOARD
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

#DASHBOARD
#INSERT DOCUMENT jobDetails
def create_jobdetails_documents():
    # Role = ["SDE1", "Analyst", "Devops", "UI/UX" ]
    # location = ["Surat", "Delhi", "Singapore", "Minnesotta" ]

    Company  = ["Amazon", "facebook", "Flipkart", "Google", "Netflix", "Nike","coco-cola", "Uber", "Instagram", "Tata", "Linkedin", "Twitter"]
    Uploaded  = ["2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago","2 days ago" ]
    JobRole = ["senior web developer","SDE1", "Graphic designer", "software engineer", "software engineer", "Graduate Trainee",
                "Back end developer", "Front end developer", "Fullstack developer", "SOC analyst", "PHP developer", "Business Analys"]
    Location  = [ "hyderabad, india"," pune, india"," hyderabad, india"," bengaluru, india", "hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"," hyderabad, india"] 
    Salary  = [ "10k - 20k","20k - 30k","30k - 40k","40k - 50k","50k - 60k","60k - 70k","70k - 80k","80k - 90k","90k - 100k","16k - 50k","10k - 20k","10k - 20k"  ]
    JobType = [ "part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time","part-time" ]
    Shift  = [ "day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift","day-shift" ]
    experience  = [ "0-1 yr","0-3 yr","2 yr","3yr","freshers","freshers","0-1yr","2 yr","3 yr","1 yr","1-2 yr","freshers" ]


    docs = []

    for Company,Uploaded ,JobRole, Location, Salary ,JobType, Shift, experience in zip(Company,Uploaded ,JobRole, Location, Salary ,JobType, Shift):
        doc = {"company" : Company, "date_uploaded" : Uploaded, "job_role" : JobRole, "job_location":Location, "salary": Salary, "job_type":JobType, "working_shift":Shift, "Experience":experience }
        docs.append(doc)

    jobDetails.insert_many(docs)

#DASHBOARD
#CALLING FUNCTION TO INSERT User Data
# create_jobdetails_documents()



# USING PRETTYPRINT TO GET A CUSTOMIZED AND CLEAN OUTPUT 
# printer = pprint.PrettyPrinter()


# def display_UserData():
#     users = jobDetails.find() #.find() method to find all the data in the user_data collection

#     for user in users:
#         printer.pprint(user)
# display_UserData()



#DASHBOARD
# SEARCH FOR A SPECIFIC DATA IN DATABASE
# def find_data():
#     data = jobDetails.find()
    # printer.pprint(list(data))

# find_data()



#DASHBOARD
#UPDATING DATA
# def updateDataById(user_id):
#     from bson.objectid import ObjectId #importing id of user object
#     _id = ObjectId(user_id)

    # allUpdates = {
    # #     "$set": {"new_field":True}, #adding new field
    #     "$set": {"experience":"0-1 yr","experience":"0-3 yr","experience":"2 yr","experience":"3yr","experience":"freshers","experience":"freshers","experience":"0-1yr","experience":"2 yr","experience":"3 yr","experience":"1 yr","experience":"1-2 yr","experience":"freshers"} #adding new field
    #     "$inc":{"age":0.5}, # to increase age by 1 we use 0.5
    #     "$rename":{"first_name":"first", "last_name":"last"} #changing field name 
    # }

    # user_collection.update_one({"_id":_id}, allUpdates)

    #REMOVE FIELD OR DATA FROM COLLECTION
    # user_collection.update_one({"_id":_id},{"$unset": {"age":""}})


# updateDataById("664729fca6ad3f4688e6d424")



#DASHBOARD
#DELETING DOCUMENTS if a particular field exisits

# def delete_method():
    # from bson.objectid import ObjectId #importing id of user object
    # item_id = ObjectId(_id)
    # _id = "_id"
#     jobDetails.delete_many({"_id":_id})
    # jobDetails.delete_many({_id:{'$exists':True}})
# delete_method("664ac557970500d9e284c9b0")
    # field_name = "Job_Role"
    # jobDetails.delete_many({field_name: {'$exists': True}})
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


@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

#Job-Detail Page
@app.route('/jobDetail')
def JobDetail():
    job_details = jobDetails.find()

    job_list = []
    for job in job_details:
        job_list.append({
            'role': job.get('job_role'),
            'company': job.get('company'),
            'location': job.get('job_location'),
            'salary': job.get('salary')
        })

    job_list=job_list

    return render_template('job-detail.html', job_list = job_list)

#profile Page
@app.route('/profile')
def profile():
    return render_template('profile.html', name = name, email = email)

@app.route('/loginsuccess')
def Lsuccess():
    status = "Login"
    message = "Successfully Logged In!"
    option = ""
    return render_template('success.html',status = status, message = message,option = option)

@app.route('/fail')
def fail():
    status = "Registered"
    message = "Successfully Registered"
    option = "Register Again"
    return render_template('Fail.html', status = status, message = message, option = option)

@app.route('/registersuccess')
def Rsuccess():
    status = "Registration"
    message = "Successfully Registered!"
    option = "Register Again"
    return render_template('success.html', status = status, message = message, option = option)

### DISPLAYING TEST DATA
@app.route('/display')
def display_data():
    jobData = jobDetails.find()  # Fetch all documents from the collection

    return render_template('AllJobs.html', data=jobData, count = 0)



### TAKING TEST INPUT AND STORING ON MONGODB in register
@app.route("/register", methods=["GET", "POST"])
def register():
    # global entered_data
    if request.method == "POST":
        # Get data from the form
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("pass")
 
        if name or email or password:
            # Insert data into MongoDB
            user_credentials.insert_one({"name": name, "email": email, "password": password })
            return redirect('/registersuccess')
        else:
            return render_template('register.html')


    return render_template('register.html')

global name
global email

### USER AUTHENTICATION in login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists in MongoDB
        user1 = user_data.user_credentials.find_one({'email': email, 'password': password})

        if user1:
            return redirect("/loginsuccess")
        else:
            return redirect("/fail")

    return render_template('login.html')


app.secret_key = "lorem"
if __name__ == '__main__':
    app.run(debug=True)

