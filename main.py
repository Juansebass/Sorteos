from flask import Flask, url_for, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#Configuranfo base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.sqlite3'
db = SQLAlchemy(app)

#Creando modelo para guardar los participantesen la base de datos
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

#Creando modelo para guardar los premios
class Premios(db.Model):
    codigo =db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)

    def __repr__(self):
        return '<Premios %r>' % self.codigo


@app.route('/', methods=['GET', 'POST'])
def inicial():
    if request.method == 'POST':
        #Verificando que todos los campos se hayan llenado
        if not request.form['nombres'] or not request.form['apellidos'] or not request.form['documento'] or not request.form['numero'] or not request.form['nacimiento']:
            flash('Por favor llena todos los campos', 'error')
        else:
            #Verificando que no tenga la misma identificación de otro
            identificacion = request.form['numero']
            if Participantes.query.filter_by(numero_documento=identificacion).count() > 0:
                flash('El participante ya se encuentra en el sistema', 'error')
            else:
                #Agregando participante a la base de datos
                persona = Participantes(tipo_documento=request.form['documento'],numero_documento=request.form['numero'],
                nombres=request.form['nombres'],apellido=request.form['apellidos'],fecha_nacimiento=request.form['nacimiento'], recibio_premio='NO',premio='')

                db.session.add(persona)
                db.session.commit()

                flash('Se ha ingresado el participante')

    #Obteniendo todos los participantes para mostrarlos en tabla
    participantes = Participantes.query.all()


    return render_template('index.html', participantes = participantes)

#url_for('function')
#request.form['username']
#redirect(url_for('login'))


#Ruta para eliminar un participante
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    participante = Participantes.query.get(id)
    if participante.recibio_premio == "SI":
         flash("No se puede eliminar el participante, ya recibió premio", 'recibido')
    else:
        db.session.delete(participante)
        db.session.commit()
        flash("Se ha eliminado el participante", 'eliminado')

    return redirect(url_for('inicial'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        persona = Participantes.query.get(request.form.get('id'))



        persona.tipo_documento = request.form['documento']
        persona.numero_documento = request.form['numero']
        persona.nombres = request.form['nombres']
        persona.apellido = request.form['apellidos']
        persona.fecha_nacimiento = request.form['nacimiento']

        db.session.commit()
        flash("Se ha editado el participante", 'editado')

        return redirect(url_for('inicial'))


@app.route('/sorteo', methods=['GET', 'POST'])
def sorteo():

    premios = Premios.query.all()
    return render_template('sorteo.html', premios = premios)
