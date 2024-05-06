from flask import Flask, request, render_template
from pymongo import MongoClient 

app = Flask(__name__) 

# root route 
@app.route('/') 
def hello_world(): 
    return 'Hello, World!'

# Set up MongoDB connection and collection 
client = MongoClient('mongodb://localhost:27017/') 
db = client['demo'] 
collection = db['data'] 

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

if __name__ == '__main__': 
    app.run(debug=True)
