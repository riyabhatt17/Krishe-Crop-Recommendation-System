from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import warnings
from datetime import timedelta
from flask import Flask, request, jsonify

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Trying to unpickle estimator StandardScaler")

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=31)  # For remember me functionality

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# Ensure the static folder exists
static_folder = os.path.join(app.root_path, 'static')
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

# Updated User model
class User(db.Model):
    __tablename__ = 'users'  # Explicitly define table name
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, fullname, email, mobile, password):
        self.fullname = fullname
        self.email = email
        self.mobile = mobile
        self.password = password
        self.username = email.split('@')[0]  # Creating username from email

def init_db():
    """Initialize the database and create all tables"""
    with app.app_context():
        # Drop all tables first to ensure clean state
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

# Initialize database tables
init_db()

# Load or create ML models and scalers
def load_or_create_models():
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        sc = pickle.load(open('standscaler.pkl', 'rb'))
        ms = pickle.load(open('minmaxscaler.pkl', 'rb'))
        print("Models loaded successfully!")
        return model, sc, ms
    except Exception as e:
        print(f"Error loading model or scalers: {e}")
        print("Recreating model and scalers...")
        
        try:
            data = pd.read_csv('Crop_recommendation.csv')
            X = data.drop('label', axis=1)  # Assuming 'label' is your target column
            y = data['label']

            sc = StandardScaler()
            ms = MinMaxScaler()
            X_scaled = sc.fit_transform(X)
            X_scaled = ms.fit_transform(X_scaled)

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_scaled, y)

            # Save the new model and scalers
            pickle.dump(model, open('model.pkl', 'wb'))
            pickle.dump(sc, open('standscaler.pkl', 'wb'))
            pickle.dump(ms, open('minmaxscaler.pkl', 'wb'))
            print("Models created and saved successfully!")
            return model, sc, ms
        except Exception as e:
            print(f"Error creating models: {e}")
            return None, None, None

# Load the models
model, sc, ms = load_or_create_models()

