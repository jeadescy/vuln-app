# 🔓 Vulnerable Web Application

A deliberately vulnerable web application built with Flask for practicing web security testing and exploitation.

## ⚠️ WARNING
This application is **intentionally vulnerable** and should only be used in controlled environments for educational purposes. Do not deploy this in production or expose it to the internet.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:5000`

## 🕳️ Built-in Vulnerabilities

### 1. SQL Injection
- **Location:** Login and registration forms
- **Vulnerability:** Direct string concatenation in SQL queries
- **Example payload:** `' OR '1'='1` in username field

### 2. Cross-Site Scripting (XSS)
- **Location:** Comments section
- **Vulnerability:** Comments are rendered without HTML escaping
- **Example payload:** `<script>alert('XSS')</script>`

### 3. Weak Password Storage
- **Vulnerability:** Passwords stored using MD5 hash (easily crackable)
- **Location:** User registration and login

### 4. Predictable Session Management
- **Vulnerability:** Session cookies use username directly
- **Location:** Login system

### 5. No Input Validation
- **Vulnerability:** No sanitization of user inputs
- **Location:** All forms

## 🧪 Testing the Vulnerabilities

### SQL Injection Test
1. Register a normal user account
2. Try logging in with: `' OR '1'='1` as username and any password
3. You should be logged in as the first user in the database

### XSS Test
1. Go to the comments page
2. Post a comment with: `<script>alert('XSS Test')</script>`
3. The script should execute when you view the comments

### Session Hijacking
1. Login with a user account
2. Check the browser cookies - session cookie will be the username
3. You can manually change this cookie to impersonate other users

## 📁 File Structure
```
vuln_webapp/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── database.db        # SQLite database (created automatically)
├── templates/         # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   └── comments.html
└── static/
    └── style.css      # CSS styling
```

## 🛠️ Security Fixes (For Learning)

After practicing exploitation, you can implement these fixes:

1. **SQL Injection Fix:** Use parameterized queries
2. **XSS Fix:** HTML escape all user input
3. **Password Fix:** Use bcrypt or Argon2 for hashing
4. **Session Fix:** Use secure, random session tokens
5. **Input Validation:** Add proper input sanitization

## ⚖️ Legal Notice
This application is for educational purposes only. Always ensure you have proper authorization before testing security vulnerabilities on any system. 