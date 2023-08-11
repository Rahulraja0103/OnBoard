from flask import render_template, url_for, flash, redirect, request, send_file,session,jsonify
from app import app,mysql
from passlib.hash import sha256_crypt
import bcrypt
import datetime
from datetime import datetime

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

def insert_log(message):
    cur = mysql.connection.cursor()
    insert_query = "INSERT INTO logs (timestamp, message) VALUES (NOW(), %s)"
    cur.execute(insert_query, (message,))
    mysql.connection.commit()
    cur.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/companyTab")
def companyTab():
    return render_template("companyTab.html")

@app.route("/userTab")
def userTab():
    return render_template("userTab.html")

@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutUs.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

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
        query_user = "SELECT userId,email,_password,firstname FROM users WHERE email = %s"
        cur.execute(query_user, (email,))
        query_user = cur.fetchone()
        

        query_company = "SELECT email,_password,comp_name FROM company WHERE email = %s"
        cur.execute(query_company, (email,))
        query_company = cur.fetchone()

        if query_user:
                stored_password_hash = query_user['_password']  # Assuming the stored password hash is retrieved from the database
                provided_password = password  # Password provided during login

                if sha256_crypt.verify(provided_password, stored_password_hash):
                    session['firstname'] = query_user['firstname']
                    session['email'] = query_user['email']
                    session['userId'] = query_user['userId']
                    session['show_welcome_message'] = True  # Set the flag to show the welcome message
                    log_message = f"User {query_user['firstname']} logged in successfully"
                    insert_log(log_message)
                    return redirect('/onBoard')  # Redirect to the Home page after successful login
                else:
                    error_msg = "Invalid credentials. Please try again."
                    return render_template('login.html', error_msg=error_msg)

        elif query_company:
                stored_password_hash_comp = query_company['_password']  # Assuming the stored password hash is retrieved from the database
                provided_password_comp = password  # Password provided during login
                if sha256_crypt.verify(provided_password_comp, stored_password_hash_comp):
                    session['comp'] = query_company['comp_name']
                    session['email'] = query_company['email']
                    log_message = f"User {query_company['comp_name']} logged in successfully"
                    insert_log(log_message)
                    return redirect('/postedshifts')  # Redirect to the Company page after successful login
                else:
                    error_msg = "Invalid credentials. Please try again."
                    return render_template('login.html', error_msg=error_msg)
        else:
            error_msg = "Invalid credentials. Please try again."
            return render_template('login.html', error_msg=error_msg)
   else:
        #return "Invalid credentials. Please try again."
    return render_template('login.html')

#Routes for Register Page
@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    if request.method == 'GET':
        current_date = datetime.now().strftime('%Y-%m-%d') #Prashanth

        return render_template('registerUser.html', current_date=current_date)

    elif request.method == 'POST':
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

        query_exists_user = "SELECT email FROM users WHERE email = %s"
        cur.execute(query_exists_user, (Email,))
        exists_user = cur.fetchone()

        # cur.execute("SELECT * FROM users Where email = % s", (Email, ))
        # account = cur.fetchone()
        if exists_user:
            flash("Account already exists","warning")
            return redirect('registerUser')
        # elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$', Password):
        #     #  flash("Account already exists","warning")
        #      message = 'Passwords must have at least one letter, one number, and one special character. !'
        # elif not FirstName or not Password or not Email:
            #  flash("Account already exists","warning")
            # message = "please fill out the form !"
        else:

        # Insert the user into the database
            cur.execute("INSERT INTO users (firstName,lastName,email,_password,phone_number,_location,skills,workPermitNumber,SIN,_availability,registration_date) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s, %s,%s)", (FirstName, LastName,Email, hashed_password,PhoneNumber,Location,Skills,WorkPermit,Sin,Availability,RegDate))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the login page or any other page you want
        log_message = f"User {FirstName} registered successfully"
        insert_log(log_message)
        flash("Successfully Registered, Now you can log-in", "warning")
        return redirect(url_for('login'))

    return render_template('registerUser.html')  # Assuming you have a 'register.html' template

