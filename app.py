import os
from dotenv import load_dotenv
from flask import Flask,render_template, request,flash,redirect,url_for
from werkzeug.security import generate_password_hash
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

@app.route('/registro',methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passwordr = request.form.get('passwordr')

        #Validaciones
        if len(username) < 6:
            flash('El username debe tener al menos 6 caracteres','danger')
            return redirect(url_for('registro'))
        elif password != passwordr:
            flash('Los password no coinciden','danger')
            return redirect(url_for('registro'))
        
         # Verifica si el usuario ya existe
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Este nombre de usuario ya está registrado.', 'danger')
            return redirect(url_for('registro'))

        #Agregar al usuario
        hashed_password = generate_password_hash(password)
        user = Users(username=username,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        #Redirigir al Login
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))


    return render_template('registro.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def abour():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)