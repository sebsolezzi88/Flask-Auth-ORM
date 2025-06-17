import os
from dotenv import load_dotenv
from flask import Flask,render_template, request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from models import db,Users,Tareas

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


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if  not username or not password:
            flash('Debe completar todos los campos', 'danger')
            return redirect(url_for('login'))
        
        #Verificar si el usuario esta en la base de datos
        user = db.session.execute(
            db.select(Users).filter_by(username=username)
        ).scalar_one_or_none()

        if user is None:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('login'))

        # Verificar contraseña
        if not check_password_hash(user.password, password):
            flash('Contraseña incorrecta', 'danger')
            return redirect(url_for('login'))

        # Iniciar sesión (almacenar en session)
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Has iniciado sesión con éxito', 'success')
        return redirect(url_for('tareas'))  
    
    return render_template('login.html')

@app.route('/tareas',methods=['GET','POST'])
def tareas():
    #Si no esta logeado se redirige
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        
        if titulo == "" or descripcion == "":
            flash("Debe completar ambos campos","danger")
            return redirect(url_for('tareas'))
        
        #Crear tarea para agregar a la base de datos
        tarea = Tareas(titulo=titulo,
                       descripcion=descripcion,
                       user_id=session['user_id'])
        db.session.add(tarea)
        db.session.commit()
        flash("Tarea agregada","success")
    
    #Buscar tareas que ingreso el usuario
    tareas = Tareas.query.filter_by(user_id=session['user_id']).all()

    return render_template('tareas.html',logged_in=True,username=session['username'],tareas=tareas)

@app.route('/about')
def about():
    return render_template('about.html',logged_in=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)