#Routes for Register Company Page
@app.route('/registerCompany', methods=['GET', 'POST'])
def registerCompany():
    if request.method == 'GET':

       current_date = datetime.now().strftime('%Y-%m-%d') #Prashanth

       return render_template('registerCompany.html', current_date=current_date)
    
    elif request.method == 'POST':
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
        log_message = f"Company {CompanyName} registered successfully"
        insert_log(log_message)
        flash("Successfully Registered, Now you can log-in", "warning")
        return redirect(url_for('login'))
    return render_template('registerCompany.html', current_date=current_date)  # Assuming you have a 'register.html' template
    


@app.route("/company")
def company():
    return render_template("company.html")

#Routes for Register Company Page
@app.route('/addShift', methods=['GET', 'POST'])
def addShift():
    # if request.method == 'GET':
    #     company = session.get('comp')
    #     cur = mysql.connection.cursor()

        
    #     query_company = "SELECT comp_name FROM company WHERE comp_name= %s;"
    #     cur.execute(query_company,(company,))
    #     user_company = cur.fetchone()

    #     print(user_company)
    #     query_companies = "SELECT companyId, comp_name FROM company;"
    #     cur.execute(query_companies)
    #     shift_data = cur.fetchall()
    #     print(shift_data)

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        company = session.get('comp')

        query_companies = "SELECT companyId, comp_name FROM company where comp_name= %s;"
        cur.execute(query_companies,(company,))
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
        pay = request.form['payrate']
        shiftstatusId = 1 #default -> Pending

        # Create a MySQL cursor
        cur = mysql.connection.cursor()
        # Insert the shift into the database
        query_insert_shift = "INSERT INTO company_shifts (companyId, shift_date, shift_type, start_time, end_time, department_name, supervisor_name, num_workers, notes,pay_rate,shiftStatus_Id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
        values = (companyId, shift_date, shift_type, start_time, end_time, department_name, supervisor_name, num_workers, notes,pay,shiftstatusId)
        cur.execute(query_insert_shift, values)

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        log_message = f"Shift added for {shift_date} successfully"
        insert_log(log_message)
        # Redirect to the company page or any other page you want
        flash("Shift has been posted sucessfully!!", "warning")
        return redirect('postedshifts')

    # Handle other cases or display error page if needed
    return render_template('addShift.html')

# for all shifts
@app.route('/shifts', methods=['GET'])
def allShifts():
    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch all shifts from the database
    #current_date = datetime.date.today().strftime('%Y-%m-%d') #Prashanth
    current_date = datetime.now().strftime('%Y-%m-%d') #Prashanth
    query_all_shifts = "SELECT * FROM company_shifts WHERE shift_date >= %s AND num_workers > 0 ORDER BY shift_date;" #Prashanth
    cur.execute(query_all_shifts,(current_date,)) #Prashanth
    shift_data = cur.fetchall()

    # Create a dictionary to store company names with their respective companyId
    company_names = {}

    # Fetch company names based on companyId for each shift
    for shift in shift_data:
        company_id = shift['companyId']
        if company_id not in company_names:
            # Fetch company name from the database
            query_company_name = "SELECT comp_name FROM company WHERE companyId = %s;"
            cur.execute(query_company_name, (company_id,))
            company_name = cur.fetchone()['comp_name']
            company_names[company_id] = company_name

    # Close the cursor
    cur.close()

    # Render the template and pass the shifts data to it
    return render_template('shifts.html',shifts=shift_data, company_names=company_names)

@app.route('/shiftDetails/<int:shift_id>', methods=['GET'])
def shift_details(shift_id):
    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch the specific shift details from the database based on the shift_id
    query_shift_details = "SELECT * FROM company_shifts WHERE shift_id = %s;"
    cur.execute(query_shift_details, (shift_id,))
    shift = cur.fetchone()

    # Close the cursor
    cur.close()

    # Render the template and pass the shift details to it
    return render_template('shiftDetails.html', shift=shift)

