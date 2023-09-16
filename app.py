import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables or use defaults
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Function to create the messages table if it doesn't exist
def create_messages_table():
    conn = mysql.connection
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}")
    cursor.execute(f"USE {app.config['MYSQL_DB']}")

    # Check if the table exists
    cursor.execute("SHOW TABLES LIKE 'messages'")
    result = cursor.fetchone()

    if not result:
        # Table doesn't exist, create it
        cursor.execute('''
            CREATE TABLE messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            )
        ''')
        print("Table 'messages' created.")

    cursor.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

# Create the database and table, then run the Flask application
if __name__ == '__main__':
    # Create the database and table
    create_messages_table()

    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)
