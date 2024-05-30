from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'retrozdbcluster.c0y8rgzc2efk.us-east-1.rds.amazonaws.com',
    'database': 'retrozdb',
    'user': 'dbadmin',
    'password': '2RaMBAUBBhRm9a'
}

# Connect to the database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    return connection

@app.route('/')
def index():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', records=records)

@app.route('/create', methods=['GET', 'POST'])
def create_record():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        connection = create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        cursor.execute(query, (username, email))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        cursor.execute(query, (username, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    else:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        record = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('update.html', record=record)

@app.route('/delete/<int:id>')
def delete_record(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)