@app.route('/bookShift', methods=['POST'])
def bookShift():
    if request.method == 'POST':
        # Check if the user is logged in before proceeding with the booking
        if 'firstname' not in session and 'comp' not in session:
            # User is not logged in. Redirect to the login page or display an error message.
            return redirect(url_for('login'))

        # Get the shift_id from the form submission
        shift_id = request.form['shiftId']
        paymentStatus = 1 #Default

        # Determine the user type (either 'user' or 'company')
        user_type = 'user' if 'firstname' in session else 'company'

        # Get the user_id based on the user type and email
        user_id = None
        if user_type == 'user':
            # For user, get user_id based on email
            email = session['email']
            cur = mysql.connection.cursor()
            query_user_id = "SELECT userId FROM users WHERE email = %s"
            cur.execute(query_user_id, (email,))
            user_id = cur.fetchone()['userId']
            cur.close()
        elif user_type == 'company':
            # For company, get user_id based on email
            email = session['email']
            cur = mysql.connection.cursor()
            query_user_id = "SELECT companyId FROM company WHERE email = %s"
            cur.execute(query_user_id, (email,))
            user_id = cur.fetchone()['companyId']
            cur.close()

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Check if the shift is already booked by the user
        query_check_booking = "SELECT * FROM bookedshift WHERE user_id = %s AND shift_id = %s"
        cur.execute(query_check_booking, (user_id, shift_id))
        existing_booking = cur.fetchone()

        if existing_booking:
            # The shift is already booked by the user. Handle accordingly (e.g., display a message).
            flash("You have already booked this shift.", "warning")
            #return render_template('shifts.html', messages=get_flashed_messages()) #Prashanth
            return redirect(url_for('allShifts'))
        else:
            # The shift is not booked by the user, so proceed with booking.

            # Insert the booking into the booked_shifts table
            query_book_shift = "INSERT INTO bookedshift (user_id, shift_id,paymentStatus_Id) VALUES (%s, %s,%s)"
            cur.execute(query_book_shift, (user_id, shift_id,paymentStatus))

            # Update the number of workers for the booked shift in the shift table
            query_update_shift = "UPDATE company_shifts SET num_workers = num_workers - 1 WHERE shift_id = %s" #Prashanth
            cur.execute(query_update_shift, (shift_id,))
            # Commit the changes to the database
            mysql.connection.commit()

            # Show a success message or handle the successful booking as needed.
            #flash("Shift successfully booked!", "warning")
            #message = "Shift successfully booked!"

             #Prashanth
            userId = session.get('userId')

            query_booked_shifts = "SELECT bs.*, cs.shift_date, cs.shift_type, c.comp_name " \
                          "FROM bookedShift bs " \
                          "JOIN company_shifts cs ON bs.shift_id = cs.shift_id " \
                          "JOIN company c ON cs.companyId = c.companyId " \
                          "WHERE bs.user_id = %s;"
            cur.execute(query_booked_shifts, (userId,))
            booked_shifts = cur.fetchall()

        # Close the cursor
        cur.close()

        log_message = f"Shift booked by {email} "
        insert_log(log_message)
        flash("Shift successfully booked!", "warning")
        # Redirect back to the allShifts page after booking
        return render_template('onBoard.html', booked_shifts=booked_shifts) #Prashanth

    # Handle GET requests for the /bookShift endpoint if needed (e.g., redirect to another page).
    return redirect(url_for('index'))  # Redirect to the home page or any other page as needed

@app.route('/onBoard', methods=['GET'])
def bookedShifts():
    # Check if the user is logged in before proceeding to show booked shifts
    if 'firstname' not in session and 'comp' not in session:
        flash("Please log in to view booked shifts.", "error")
        return redirect(url_for('login'))

    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch all booked shifts by the current user from the database
    #user_id = session.get('user_id')  # Assuming you have a session variable for user_id
    userId = session.get('userId')

    #current_date = datetime.date.today().strftime('%Y-%m-%d') #Prashanth
    current_date = datetime.now().strftime('%Y-%m-%d') #Prashanth
        #current_time = current_datetime.time()

    query_booked_shifts = "SELECT bs.*, cs.shift_date, cs.shift_type, c.comp_name, cs.shiftStatus_Id " \
                          "FROM bookedShift bs " \
                          "JOIN company_shifts cs ON bs.shift_id = cs.shift_id " \
                          "JOIN company c ON cs.companyId = c.companyId " \
                          "WHERE bs.user_id = %s AND cs.shift_date >= %s ORDER BY shift_date;;"
    cur.execute(query_booked_shifts, (userId,current_date,))
    booked_shifts = cur.fetchall()


    # Close the cursor
    cur.close()
    # Render the template and pass the booked shifts data to it
    return render_template('onBoard.html', booked_shifts=booked_shifts)


