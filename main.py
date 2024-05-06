from flask import Flask, request, render_template, session, redirect, url_for
from bson import ObjectId  # Import ObjectId from bson module
from pymongo import MongoClient 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Set up MongoDB connection and collection 
client = MongoClient('mongodb://localhost:27017/') 
db = client['demo'] 
collection = db['data'] 

# Add index page route
@app.route('/')
def index():
    return render_template('index.html')

# Add signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        
        # Create dictionary to represent the user data
        data = {
            'fname': fname,
            'lname': lname,
            'email': email
        }
        
        # Insert the user data into MongoDB
        collection.insert_one(data)
        
        return 'Signup successful!'


# Add Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        data = collection.find_one({'email': email, 'password': password})
        if data:
            session['loggedin'] = True
            session['id'] = str(data['_id'])  # Convert ObjectId to string
            session['email'] = data['email']
            msg = 'Logged in successfully!'
            return redirect(url_for('profile'))  # Redirect to user profile page
        else:
            msg = 'Incorrect email/password'
            return render_template('login.html', msg=msg), 401  # Unauthorized status code
    return render_template('login.html')

# User profile route
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        # Get user data from session
        user_id = session['id']
        user_data = collection.find_one({'_id': ObjectId(user_id)})
        return render_template('profile.html', user=user_data)
    else:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect to login page after logout
if __name__ == '__main__': 
    app.run(debug=True)
