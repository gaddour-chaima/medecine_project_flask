Médical Appointment System (Flask)
Description
Le projet "Médical Appointment System" est une application web construite avec Flask qui permet aux utilisateurs de prendre des rendez-vous médicaux, avec la possibilité de prédire des résultats en fonction des informations fournies lors de la prise de rendez-vous. Cette application est intégrée à une base de données relationnelle utilisant SQLAlchemy pour la gestion des données.

Fonctionnalités principales :
Création de rendez-vous : Permet aux utilisateurs de planifier un rendez-vous médical en soumettant leur prénom, nom, adresse e-mail et date de rendez-vous.
Prédiction de résultats : Basé sur les informations fournies lors de la prise de rendez-vous, un résultat de prédiction est généré et enregistré (par exemple, des résultats relatifs à une analyse médicale).
Gestion des utilisateurs : Système de gestion des utilisateurs avec possibilité de suivre les rendez-vous associés à chaque utilisateur.
Base de données : Utilisation de SQLAlchemy pour la gestion de la base de données relationnelle.

git clone https://github.com/gaddour-chaima/medecine_project_flask.git
cd medecine_project_flask

version python : 3.10

# # # # # # # # #
# #  COMMAND  # #
# # # # # # # # #

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pymysql
flask run


# # # # # # # # #
# #  DataBase # #
# # # # # # # # #

-- Créer la base de données
CREATE DATABASE medecin_db;

-- Sélectionner la base de données
USE medecin_db;

-- Créer la table 'users'
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telephone VARCHAR(15) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Créer la table 'appointments'
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    date DATETIME NOT NULL,
    user_id INT NOT NULL,
    prediction_result VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
