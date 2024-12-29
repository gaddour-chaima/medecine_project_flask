from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration pour la session
app.secret_key = "your_secret_key_here"

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/medecin_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration pour les fichiers uploadés
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Charger le modèle IA (modèle brainT_detect.h5)
model = load_model('brainT_detect.h5')

db = SQLAlchemy(app)

# Modèle pour les utilisateurs


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Modèle pour les rendez-vous


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='appointments')
    prediction_result = db.Column(db.String(100), nullable=True)

# Route pour la page d'accueil


@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
    return redirect(url_for('login'))

# Route pour la connexion


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('home'))
        flash('Invalid email or password.')
    return render_template('index.html')

# Route pour l'enregistrement


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        telephone = request.form['telephone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        new_user = User(
            firstname=firstname, lastname=lastname,
            email=email, telephone=telephone, password=password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists.')
    return render_template('register.html')

# Route pour les rendez-vous


@app.route('/make_appointment', methods=['GET', 'POST'])
def make_appointment():
    if 'user_id' not in session:
        flash('Please log in to make an appointment.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            new_appointment = Appointment(
                firstname=firstname, lastname=lastname,
                email=email, date=date, user_id=user.id, prediction_result=""
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment added successfully!")
        except ValueError:
            flash("Invalid date format.")
    appointments = Appointment.query.filter_by(
        user_id=user.id).order_by(Appointment.date).all()
    return render_template('clients.html', appointments=appointments)

# Route pour l'upload de l'image et la prédiction


@app.route('/ai_upload/<int:appointment_id>', methods=['GET', 'POST'])
def ai_upload(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)

        # Check if there's already a prediction result
        if appointment.prediction_result:
            result = appointment.prediction_result
        else:
            result = None

        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No file part.')
                return redirect(request.url)
            file = request.files['image']
            if file.filename == '':
                flash('No selected file.')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Preprocess image (resize, grayscale, etc.)
                img = Image.open(filepath)
                img = img.resize((200, 200))  # Resize the image to 200x200
                img = img.convert('L')  # Convert to grayscale

                image_array = np.array(img)
                image_array = np.expand_dims(
                    image_array, axis=-1)  # Add channel dimension
                image_array = np.expand_dims(
                    image_array, axis=0)  # Add batch dimension
                image_array = image_array / 255.0  # Normalize the image

                # Prediction
                prediction = model.predict(image_array)
                result_class = ['glioma', 'meningioma', 'notumor', 'pituitary']
                predicted_class = result_class[np.argmax(prediction)]

                # Save the result to the database
                appointment.prediction_result = predicted_class
                db.session.commit()

                # Flash the result message
                flash(f"Prediction Result: {predicted_class}", 'success')

                # Update the result to show in the template
                result = predicted_class

        # Render the template and pass the result
        return render_template('ai_upload.html', result=result, appointment_id=appointment_id)

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('ai_upload', appointment_id=appointment_id))


# Vérifier si le fichier est valide


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes supplémentaires


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/ourService')
def our_service():
    return render_template('ourService.html')


@app.route('/clients')
def clients():
    return redirect(url_for('make_appointment'))


@app.route('/about')
def about():
    return render_template('about.html')

# Création des tables


def create_tables():
    db.create_all()


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    create_tables()
    app.run(debug=True)
