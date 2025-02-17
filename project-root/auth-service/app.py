from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database connection
db = pymysql.connect(
    host='db',  # Hostname of the database container
    user='root',
    password='password',
    database='userdb'
)

# Default route for testing
@app.route('/')
def index():
    return "Auth Service is running!", 200

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (data['username'], data['password']))
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor = db.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (data['username'], data['password']))
    db.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

