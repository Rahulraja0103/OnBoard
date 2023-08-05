
# Importing various Modules
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL,MySQLdb


# Initializing the Flask Application an Configure the database connection
app = Flask(__name__)
app.secret_key = 'abc'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Justdoit@123' # Password Here
app.config['MYSQL_DB'] = 'onboard' # Database Name 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



from app import routes