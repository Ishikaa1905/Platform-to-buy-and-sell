# Buy & Sell Platform (Simple)

A minimal Flask + MySQL app where users can register/login, vendors can add products, and everyone can browse products.

## Stack
- Flask, Flask-MySQLdb, Flask-Session, bcrypt
- HTML/CSS/JS (vanilla)
- MySQL

## Setup

1. **Create & activate venv (optional)**
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\\Scripts\\activate
```

2. **Install deps**
```bash
pip install -r requirements.txt
```
> Note: `Flask-MySQLdb` requires MySQL client libraries. On Windows install MySQL and ensure `mysqlclient` libs are present.

3. **Create database & tables**
```bash
# edit MySQL credentials in app.py if needed
mysql -u root -p < schema.sql
```

4. **Run the app**
```bash
python app.py
```
Open `http://127.0.0.1:5000/`

## Default Roles
- Choose **User** or **Vendor** during registration. Only *vendors* can add products.

## Notes
- Passwords are hashed with `bcrypt`.
- This is a simple starter. Add orders/checkout later if needed.