# Login required decorator
def login_required(f):
    def wrapped_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapped_function.__name__ = f.__name__
    return wrapped_function

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message', '').lower()
    
    responses = {
    # Greetings
    'hello': 'Hello! Welcome to Krishe. How can I assist you today?',
    'hi': 'Hi there! Welcome to Krishe. How can I help you?',
    'good morning': 'Good morning! Wishing you a productive day ahead. How can Krishe assist you?',
    'good evening': 'Good evening! Hope you had a great day. How can I help you with Krishe?',

    # Login and Registration
    'how to login': 'To login to Krishe:\n1. Click on the "Login" button in the top right\n2. Enter your registered email and password\n3. Click "Sign In"\nIf you need help, click "Forgot Password".',
    'how to register': 'To register on Krishe:\n1. Click "Sign Up" in the top right\n2. Fill in your details (name, email, password)\n3. Verify your email\n4. Complete your profile.\nFeel free to reach out if you face any issues!',
    'login': 'To login to Krishe:\n1. Click on the "Login" button in the top right\n2. Enter your registered email and password\n3. Click "Sign In"\nIf you need help, click "Forgot Password".',
    'register': 'To register on Krishe:\n1. Click "Sign Up" in the top right\n2. Fill in your details (name, email, password)\n3. Verify your email\n4. Complete your profile.\nFeel free to reach out if you face any issues!',
    

    # About Krishe
    'what is krishe': 'Krishe is a comprehensive crop recommendation system that helps farmers choose the best crops based on soil conditions and environmental factors.',
    'about krishe': 'Krishe is an advanced agricultural platform that:\n- Analyzes soil parameters\n- Considers environmental conditions\n- Provides accurate crop recommendations\n- Helps optimize farming decisions\n- Supports sustainable farming practices.',
    'what': 'Krishe is a comprehensive crop recommendation system that helps farmers choose the best crops based on soil conditions and environmental factors.',
    'about': 'Krishe is an advanced agricultural platform that:\n- Analyzes soil parameters\n- Considers environmental conditions\n- Provides accurate crop recommendations\n- Helps optimize farming decisions\n- Supports sustainable farming practices.',


    # How Krishe Works
    'how does krishe work': 'Krishe works by:\n1. Analyzing your soil parameters (N, P, K)\n2. Considering environmental factors (temperature, rainfall, humidity, pH)\n3. Using advanced ML models to process data\n4. Providing tailored crop recommendations to maximize yield.',
    'how it work': 'Krishe works by:\n1. Analyzing your soil parameters (N, P, K)\n2. Considering environmental factors (temperature, rainfall, humidity, pH)\n3. Using advanced ML models to process data\n4. Providing tailored crop recommendations to maximize yield.',


    # Crop Prediction
    'predictions': 'Krishe can predict suitable crops based on:\n- Nitrogen content (N)\n- Phosphorus levels (P)\n- Potassium levels (K)\n- Temperature\n- Humidity\n- Soil pH levels\n- Rainfall\n- Historical crop performance.',
    'predict': 'Krishe can predict suitable crops based on:\n- Nitrogen content (N)\n- Phosphorus levels (P)\n- Potassium levels (K)\n- Temperature\n- Humidity\n- Soil pH levels\n- Rainfall\n- Historical crop performance.',


    # Benefits of Krishe
    'benefits': 'With Krishe, you can:\n- Get accurate crop recommendations\n- Maximize your yield potential\n- Save costs on fertilizers\n- Adopt sustainable farming practices\n- Stay updated with seasonal trends.',
    'benefit': 'With Krishe, you can:\n- Get accurate crop recommendations\n- Maximize your yield potential\n- Save costs on fertilizers\n- Adopt sustainable farming practices\n- Stay updated with seasonal trends.',

    # Soil Parameters
    'soil parameters': 'The soil parameters Krishe analyzes include:\n- Nitrogen (N)\n- Phosphorus (P)\n- Potassium (K)\n- pH level\n- Organic matter content\nThese are crucial for determining crop suitability.',
    'soil': 'The soil parameters Krishe analyzes include:\n- Nitrogen (N)\n- Phosphorus (P)\n- Potassium (K)\n- pH level\n- Organic matter content\nThese are crucial for determining crop suitability.',


    # Environmental Factors
    'environmental factors': 'Environmental factors considered by Krishe are:\n- Temperature\n- Rainfall patterns\n- Humidity levels\n- Seasonal trends\n- Regional weather forecasts.',
    'environment': 'Environmental factors considered by Krishe are:\n- Temperature\n- Rainfall patterns\n- Humidity levels\n- Seasonal trends\n- Regional weather forecasts.',
    'weather': 'Environmental factors considered by Krishe are:\n- Temperature\n- Rainfall patterns\n- Humidity levels\n- Seasonal trends\n- Regional weather forecasts.',


    # Contact and Support
    'contact': 'You can contact us through:\n- Email: support@krishe.com\n- Phone: +1-234-567-8900\n- Office: 123 Real Estate Street, City\nWe’re here to help you succeed!',
    'help': 'I can help you with:\n- Login/Registration\n- Soil analysis\n- Crop recommendations\n- Platform usage\n- Any questions about Krishe\nWhat would you like to know?',
    'support': 'You can contact us through:\n- Email:',

    # Farewell
    'bye': 'Goodbye! Thank you for using Krishe. Have a great day ahead!',
    'thank you': 'You’re welcome! If you have any more questions, feel free to ask. Happy farming!',
    'thanks': 'You’re welcome! If you have any more questions, feel free to ask. Happy farming!',
    'thank': 'You’re welcome! If you have any more questions, feel free to ask. Happy farming!',
}

    
    for key, value in responses.items():
        if key in message:
            return jsonify({"response": value})
    
    return jsonify({"response": "I'm not sure about that. Would you like to know about how to use Krishe, get crop recommendations, or learn about our soil analysis process?"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('predict_form'))
        
    if request.method == 'POST':
        try:
            fullname = request.form['fullname'].strip()
            email = request.form['email'].strip().lower()
            mobile = request.form['mobile'].strip()
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validation
            if not all([fullname, email, mobile, password, confirm_password]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('register'))

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('register'))

            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return redirect(url_for('register'))

            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered. Please use a different email.', 'danger')
                return redirect(url_for('register'))

            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = User(
                fullname=fullname,
                email=email,
                mobile=mobile,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {e}")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('predict_form'))
        
    if request.method == 'POST':
        try:
            username = request.form['username'].strip().lower()  # This could be email
            password = request.form['password']
            remember = 'remember' in request.form

            if not username or not password:
                flash('Please enter both email and password.', 'danger')
                return redirect(url_for('login'))

            # Check if input is email or username
            user = User.query.filter(
                (User.email == username) | (User.username == username)
            ).first()

            if user and check_password_hash(user.password, password):
                session['username'] = user.username
                session['user_id'] = user.id
                if remember:
                    session.permanent = True
                flash('Logged in successfully.', 'success')
                return redirect(url_for('predict_form'))
            else:
                flash('Invalid username/email or password.', 'danger')
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            print(f"Login error: {e}")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/predict_form')
@login_required
def predict_form():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@login_required
def predict():
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        if model is None or sc is None or ms is None:
            flash('Prediction service is currently unavailable.', 'danger')
            return redirect(url_for('predict_form'))

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
        
        return render_template('index.html', result=result)
    except Exception as e:
        flash('An error occurred during prediction. Please try again.', 'danger')
        print(f"Prediction error: {e}")
        return redirect(url_for('predict_form'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view_users')
def view_users():
    try:
        users = User.query.all()
        user_data = [
            {
                'id': user.id,
                'fullname': user.fullname,
                'email': user.email,
                'mobile': user.mobile,
                'username': user.username
            }
            for user in users
        ]
        return jsonify(user_data)
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return jsonify({"error": "Unable to fetch users from database."}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
