from flask import Flask, render_template, request, url_for, redirect, session,jsonify
from pymongo import MongoClient
import bcrypt
#set app as a Flask instance 
app = Flask(__name__)
import datetime

#encryption relies on secret keys so they could be run
app.secret_key = "testing"
import json


# #connect to your Mongo DB database
def MongoDB():
    client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    db = client.get_database('SWATCH')
    return db
docnurse_records = MongoDB()
docnurse_records=docnurse_records.register_docnurse
patientrecords=MongoDB()
patientrecords=patientrecords.register_patient
@app.route("/editpatient", methods=['post', 'get'])
def edit_patients():
    message = ''
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        currUserID = request.form.get("curruserid")
        user_type="Patient"
        newUserID = request.form.get("newuserid")
        #if found in database showcase that it's found 
        user_found = patientrecords.find_one({"name": user})
        newuserid_found = patientrecords.find_one({"userID": newUserID})
        curruserid_found = patientrecords.find_one({"userID": currUserID})
        if not curruserid_found:
            message = 'This CurrUserID doesnt exists in database'
            return render_template('editpatient.html', message=message)
        if newuserid_found:
            message = 'This UserID already exists in database'
            return render_template('editpatient.html', message=message)
        if currUserID == newUserID:
            message = 'Same UserID selected!'
            return render_template('editpatient.html', message=message)
        else:
            patientrecords.update_one({"userID": currUserID}, {"$set": {"userID": newUserID}})

            return "Edit Done!"
    return render_template('editpatient.html',email=email)

@app.route("/addpatient", methods=['post', 'get'])
def add_patients():
    message = ''
    #if method post in index
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        age = request.form.get("age")
        user_type="Patient"
        userID = request.form.get("userID")
        #if found in database showcase that it's found 
        user_found = patientrecords.find_one({"name": user})
        userID_found = patientrecords.find_one({"userID": userID})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('addpatient.html', message=message)
        if userID_found:
            message = 'This userID already exists in database'
            return render_template('addpatient.html', message=message)
        else:
            #hash the password and encode it
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'userID': userID, 'age': age,'user_type':user_type,'data':[]}
            #insert it in the record collection
            patientrecords.insert_one(user_input)
            
            return "Added Patient Successfully"
    return render_template('addpatient.html',email=email)



#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        user_type="Doctor/Nurse"
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = docnurse_records.find_one({"name": user})
        email_found = docnurse_records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed,'user_type':user_type}
            #insert it in the record collection
            docnurse_records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = docnurse_records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        #check if email exists in database
        email_found = docnurse_records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    with open('data.json', 'r') as file:
        patients_data = json.load(file)
        return render_template('dashboard.html', patients=patients_data["patients_data"])

@app.route('/data', methods=['GET'])
def get_data():
    # if "email" in session:
    #     email = session["email"]
        with open('data.json', 'r') as file:
            patients_data = json.load(file)
            data=patients_data
            return jsonify(data)
    # else:
    #     return "Not logged in Nurse/Doctor account"
    

@app.route('/update_data', methods=['POST'])
def update_data():
    json_data = request.get_json()

    # Print and save the data as per your requirements
    print("########################NEW DATA#######################")
    print(json_data)

    # Extract the user data from json_data
    patient_data = json_data["patients_data"][0]
    currUserID = patient_data["userID"]
    data = patient_data["data"]
    userid_found = patientrecords.find_one({"userID": currUserID})
    if userid_found:
        patientrecords.update_one({"userID": currUserID}, {"$set": {"data": data}})
        print("---DATA UPDATED SUCCESFULLY IN DB---")
    else:
        print("---USER ID NOT FOUND IN DB---")
    # Update the data in data.json for the matching userID
    with open('data.json', 'r') as file:
        existing_data = json.load(file)

    for patient in existing_data["patients_data"]:
        if patient["userID"] == currUserID:
            patient["data"] = data
            print("---DATA UPDATED SUCCESSFULLY IN data.json---")
            break
    else:
        print("---USER ID NOT FOUND IN data.json---")

    # Save the updated data in data.json
    with open('data.json', 'w') as file:
        json.dump(existing_data, file)

    # Send a response indicating the success
    return 'Data received and saved successfully.'

    
if __name__ == "__main__":
#   chart.init_app(app)
  app.run(debug=True, host='0.0.0.0', port=5000)