@app.route('/bookedShiftDetails/<int:booking_id>', methods=['GET'])
def bookedShiftDetails(booking_id):
    # Check if the user is logged in before proceeding to show booked shift details
    if 'firstname' not in session and 'comp' not in session:
        flash("Please log in to view booked shift details.", "error")
        return redirect(url_for('login'))

    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch the booked shift details based on the booking_id
    query_booked_shift_details = "SELECT bs.*, cs.shift_date, cs.shift_type, c.comp_name, cs.shiftStatus_Id " \
                                 "FROM bookedShift bs " \
                                 "JOIN company_shifts cs ON bs.shift_id = cs.shift_id " \
                                 "JOIN company c ON cs.companyId = c.companyId " \
                                 "WHERE bs.booking_id = %s;"
    cur.execute(query_booked_shift_details, (booking_id,))
    booked_shift_details = cur.fetchone()

    # Close the cursor
    cur.close()

    # Render the template and pass the booked shift details to it
    return render_template('bookedShiftDetails.html', booked_shift=booked_shift_details)

#completed shifts
@app.route('/completedShifts', methods=['GET'])
def completedShifts():
    # Check if the user is logged in before proceeding to show booked shifts
    if 'firstname' not in session and 'comp' not in session:
        flash("Please log in to view booked shifts.", "error")
        return redirect(url_for('login'))

    # Create a MySQL cursor
    cur = mysql.connection.cursor()

    # Fetch all booked shifts by the current user from the database
    #user_id = session.get('user_id')  # Assuming you have a session variable for user_id
    userId = session.get('userId')

    #current_date = datetime.date.today().strftime('%Y-%m-%d') #Prashanth
    current_date = datetime.now().strftime('%Y-%m-%d') #Prashanth
    #query_all_shifts = "SELECT * FROM company_shifts WHERE shift_date >= %s ORDER BY shift_date;" #Prashanth
    #cur.execute(query_all_shifts,(current_date,)) #Prashanth

    query_completed_shifts = "SELECT bs.*, cs.shift_date, cs.shift_type, c.comp_name, bs.paymentStatus_Id " \
                          "FROM bookedShift bs " \
                          "JOIN company_shifts cs ON bs.shift_id = cs.shift_id " \
                          "JOIN company c ON cs.companyId = c.companyId " \
                          "WHERE bs.user_id = %s AND cs.shift_date < %s ORDER BY shift_date;"
    cur.execute(query_completed_shifts, (userId,current_date,))
    completed_shifts = cur.fetchall()



    # Close the cursor
    cur.close()

    # Render the template and pass the booked shifts data to it
    return render_template('completedShifts.html', completed_shifts=completed_shifts)

