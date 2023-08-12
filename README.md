# OnBoard

#Installation 
1.) Creating a new Environment python -m venv myenv

2.) Activate the virtual environment myenv\Scripts\activate

3.) Clone the Repository git clone

4.) Install the required Flask for the App pip install Flask 

5.) Install the mySql required for flask 
pip install flask-mysql
# Initializing the Flask Application an Configure the database connection
app = Flask(__name__)
app.secret_key = 'abc'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rahul' # Password Here
app.config['MYSQL_DB'] = 'onboard' # Database Name 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

6.) Run the App python run.py