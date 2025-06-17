from flask import Flask

app = Flask('__name__')

app.route('/registro')
def registro():
    return 'registro'


if __name__ == '__main__':
    app.run(debug=True)