@app.route('/update_status/<int:shift_id>', methods=['POST'])
def update_status(shift_id):
    if request.method == 'POST':
        new_status = request.form.get('new_status')
        print(new_status)

        # Validate the new_status value
        valid_status_values = ['1', '2', '3']  # Valid status values
        if new_status not in valid_status_values:
            flash("Invalid status.", "error")
            return redirect(url_for('bookedShifts'))

        # Check if the shift is currently within the start and end times
        cur = mysql.connection.cursor()
        query_fetch_shift = "SELECT shift_date,start_time, end_time FROM company_shifts WHERE shift_id = %s"
        cur.execute(query_fetch_shift, (shift_id,))
        shift_times = cur.fetchone()

        shift_date = shift_times['shift_date']
        shift_start_time = shift_times['start_time']

        # Convert shift_date and shift_start_time to strings
        shift_date_str = shift_date.strftime('%Y-%m-%d')
        shift_start_time_str = str(shift_start_time)

        # Combine shift_date and shift_start_time into a single datetime object
        shift_datetime = datetime.strptime(shift_date_str + ' ' + shift_start_time_str, '%Y-%m-%d %H:%M:%S')

        cur.close()

        current_datetime = datetime.now()

        if current_datetime >= shift_datetime :
            # Update the status in the database
            print(current_datetime)
            #print(shift_start_time)
            cur = mysql.connection.cursor()
            query_update_status = "UPDATE company_shifts SET shiftStatus_Id = %s WHERE shift_id = %s"
            cur.execute(query_update_status, (new_status, shift_id))
            mysql.connection.commit()

            userId = session.get('userId')

            #current_date = datetime.date.today().strftime('%Y-%m-%d') #Prashanth

            cur.close()

            log_message = f"Shift edited by sucessfully"
            insert_log(log_message)
            flash("Shift status updated.", "success")
            return redirect(url_for('bookedShifts'))
        else:
            flash("Shift is not currently active.", "error")
            return redirect(url_for('bookedShifts'))

@app.route('/logout')
def logout():
    # Clear the session data for the company
    session.pop('comp', None)
    session.pop('email', None)

    # Redirect to the login page or any other page you want
    return redirect(url_for('login'))


@app.route("/postedshifts" , methods=['GET'])
def posted_shifts():
    try:
        # Fetch the company name from the session
        comp_name = session.get('comp')

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Execute the query to fetch posted shifts from the database
        query_fetch_shifts = "SELECT cs.* FROM company_shifts cs INNER JOIN company c ON c.companyId=cs.companyId WHERE c.comp_name = %s ;"
        cur.execute(query_fetch_shifts, (comp_name,))


        print(comp_name)
        # Fetch all posted shifts
        posted_shifts_data = cur.fetchall()

        # Close the cursor
        cur.close()

        # Check if any shifts were fetched
        if posted_shifts_data:
            return render_template("postedshifts.html", posted_shifts=posted_shifts_data)
        else:
            # Handle the case where no shifts were fetched (e.g., display an error message)
            return render_template("postedshifts.html")
            #return "No posted shifts found."

    except Exception as e:
        # Handle exceptions (e.g., display an error page)
        return "Error fetching posted shifts."

@app.route('/editshift/<int:shift_id>', methods=['GET', 'POST'])
def edit_shift(shift_id):
    message = ""  # Initialize the message variable with an empty string
    shift = None  # Initialize the shift variable
    query_fetch_shift = "SELECT * FROM company_shifts WHERE shift_id = %s;"  # Define the query outside the request blocks

    if request.method == 'GET':
        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Fetch the shift details based on the shift_id from the database
        cur.execute(query_fetch_shift, (shift_id,))
        shift = cur.fetchone()

        # Close the cursor
        cur.close()

        return render_template('editshift.html', shift=shift, message=message)

    elif request.method == 'POST':
        # Handle the form submission for updating the shift details
        # Extract the form data for the updated shift details
        shift_date = request.form['shift_date']
        shift_type = request.form['shift_type']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        department_name = request.form['department_name']
        supervisor_name = request.form['supervisor_name']
        num_workers = request.form['num_workers']
        notes = request.form['notes']

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Implement the database query to update the shift details based on the shift_id
        query_update_shift = "UPDATE company_shifts SET shift_date = %s, shift_type = %s, start_time = %s, end_time = %s, department_name = %s, supervisor_name = %s, num_workers = %s, notes = %s WHERE shift_id = %s;"
        cur.execute(query_update_shift, (
            shift_date, shift_type, start_time, end_time, department_name, supervisor_name, num_workers, notes, shift_id))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Fetch the shift details again after the update
        cur = mysql.connection.cursor()
        cur.execute(query_fetch_shift, (shift_id,))
        shift = cur.fetchone()
        cur.close()

        flash("Shift details updated successfully!", "success")

        return redirect("/postedshifts")


