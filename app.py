import os
from dotenv import load_dotenv
from flask import Flask,render_template

#Cargar variable de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/registro')
def registro():
    return render_template('registro.html')


if __name__ == '__main__':
    app.run(debug=True)