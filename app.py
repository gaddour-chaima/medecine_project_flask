from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Remplacez par une clé secrète pour la session

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/medecin_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de l'utilisateur
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Référence à l'utilisateur
    user = db.relationship('User', backref='appointments')  # Relation avec l'utilisateur

# Page d'accueil (redirection vers la connexion)
@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
    return redirect(url_for('login'))

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérification de l'utilisateur dans la base de données
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('User not found with this email. Please try again.')
            return redirect(url_for('login'))

        # Vérification si le mot de passe est correct (sans hachage)
        if user.password == password:
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.')

    return render_template('index.html')  # Page de connexion

# Route pour la page de registre
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
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('register'))

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            telephone=telephone,
            password=password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists. Please choose a different one.')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')

    return render_template('register.html')

# Route pour les rendez-vous
@app.route('/make_appointment', methods=['GET', 'POST'])
def make_appointment():
    if 'user_id' not in session:  # Vérifier que l'utilisateur est connecté
        flash('You must be logged in to make an appointment.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])  # Récupérer l'utilisateur connecté

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        date_str = request.form['date']

        try:
            # Conversion de la date string en datetime
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

            # Création d'un nouvel enregistrement
            new_appointment = Appointment(
                firstname=firstname,
                lastname=lastname,
                email=email,
                date=date,
                user_id=user.id  # Associer le rendez-vous à l'utilisateur connecté
            )

            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment added successfully!")
        except ValueError:
            flash("Invalid date format. Please use the correct format.")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}")

    # Récupération des rendez-vous de l'utilisateur connecté
    appointments = Appointment.query.filter_by(user_id=user.id).order_by(Appointment.date).all()

    # Retourner la page avec les rendez-vous
    return render_template('clients.html', appointments=appointments)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Vide toutes les informations de session
    return redirect(url_for('home'))
# Routes supplémentaires pour les pages statiques
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/ourService')
def our_service():
    return render_template('ourService.html')

@app.route('/clients')
def clients():
    return redirect(url_for('make_appointment'))  # Rediriger vers la route des rendez-vous

@app.route('/about')
def about():
    return render_template('about.html')

# Lancer l'application
if __name__ == "__main__":
    db.create_all()  # Crée les tables de la base de données
    app.run(debug=True)