@app.route('/deleteshift/<int:shift_id>', methods=['GET'])
def delete_shift(shift_id):
    try:
        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Fetch the shift details based on the shift_id
        query_fetch_shift = "SELECT * FROM company_shifts WHERE shift_id = %s;"
        cur.execute(query_fetch_shift, (shift_id,))
        shift = cur.fetchone()

        # Check if the shift exists
        if not shift:
            # Instead of flash, return a JavaScript alert with the error message
            return f"<script>alert('Shift not found.'); window.location.href = '{url_for('posted_shifts')}';</script>"

        # Implement the database query to delete the shift based on the shift_id
        query_delete_shift = "DELETE FROM company_shifts WHERE shift_id = %s;"
        cur.execute(query_delete_shift, (shift_id,))

        # Commit the changes to the database
        mysql.connection.commit()

        # Instead of flash, return a JavaScript alert with the success message
        return f"<script>alert('Shift deleted successfully!'); window.location.href = '{url_for('posted_shifts')}';</script>"

    except mysql.connection.Error as e:
        # Instead of flash, return a JavaScript alert with the error message
        if e.args[0] == 1451:
            return f"<script>alert('Cannot delete the shift as it is already claimed by a user.');</script>"
        else:
            return f"<script>alert('An error occurred: {e}'); window.location.href = '{url_for('posted_shifts')}';</script>"

        # Rollback the transaction to maintain data consistency
        mysql.connection.rollback()

    return redirect("/postedshifts")

@app.route("/pendingpayments", methods=['GET', 'POST'])
def pending_payments():
    
        # Fetch the company name from the session
        comp_name = session.get('comp')

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Execute the query to fetch pending shifts from the database
        query_fetch_pending_shifts = "SELECT cs.*, bs.*,ps.statusName,u.firstname,cs.pay_rate FROM bookedshift bs INNER JOIN company_shifts cs ON cs.shift_id=bs.shift_id INNER JOIN company c ON c.companyId=cs.companyId INNER JOIN Paymentstatus ps ON ps.statusId=bs.paymentStatus_Id INNER join users u ON u.userid=bs.user_id WHERE c.comp_name = %s;"
        cur.execute(query_fetch_pending_shifts, (comp_name,))
        
        # Fetch all pending shifts
        pending_shifts_data = cur.fetchall()

        # Close the cursor
        cur.close()

        return render_template("pendingpayments.html", pending_shifts=pending_shifts_data)

    

@app.route("/update_payment_status/<int:shift_id>", methods=['GET', 'POST'])
def update_payment_status(shift_id):
    if request.method == 'GET':
        try:
            new_status = '2'  # Set the status directly to "Paid"

            print(new_status,shift_id)
            # Update the payment status in the database
            cur = mysql.connection.cursor()

            query_status_check = "Select shiftStatus_Id from company_shifts WHERE shift_id = %s"
            cur.execute(query_status_check, (shift_id,))
            shift_status = cur.fetchone()
            print(shift_status)

            if (shift_status == 3):
                query_update_status = "UPDATE bookedshift SET paymentStatus_Id = %s WHERE shift_id = %s"
                cur.execute(query_update_status, (new_status, shift_id))
                mysql.connection.commit()
                cur.close()

                log_message = f"Payment done successfully "
                insert_log(log_message)
                flash("Payment status updated.", "success")
                return redirect("/pendingpayments")
            else:
                flash("Shift is not completed.")
                return redirect("/pendingpayments")
        

        except Exception as e:
            # Handle exceptions (e.g., display an error page)
            flash("Error updating payment status.", "error")
            return redirect("/pendingpayments")
        
#Routes for Feedback Page
@app.route('/feedback', methods=['GET', 'POST'])
def feedbackform():
    if request.method == 'POST':
        # Get form data
        Name = request.form['name']
        Email = request.form['email']
        feedback = request.form['feedback']

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Insert the user into the database
        cur.execute("INSERT INTO feedback (Username,email,feedback) VALUES (%s, %s, %s)", (Name, Email, feedback))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the login page or any other page you want
        log_message = f"User {Name} has given feedback "
        insert_log(log_message)
        return redirect(url_for('feedback'))

    return render_template('onBoard.html')  # Assuming you have a 'register.html' template
        








