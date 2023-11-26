from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aotb39v6404nf888s0jdob2j4'  # Change this to your actual secret key

# Initialize SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create a table for users if it does not exist
def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

# Call the function to ensure the table is created
init_db()

# Middleware to require tokens for certain routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            db = get_db_connection()
            user = db.execute('SELECT * FROM users WHERE username = ?', (data['username'],)).fetchone()
            db.close()
            if user is None:
                raise RuntimeError('User not found.')
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(user, *args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])

    db = get_db_connection()
    existing_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if existing_user:
        db.close()
        return jsonify({'message': 'Username already exists!'}), 400

    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()
    db.close()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user is None:
        db.close()
        return jsonify({'message': 'User not found!'}), 401

    if check_password_hash(user['password'], password):
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        db.close()
        print(token)
        return jsonify({'token': token})

    db.close()
    return jsonify({'message': 'Password is wrong!'}), 403

@app.route('/validate', methods=['GET'])
@token_required
def validate_token(current_user):
    return jsonify({'message': 'Token is valid.', 'user_id': current_user['user_id']}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
