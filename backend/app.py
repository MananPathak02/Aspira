import os
import ssl
from flask import session
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(
    __name__,
    template_folder='templates',       # HTML templates
    static_folder='static'  # CSS/JS/images
)
app.secret_key = 'supersecretkey'  # required for session
# MongoDB Atlas connection
CONNECTION_STRING = "mongodb+srv://mananpathak0052_db_user:u8ckqDFntBZoXPyF@cluster0.mjxtlsu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"
client = MongoClient(
    CONNECTION_STRING,
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client['aspiraDB']
users_collection = db['users']

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# Flask-Mail configuration (put this near the top, before using Mail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mananpathak672@gmail.com'  # sender email
app.config['MAIL_PASSWORD'] = 'fudjyocvluhvdfxv'          # Gmail app password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)  # initialize Mail AFTER config

# ----------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        username = request.form['email']
        password = request.form['password']

        if users_collection.find_one({"username": username}):
            return "Email already exists"
        
        # Insert user in DB
        users_collection.insert_one({
            "name": name,
            "username": username,
            "password": password
        })

        # Send welcome email
        try:
            with app.app_context():
                print("Sending welcome email to", username)
                msg = Message(
                    subject="Welcome to Aspira!",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[username]
                )
                msg.html = render_template('welcome.html', name=name)
                mail.send(msg)
                print("Email sent successfully!")
        except Exception as e:
            print("Error sending email:", e)

        return redirect(url_for('dashboard'))

    return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({"username": email, "password": password})
        if user:
            session['username']=user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password"
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['username'])


if __name__ == '__main__':
    app.run(debug=True)
