import os
from dotenv import load_dotenv
from flask import Flask,render_template
from models import db,Users

#Cargar variable de entorno
load_dotenv()

DATABASE_PATH = os.environ.get('DATABASE_PATH')


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
db.init_app(app)

#Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def abour():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)