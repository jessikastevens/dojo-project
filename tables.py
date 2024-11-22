import sqlite3

conn = sqlite3.connect('DojoProject.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS instructors
             (instructorId INT PRIMARY KEY NOT NULL,
              firstName TEXT NOT NULL,
              lastName TEXT NOT NULL,
              email TEXT NOT NULL)''')

c.execute("INSERT INTO instructors (instructorId, firstName, lastName, email) VALUES (1, 'James', 'Smith', 'james.smith@instructor.com')")
c.execute("INSERT INTO instructors (instructorId, firstName, lastName, email) VALUES (2, 'Jenny', 'Green', 'jenny.green@instructor.com')")
c.execute("INSERT INTO instructors (instructorId, firstName, lastName, email) VALUES (3, 'Oliver', 'Turner', 'oliver.turner@instructor.com')")
c.execute("INSERT INTO instructors (instructorId, firstName, lastName, email) VALUES (4, 'Danny', 'Baker', 'danny.baker@instructor.com')")

conn.commit()

conn.close()


conn = sqlite3.connect('DojoProject.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS locations
             (locationId INT PRIMARY KEY NOT NULL,
              city TEXT NOT NULL)''')

c.execute("INSERT INTO locations (locationId, city) VALUES (1, 'London')")
c.execute("INSERT INTO locations (locationId, city) VALUES (2, 'Manchester')")
c.execute("INSERT INTO locations (locationId, city) VALUES (3, 'York')")
c.execute("INSERT INTO locations (locationId, city) VALUES (4, 'Cambridge')")

conn.commit()

conn.close()


conn = sqlite3.connect('DojoProject.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS courses
             (courseId INT PRIMARY KEY NOT NULL,
              course TEXT NOT NULL)''')

c.execute("INSERT INTO courses (courseId, course) VALUES (1, 'Game design')")
c.execute("INSERT INTO courses (courseId, course) VALUES (2, 'Scratch')")
c.execute("INSERT INTO courses (courseId, course) VALUES (3, 'Basic python')")
c.execute("INSERT INTO courses (courseId, course) VALUES (4, 'Web design')")

conn.commit()

conn.close()