from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecret"
app.config['SESSION_TYPE'] = 'filesystem'

# MySQL Config (edit as needed)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   # change to your MySQL password
app.config['MYSQL_DB'] = 'buy_sell'

mysql = MySQL(app)
Session(app)

def logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password_plain = request.form['password'].encode('utf-8')
        role = request.form['role']

        # hash password and store as utf-8 string
        password_hashed = bcrypt.hashpw(password_plain, bcrypt.gensalt()).decode('utf-8')

        # insert
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password_hashed, role)
            )
            mysql.connection.commit()
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash("Username already exists or database error.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password_input = request.form['password'].encode('utf-8')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username=%s", [username])
        user = cursor.fetchone()

        if user:
            stored_hash = user['password'].encode('utf-8')
            if bcrypt.checkpw(password_input, stored_hash):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not logged_in() or session.get('role') != 'vendor':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        price = request.form['price']

        if not name or float(price) <= 0:
            flash("Please provide a valid name and price.")
            return redirect(url_for('add_product'))

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, vendor_id) VALUES (%s, %s, %s, %s)",
            (name, description, price, session['user_id'])
        )
        mysql.connection.commit()
        flash("Product added successfully")
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
