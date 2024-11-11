from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

connection = sqlite3.connect('DojoProject.db', check_same_thread=False)
query = """CREATE TABLE IF NOT EXISTS
    users(id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, surname TEXT NOT NULL,
email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)"""
cursor = connection.cursor()
cursor.execute(query)
cursor.close()

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
        finally:    
            cursor.close()
            
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
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
            cursor.execute("INSERT INTO users (firstname, surname, email, password) VALUES (?, ?, ?, ?)",
                           (firstname, surname, email, hashed_password))
            connection.commit()
            cursor.close()
            return redirect(url_for('login'))
        except sqlite3.Error as error:
            print("Database error:", error)
            return render_template('signup.html', error="Error registering user")
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()