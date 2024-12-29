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

# # # # # # # #
# # COMMAND # #
# # # # # # # #

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pymysql
flask run
