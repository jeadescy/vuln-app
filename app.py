from flask import Flask, render_template, request, redirect, make_response, session
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # ⚠️ Weak secret key

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            comment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ⚠️ INTENTIONAL VULNERABILITY: Weak password hashing (MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ⚠️ INTENTIONAL VULNERABILITY: No input validation
        hashed_password = hash_password(password)
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        try:
            # ⚠️ INTENTIONAL VULNERABILITY: SQL Injection possible
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')")
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists!"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = hash_password(password)
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # ⚠️ INTENTIONAL VULNERABILITY: SQL Injection
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # ⚠️ INTENTIONAL VULNERABILITY: Predictable session cookie
            resp = make_response(redirect('/comments'))
            resp.set_cookie('session', username)
            resp.set_cookie('user_id', str(user[0]))
            return resp
        else:
            return "Invalid credentials!"
    
    return render_template('login.html')

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        comment = request.form['comment']
        username = request.cookies.get('session', 'Anonymous')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # ⚠️ INTENTIONAL VULNERABILITY: XSS - No HTML escaping
        cursor.execute(f"INSERT INTO comments (username, comment) VALUES ('{username}', '{comment}')")
        conn.commit()
        conn.close()
        
        return redirect('/comments')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, comment, timestamp FROM comments ORDER BY timestamp DESC")
    comments = cursor.fetchall()
    conn.close()
    
    return render_template('comments.html', comments=comments)

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('session')
    resp.delete_cookie('user_id')
    return resp

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 