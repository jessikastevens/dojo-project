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
        email = request.form['email']
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email= '{username}'")
            user = cursor.fetchone()
        except sqlite3.Error as error:
            print("Database error:", error)
            return render_template('login.html')
        finally:    
            cursor.close()
        if user: 
            if check_password_hash(user[3], password):
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error = "Invalid password")
        else:
            try:
                query = "INSERT INTO users VALUES (NULL, ?, ?, ?)"
                insert_data = (username, email, generate_password_hash(password))
                cursor = connection.cursor()
                cursor.execute(query, insert_data)
                connection.commit()
            except sqlite3.Error as error:
                print("Database error: ", error)
                return render_template('signup.html')
            finally:
                cursor.close()
                return redirect(url_for('login'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run()