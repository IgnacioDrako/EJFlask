from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Se crea la instancia de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar sesiones
# Base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Se crea la tabla usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    administrador = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '<Usuario %r>' % self.id

# Se crea la tabla tarea
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # quien crea la tarea
    nombre_usuario = db.relationship('Usuario', backref=db.backref('tareas', lazy=True)) 
    def __repr__(self):
        return '<Tarea %r>' % self.id

with app.app_context():
    db.create_all()

# Ruta 1: inicio
@app.route('/')
def inicio():
    usuarios = Usuario.query.all()
    if not usuarios:
        return "No hay usuarios en la base de datos"
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Ruta para verificar el login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    usuario = Usuario.query.filter_by(nombre=username, contrasena=password).first()
    if usuario:
        session['user_id'] = usuario.id
        session['admin'] = usuario.administrador
        return jsonify(success=True)
    else:
        return jsonify(success=False)

# Ruta gestor de tareas
@app.route('/tareas/<int:tarea_id>')
def ver_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    tarea = Tarea.query.get_or_404(tarea_id)
    usuario = Usuario.query.get(tarea.id_usuario)
    
    tarea_info = {
        'id': tarea.id,
        'nombre': tarea.nombre,
        'descripcion': tarea.descripcion,
        'fecha_creacion': tarea.fecha_creacion,
        'creador': usuario.nombre
    }
    
    return render_template('ver_tarea.html', tarea=tarea_info)

@app.route('/tareas')
def tareas():
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    if session['admin']:
        tareas = Tarea.query.all()
    else:
        tareas = Tarea.query.filter_by(id_usuario=session['user_id']).all()
    
    tareas_info = []
    for tarea in tareas:
        usuario = Usuario.query.get(tarea.id_usuario)
        tarea_info = {
            'id': tarea.id,
            'nombre': tarea.nombre,
            'descripcion': tarea.descripcion,
            'fecha_creacion': tarea.fecha_creacion,
            'creador': usuario.nombre,
            'id_usuario': tarea.id_usuario
        }
        tareas_info.append(tarea_info)
    
    return render_template('tareas.html', tareas=tareas_info, admin=session['admin'])

# Ruta para crear una nueva tarea
@app.route('/tareas/nueva', methods=['POST'])
def nueva_tarea():
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    data = request.get_json()
    nueva_tarea = Tarea(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        id_usuario=session['user_id']
    )
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify(success=True)

# Ruta para editar una tarea
@app.route('/tareas/editar/<int:tarea_id>', methods=['GET', 'POST'])
def editar_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    tarea = Tarea.query.get_or_404(tarea_id)
    
    if request.method == 'POST':
        tarea.nombre = request.form['nombre']
        tarea.descripcion = request.form['descripcion']
        tarea.fecha_creacion = datetime.utcnow()  # Actualizar la fecha de creación
        db.session.commit()
        return redirect(url_for('ver_tarea', tarea_id=tarea.id))
    
    return render_template('editar_tarea.html', tarea=tarea)

# Ruta para eliminar una tarea
@app.route('/tareas/eliminar/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    tarea = Tarea.query.get_or_404(tarea_id)
    
    if session['admin'] or tarea.id_usuario == session['user_id']:
        db.session.delete(tarea)
        db.session.commit()
        return redirect(url_for('tareas'))
    else:
        return redirect(url_for('inicio'))

# Ruta info de usuario
@app.route('/usuario')
def usuario():
    if 'user_id' not in session:
        return redirect(url_for('inicio'))
    
    usuario = Usuario.query.get(session['user_id'])
    if not usuario:
        return "No hay información del usuario en la base de datos"
    
    admin = session.get('admin', False)
    return render_template('usuario.html', usuario=usuario, admin=admin)

# Ruta de gestor de usuarios
@app.route('/usuarios')
def G_usuarios():
    if 'user_id' not in session or not session.get('admin'):
        return render_template('noadmin.html')
    
    usuarios = Usuario.query.all()
    if not usuarios:
        return "No hay usuarios en la base de datos"
    
    admin = session.get('admin', False)
    return render_template('G_usuarios.html', usuarios=usuarios, admin=admin)

# Ruta para ver un usuario
@app.route('/usuarios/<int:usuario_id>')
def ver_usuario(usuario_id):
    if 'user_id' not in session or not session.get('admin'):
        return render_template('noadmin.html')
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    return render_template('ver_usuario.html', usuario=usuario)

# Ruta para crear un nuevo usuario
@app.route('/usuarios/nuevo', methods=['POST'])
def nuevo_usuario():
    if 'user_id' not in session or not session.get('admin'):
        return render_template('noadmin.html')
    
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        contrasena=data['contrasena']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(success=True)

# Ruta para editar un usuario
@app.route('/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    if 'user_id' not in session or not session.get('admin'):
        return render_template('noadmin.html')
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        usuario.contrasena = request.form['contrasena']
        usuario.administrador = 'administrador' in request.form
        db.session.commit()
        return redirect(url_for('ver_usuario', usuario_id=usuario.id))
    
    return render_template('editar_usuario.html', usuario=usuario)

# Ruta para eliminar un usuario
@app.route('/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if 'user_id' not in session or not session.get('admin'):
        return render_template('noadmin.html')
    
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('G_usuarios'))

if __name__ == '__main__':
    # debug=True es útil para desarrollo (muestra errores en tiempo real).
    app.run(debug=True)