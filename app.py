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
    try:
        conn = mysql.connection

        if conn is None:
            raise Exception("MySQL connection is None")

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
    except Exception as e:
        print("An error occurred during database and table creation:", str(e))
    finally:
        if cursor:
            cursor.close()

@app.route('/')
def hello():
    try:
        create_messages_table()  # Create the messages table

        cur = mysql.connection.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        new_message = request.form.get('new_message')
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('hello'))
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
