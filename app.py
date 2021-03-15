from flask import Flask, request, render_template, redirect, url_for
from hashlib import sha256

app = Flask(__name__)
user_data = []

error_message = ''
is_currently_logged_in = False

local_user_data = []

## signup form
@app.route('/signup')
def signup():
    global error_message, is_currently_logged_in, local_user_data
    local_user_data = []

    if not is_currently_logged_in:
        return render_template('signup.html', error=error_message)

    else:
        return redirect(url_for('preformsignup'))


## login form
@app.route('/login')
def login():

    if not is_currently_logged_in:
        return render_template('login.html')
    else:
        return redirect(url_for('home'))


## necessary checks before logging in
@app.route('/preformlogin', methods=['POST'])
def preformlogin():
    global local_user_data, is_currently_logged_in

    username_input = str(request.form['name']).lower()
    password = sha256(str(request.form['password']).encode('utf-8')).hexdigest()

    for u in user_data:
        _user = str(u[0]).lower()
        _pass = str(u[1]).lower()
        if _user == username_input and _pass == password:
            local_user_data.append(str(request.form['name']))
            is_currently_logged_in = True
            return redirect(url_for('home'))

    return redirect(url_for('login'))


## checks before signing up
@app.route('/preformsignup', methods=['POST'])
def preformsignup():
    global error_message, is_currently_logged_in, local_user_data
    username = str(request.form['name'])
    password = str(request.form['password'])

    if (len(username) > 2  and len(username) < 21 and len(password) > 7):

        password = sha256(password.encode('utf-8')).hexdigest()

        # checks if the username is registered
        for u in user_data:
            user = str(u[0]).lower()
            if user == str(username).lower():
                error_message = 'Username already registered'
                return redirect(url_for('signup'))

        # adds the data to an array
        is_currently_logged_in = True
        user_data.append([username, password])
        local_user_data.append(username)

        error_message = ''
        print('to home')
        return redirect(url_for('home'))

    error_message = 'Short username or password'
    return redirect(url_for('signup'))

## main page
@app.route('/home', methods=['GET','POST'])
def home():
    global local_user_data
    
    return render_template('home.html', usr=local_user_data[0])


## logs out the user
@app.route('/preformlogout', methods=['POST'])
def preformlogout():
    global is_currently_logged_in, local_user_data
    local_user_data = []
    is_currently_logged_in = False
    return redirect(url_for('signup'))

app.run()