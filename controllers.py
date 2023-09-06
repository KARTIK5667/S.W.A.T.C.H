from flask import render_template, request, url_for, redirect, session, jsonify
from models import MongoDB

# Establish database connections
docnurse_records = MongoDB().register_docnurse
patientrecords = MongoDB().register_patient

def edit_patient():
    message = ''
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        user = request.form.get("fullname")
        currUserID = request.form.get("curruserid")
        user_type = "Patient"
        newUserID = request.form.get("newuserid")

        # Check if currUserID exists in the database
        curruserid_found = patientrecords.find_one({"userID": currUserID})
        if not curruserid_found:
            message = 'This CurrUserID does not exist in the database'
            return render_template('editpatient.html', message=message)

        # Check if newUserID already exists in the database
        newuserid_found = patientrecords.find_one({"userID": newUserID})
        if newuserid_found:
            message = 'This UserID already exists in the database'
            return render_template('editpatient.html', message=message)

        # Check if currUserID and newUserID are the same
        if currUserID == newUserID:
            message = 'Same UserID selected!'
            return render_template('editpatient.html', message=message)

        # Update the userID for the patient
        patientrecords.update_one({"userID": currUserID}, {"$set": {"userID": newUserID}})

        return "Edit Done!"

    return render_template('editpatient.html', email=email)

def register_patient():
    message = ''
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        user = request.form.get("fullname")
        age = request.form.get("age")
        user_type = "Patient"
        userID = request.form.get("userID")

        # Check if user already exists in the database
        user_found = patientrecords.find_one({"name": user})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('addpatient.html', message=message)

        # Check if userID already exists in the database
        userID_found = patientrecords.find_one({"userID": userID})
        if userID_found:
            message = 'This userID already exists in the database'
            return render_template('addpatient.html', message=message)

        # Create a new patient record
        user_input = {'name': user, 'userID': userID, 'age': age, 'user_type': user_type, 'data': []}
        patientrecords.insert_one(user_input)

        return "Added Patient Successfully"

    return render_template('addpatient.html', email=email)

def register_user():
    message = 'Please register for an account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        user_type = "Doctor/Nurse"
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if user already exists in the database
        user_found = docnurse_records.find_one({"name": user})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)

        # Check if email already exists in the database
        email_found = docnurse_records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in the database'
            return render_template('register.html', message=message)

        # Check if passwords match
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)

        # Hash the password
        hashed_password = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

        # Create a new user record
        user_input = {'name': user, 'email': email, 'user_type': user_type, 'password': hashed_password}
        docnurse_records.insert_one(user_input)

        return redirect(url_for("login"))

    return render_template('register.html', message=message)

def login_user():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if email exists in the database
        email_found = docnurse_records.find_one({"email": email})
        if email_found:
            # Check if the password matches the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), email_found['password']):
                session["email"] = email
                return redirect(url_for("logged_in"))
            else:
                message = 'Wrong password!'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found!'
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)

def logout_user():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

def get_data():
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("login"))

    if request.method == "GET":
        data = []
        for doc in patientrecords.find():
            data.append({'name': doc['name'], 'userID': doc['userID'], 'age': doc['age']})

        return jsonify(data)

def update_data():
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Update the data in the database as required
        return "Data updated successfully"

    return render_template('update.html', email=email)

def dashboard():
    if "email" in session:
        email = session["email"]  # Get the logged-in email from the session
    else:
        return redirect(url_for("login"))

    return render_template('dashboard.html', email=email)
