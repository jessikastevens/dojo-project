from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

connection = sqlite3.connect('DojoProject.db', check_same_thread=False)
query = """CREATE TABLE IF NOT EXISTS
    users(id INTEGER PRIMARY KEY,username TEXT NOT NULL, firstname TEXT NOT NULL, surname TEXT NOT NULL,
email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)"""
cursor = connection.cursor()
cursor.execute(query)

connection = sqlite3.connect('DojoProject.db', check_same_thread=False)
query = """CREATE TABLE IF NOT EXISTS
    events(id INTEGER PRIMARY KEY, location TEXT NOT NULL, course TEXT NOT NULL,
instructor TEXT NOT NULL, date DATETIME NOT NULL, organiser TEXT NOT NULL)"""
cursor = connection.cursor()
cursor.execute(query)

connection = sqlite3.connect('DojoProject.db', check_same_thread=False)
query = """CREATE TABLE IF NOT EXISTS
    bookings(id INTEGER PRIMARY KEY, location TEXT NOT NULL, course TEXT NOT NULL, childName TEXT NOT NULL, 
    childAge INTEGER NOT NULL, date DATETIME NOT NULL, codingExperience TEXT NOT NULL, addChild TEXT NOT NULL)"""
cursor = connection.cursor()
cursor.execute(query)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email= '{username}'")
            user = cursor.fetchone()
        except sqlite3.Error as error:
            print("Database error:", error)
            return render_template('login.html')
            
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstName']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('signup.html', error="Email is already registered")
        
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, firstname, surname, email, password) VALUES (?, ?, ?, ?, ?)",
                           (username, firstname, surname, email, hashed_password))
            connection.commit()
            return redirect(url_for('login'))
        except sqlite3.Error as error:
            print("Database error:", error)
            return render_template('signup.html', error="Error registering user")
    
    return render_template('signup.html')

@app.route("/booking", methods = ['GET','POST'])
def booking():
    if request.method == 'POST':
        location = request.form('location')
        course = request.form('course')
        childName = request.form('childName')
        childAge = request.form('childAge')
        date = request.form('datetime')
        codingExperience = request.form('codingExperience')
        addChild = request.form('addChild')

        if not all([location, course, childName, childAge, date, codingExperience, addChild]):
            return render_template('booking_form.html', error="All fields are required.")
        
        try:
            cursor.execute(
                "INSERT INTO bookings (location, course, childName, childAge, date, codingExperience, addChild) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (location, course, childName, childAge, date, codingExperience, addChild)
            )
            connection.commit()
            return redirect(url_for('booking'))
        except sqlite3.Error as error:
            print("Database error: ", error)
            return render_template('booking.html', error="Error booking event")
       
    return render_template('booking.html')

@app.route("/organise", methods=["GET", "POST"])
def organise():
    if request.method == 'POST':
        location = request.form.get('location')
        course = request.form.get('course')
        instructor = request.form.get('instructor')
        date = request.form.get('date')
        organiser = request.form.get('organiser')

        if not all([location, course, instructor, date, organiser]):
            return render_template('organise.html', error="All fields are required.")

        try:
            cursor.execute(
                "INSERT INTO events (location, course, instructor, date, organiser) VALUES (?,?,?,?,?)",
                (location, course, instructor, date, organiser)
            )
            connection.commit()
            return redirect(url_for('booking'))
        except sqlite3.Error as error:
            print("Database error: ", error)
            return render_template('organise.html', error="Error organising event")
        finally:
            cursor.close()

    return render_template('organise.html')

if __name__ == '__main__':
    app.run()