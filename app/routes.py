from flask import render_template, url_for, flash, redirect, request, send_file,session
from app import app,mysql
from passlib.hash import sha256_crypt
import bcrypt

# # Function to run SQL commands from config.sql
# def run_sql_file(filename):
#     with open(filename, 'r') as file:
#         commands = file.read().split(';')
# # Create a MySQL cursor
#         cur = mysql.connection.cursor()
#     for command in commands:
#         try:
#             if command.strip() != '':
#                 cur.execute(command)
#         except Exception as e:
#             # Check if the table exists before running the command
#             if "Table 'your_database.table_name' doesn't exist" in str(e):
#                 continue  # Skip the command if the table doesn't exist
#             else:
#                 print(f"Error executing SQL command: {e}")

 

# Load the database schema from config.sql
#run_sql_file('app/dbConfig.sql')

@app.route("/")
def index():
    return render_template("index.html")

#Routes for Login Page
@app.route("/login",methods=["GET", "POST"])
def login():
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

     # Create a MySQL cursor
        cur = mysql.connection.cursor()

    # Execute the query to find the user by email
        # Query the database for the user
        query_user = "SELECT email,_password,firstname FROM users WHERE email = %s"
        cur.execute(query_user, (email,))
        query_user = cur.fetchone()
        

        query_company = "SELECT email,_password,comp_name FROM company WHERE email = %s"
        cur.execute(query_company, (email,))
        query_company = cur.fetchone()

        if query_user:
            session['firstname'] = query_user['firstname']
            return redirect('/onBoard')  # Redirect to the Home page after successful login
        elif query_company:
             session['comp'] = query_company['comp_name']
             return redirect('/company')  # Redirect to the Company page after successful login
        else:
            error_msg = "Invalid credentials. Please try again."
            return render_template('login.html', error_msg=error_msg)
   else:
        #return "Invalid credentials. Please try again."
    return render_template('login.html')

#Routes for Register Page
@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    if request.method == 'POST':
        # Get form data
        FirstName = request.form['firstname']
        LastName = request.form['lastname']
        Email = request.form['email']
        Password = request.form['password']
        PhoneNumber = request.form['phoneNo']
        Location = request.form['location']
        Skills = request.form['skills']
        WorkPermit = request.form['workPermit']
        Sin = request.form['sin']
        Availability = request.form['availability']
        RegDate = request.form['regDate']
        # Hash the password
        hashed_password = sha256_crypt.hash(Password)

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Insert the user into the database
        cur.execute("INSERT INTO users (firstName,lastName,email,_password,phone_number,_location,skills,workPermitNumber,SIN,_availability,registration_date) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s, %s,%s)", (FirstName, LastName,Email, hashed_password,PhoneNumber,Location,Skills,WorkPermit,Sin,Availability,RegDate))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the login page or any other page you want
        return redirect(url_for('login'))

    return render_template('registerUser.html')  # Assuming you have a 'register.html' template

#Routes for Register Company Page
@app.route('/registerCompany', methods=['GET', 'POST'])
def registerCompany():
    if request.method == 'POST':
        # Get form data
        CompanyName = request.form['compname']
        Email = request.form['email']
        Password = request.form['password']
        PhoneNumber = request.form['phoneNo']
        Location = request.form['location']
        Industry = request.form['industry']
        Description = request.form['location']
        RegDate = request.form['regDate']

        # Hash the password
        hashed_password = sha256_crypt.hash(Password)

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Insert the user into the database
        cur.execute("INSERT INTO company (comp_name, email, _password,phone_number,_location,industry,_description,registration_date) VALUES (%s, %s, %s,%s,%s, %s, %s,%s)", (CompanyName,Email,hashed_password,PhoneNumber,Location,Industry,Description,RegDate))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the login page or any other page you want
        return redirect(url_for('login'))

    return render_template('registerCompany.html')  # Assuming you have a 'register.html' template



@app.route("/onBoard")
def onBoard():
    #jobs = Jobs.query.all()
    return render_template('onBoard.html')

@app.route("/company")
def company():
    return render_template("company.html")

#Routes for Register Company Page
# @app.route('/addShift', methods=['GET'])
# def addShift():
#     if request.method == 'GET':
#         cur = mysql.connection.cursor()

#         query_companies = "select companyId,comp_name from company;"
#         cur.execute(query_companies)
#         shift_data = cur.fetchone()

#     return render_template('addShift.html', shifts=shift_data)


#Routes for Register Company Page
@app.route('/addShift', methods=['GET', 'POST'])
def addShift():
    if request.method == 'GET':
        cur = mysql.connection.cursor()

        query_companies = "SELECT companyId, comp_name FROM company;"
        cur.execute(query_companies)
        shift_data = cur.fetchall()

        return render_template('addShift.html', shifts=shift_data)
    
    elif request.method == 'POST':
        # Get form data
        companyId = request.form['company']
        shift_date = request.form['shiftdate']
        shift_type = request.form['shifttype']
        start_time = request.form['starttime']
        end_time = request.form['endtime']
        department_name = request.form['departmentname']
        supervisor_name = request.form['supervisorname']
        num_workers = request.form['noOfWorkers']
        notes = request.form['notes']

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Insert the shift into the database
        query_insert_shift = "INSERT INTO company_shifts (companyId, shift_date, shift_type, start_time, end_time, department_name, supervisor_name, num_workers, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (companyId, shift_date, shift_type, start_time, end_time, department_name, supervisor_name, num_workers, notes)
        cur.execute(query_insert_shift, values)

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the company page or any other page you want
        return redirect(url_for('company'))

    # Handle other cases or display error page if needed
    return render_template('addShift.html')

# for all shifts
@app.route('/shifts', methods=['GET'])
def allShifts():
    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch all shifts from the database
    query_all_shifts = "SELECT * FROM company_shifts;"
    cur.execute(query_all_shifts)
    shift_data = cur.fetchall()

    print(shift_data)

    # Close the cursor
    cur.close()

    # Render the template and pass the shifts data to it
    return render_template('shifts.html',shifts=shift_data)




