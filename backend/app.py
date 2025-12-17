import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os 
import ssl
from ml.predict import predict_profile
from flask import session
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(
    __name__,
    template_folder='templates',  
    static_folder='static'  
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
profiles_collection = db['career_profiles'] 

# Routes
@app.route('/')
def home():
    return render_template('index.html')


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mananpathak672@gmail.com'  
app.config['MAIL_PASSWORD'] = 'fudjyocvluhvdfxv'          
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)  

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

@app.route('/api/submit-profile', methods=['POST'])
def submit_profile():
    try:
        data = request.get_json(force=True)
        # sanitize / minimal validation
        profile = {
            "firstName": data.get("firstName", "").strip(),
            "lastName": data.get("lastName", "").strip(),
            "age": int(data.get("age")) if data.get("age") not in (None, "") else None,
            "marks10": float(data.get("marks10")) if data.get("marks10") not in (None, "") else None,
            "marks12": float(data.get("marks12")) if data.get("marks12") not in (None, "") else None,
            "subjects12": data.get("subjects12", "").strip(),
            "interests": data.get("interests", "").strip(),
            "strengths": data.get("strengths", "").strip(),
            "weaknesses": data.get("weaknesses", "").strip(),
            # keep location fields in profile but we WILL NOT use it for prediction
            "currentLocation": data.get("currentLocation", "").strip(),
            "preferredLocation": data.get("preferredLocation", "").strip(),
            "budget": data.get("budget"),
            "goal": data.get("goal", "").strip(),
            "exams": data.get("exams", "").strip(),
            "rank": data.get("rank", None),
            "created_at": None
        }

        # Add timestamp
        import datetime
        profile["created_at"] = datetime.datetime.utcnow()

        # Save profile in MongoDB
        res = profiles_collection.insert_one(profile)
        profile["_id"] = str(res.inserted_id)

        # RUN prediction (do NOT use location fields)
        prediction_input = {
            "marks12": profile["marks12"],
            "subjects12": profile["subjects12"],
            "interests": profile["interests"],
            "exams": profile.get("exams", ""),
            "rank": profile.get("rank", None)
        }
        prediction = predict_profile(prediction_input)

        # Persist prediction into the same doc
        profiles_collection.update_one({"_id": res.inserted_id}, {"$set": {"prediction": prediction}})

        # Return prediction to frontend
        return jsonify({"success": True, "profile_id": profile["_id"], "prediction": prediction})

    except Exception as e:
        print("Error in /api/submit-profile:", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
