from flask import Flask, url_for, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#Configuranfo base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)


class Participantes(db.Model):
    tipo_documento = db.Column(db.String(4))
    numero_documento = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(100))
    apellido =  db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.String(20))
    recibio_premio = db.Column(db.String(2))
    premio = db.Column(db.String(100))

    def __repr__(self):
        return '<Participantes %r>' % self.nombres






@app.route('/', methods=['GET', 'POST'])
def inicial():
    if request.method == 'POST':
        return 'Post'
    else:
        flash('You were successfully logged in', 'error')
        return render_template('index.html')

#url_for('function')
#request.form['username']
#redirect(url_for('login'))
