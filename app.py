from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/cryptography_db"

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        crypto = mongo.db.cryptography_data
        login_user = crypto.find_one({'email': request.form['email']})

        if login_user:
            hashpass = hashlib.sha256(request.form['password'].encode('utf-8'))
            hpass = hashpass.hexdigest()
            if hpass == login_user['password']:
                return 'Hello!'

            return 'Invalid email or password'
        return 'Invalid method'

    return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        crypto = mongo.db.cryptography_data
        existing_user = crypto.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = hashlib.sha256(request.form['password'].encode('utf-8'))
            hpass = hashpass.hexdigest()
            crypto.insert({'email':request.form['email'], 'password': hpass})
            return redirect(url_for('sign_up'))

        return 'This email already exists!'

    return render_template('sign_up.html')





if __name__ == "__main__":
    app.run(debug=True)