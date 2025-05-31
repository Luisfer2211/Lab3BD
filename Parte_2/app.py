from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, CheckConstraint, UniqueConstraint, text
from sqlalchemy.orm import relationship
from datetime import datetime
import os

with open('contraseña.txt', 'r') as f:
    db_password = f.read().strip()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_password}@localhost:5432/wwe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

# Definición de tipos personalizados para validación
class PesoType(db.TypeDecorator):
    impl = db.Numeric(5, 2)
    
    def process_bind_param(self, value, dialect):
        if value <= 0 or value >= 300:
            raise ValueError("El peso debe estar entre 0.1 y 299.9 kg")
        return value

class AlturaType(db.TypeDecorator):
    impl = db.Numeric(4, 1)
    
    def process_bind_param(self, value, dialect):
        if value <= 100 or value >= 230:
            raise ValueError("La altura debe estar entre 101 y 229 cm")
        return value

# Modelos en el orden correcto para evitar problemas de dependencia
class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(Enum('PPV', 'Semanal', name='tipo_show'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    
    luchas = db.relationship('Lucha', back_populates='show')

class Lucha(db.Model):
    __tablename__ = 'lucha'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    tipo = db.Column(Enum('Singles', 'Tag Team', 'Royal Rumble', name='tipo_lucha'), nullable=False)
    estipulacion = db.Column(db.String(100))
    
    # Relación con Show
    show = db.relationship('Show', back_populates='luchas')
    
    @property
    def nombre_completo(self):
        return f"{self.show.nombre} - {self.tipo}"

class Luchador(db.Model):
    __tablename__ = 'luchador'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apodo = db.Column(db.String(100))
    peso_kg = db.Column(PesoType, nullable=False)
    altura_cm = db.Column(AlturaType, nullable=False)
    debut = db.Column(db.Date, nullable=False)
    
    titulos = relationship('LuchadorTitulo', back_populates='luchador', cascade='all, delete-orphan')
    participaciones = relationship('Participacion', back_populates='luchador', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Luchador {self.nombre}>'

class Titulo(db.Model):
    __tablename__ = 'titulo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    vigente = db.Column(db.Boolean, nullable=False, default=True)
    
    luchadores = relationship('LuchadorTitulo', back_populates='titulo')

class LuchadorTitulo(db.Model):
    __tablename__ = 'luchador_titulo'
    
    id = db.Column(db.Integer, primary_key=True)
    luchador_id = db.Column(db.Integer, db.ForeignKey('luchador.id'), nullable=False)
    titulo_id = db.Column(db.Integer, db.ForeignKey('titulo.id'), nullable=False)
    fecha_obtencion = db.Column(db.Date, nullable=False)
    fecha_perdida = db.Column(db.Date)
    
    luchador = relationship('Luchador', back_populates='titulos')
    titulo = relationship('Titulo', back_populates='luchadores')
    
    __table_args__ = (
        UniqueConstraint('luchador_id', 'titulo_id', 'fecha_obtencion', name='uix_luchador_titulo_fecha'),
        CheckConstraint('fecha_perdida IS NULL OR fecha_perdida > fecha_obtencion', name='check_fechas_titulo'),
    )

class Participacion(db.Model):
    __tablename__ = 'participacion'
    
    luchador_id = db.Column(db.Integer, db.ForeignKey('luchador.id'), primary_key=True)
    lucha_id = db.Column(db.Integer, db.ForeignKey('lucha.id'), primary_key=True)
    resultado = db.Column(Enum('Ganó', 'Perdió', 'Empate', name='resultado_enum'), nullable=False)
    
    luchador = relationship('Luchador', back_populates='participaciones')
    lucha = relationship('Lucha')

# Vista para el índice
class LuchadoresConTitulos(db.Model):
    __tablename__ = 'luchadores_con_titulos'
    __table_args__ = {'info': dict(is_view=True)}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apodo = db.Column(db.String(100))
    peso_kg = db.Column(db.Numeric(5, 2))
    altura_cm = db.Column(db.Numeric(4, 1))
    debut = db.Column(db.Date)
    titulos_actuales = db.Column(db.ARRAY(db.String))
    titulos_historicos = db.Column(db.ARRAY(db.String))

# Funciones de ayuda
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    except ValueError:
        return None

# Validaciones a nivel aplicación
def validate_luchador_form(data):
    errors = []
    
    # Validar campos requeridos
    if not data.get('nombre'):
        errors.append("El nombre es obligatorio")
    
    # Validar fechas
    if not data.get('debut'):
        errors.append("La fecha de debut es obligatoria")
    elif parse_date(data['debut']) is None:
        errors.append("Formato de fecha inválido (debe ser AAAA-MM-DD)")
    
    # Validar tipos personalizados
    try:
        peso = float(data.get('peso_kg', 0))
        if peso <= 0 or peso >= 300:
            errors.append("El peso debe estar entre 0.1 y 299.9 kg")
    except ValueError:
        errors.append("El peso debe ser un número")
    
    try:
        altura = float(data.get('altura_cm', 0))
        if altura <= 100 or altura >= 230:
            errors.append("La altura debe estar entre 101 y 229 cm")
    except ValueError:
        errors.append("La altura debe ser un número")
    
    return errors

# Crear la vista si no existe
def create_view():
    with app.app_context():
        # Usar text() para envolver la consulta SQL
        db.session.execute(text("""
        CREATE OR REPLACE VIEW luchadores_con_titulos AS
        SELECT 
            l.id,
            l.nombre,
            l.apodo,
            l.peso_kg,
            l.altura_cm,
            l.debut,
            ARRAY_AGG(t.nombre) FILTER (WHERE lt.fecha_perdida IS NULL) AS titulos_actuales,
            ARRAY_AGG(t.nombre) FILTER (WHERE lt.fecha_perdida IS NOT NULL) AS titulos_historicos
        FROM luchador l
        LEFT JOIN luchador_titulo lt ON l.id = lt.luchador_id
        LEFT JOIN titulo t ON t.id = lt.titulo_id
        GROUP BY l.id;
        """))
        db.session.commit()

# Rutas CRUD
@app.route('/')
def index():
    # Usando la vista para el índice
    luchadores = db.session.query(LuchadoresConTitulos).all()
    return render_template('index.html', luchadores=luchadores)

@app.route('/luchadores/new', methods=['GET', 'POST'])
def new_luchador():
    titulos_disponibles = Titulo.query.all()
    luchas_disponibles = db.session.query(Lucha).join(Show).all()
    
    if request.method == 'POST':
        data = request.form
        errors = validate_luchador_form(data)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            try:
                # Crear luchador
                luchador = Luchador(
                    nombre=data['nombre'],
                    apodo=data['apodo'],
                    peso_kg=float(data['peso_kg']),
                    altura_cm=float(data['altura_cm']),
                    debut=parse_date(data['debut'])
                )
                db.session.add(luchador)
                db.session.flush()  # Para obtener el ID
                
                # Asociar títulos (tabla intermedia)
                for key in request.form:
                    if key.startswith('titulo_id_'):
                        index = key.split('_')[-1]
                        titulo_id = request.form[key]
                        fecha_obtencion = parse_date(request.form[f'fecha_obtencion_{index}'])
                        fecha_perdida = parse_date(request.form[f'fecha_perdida_{index}'])
                        
                        if titulo_id and fecha_obtencion:
                            luchador_titulo = LuchadorTitulo(
                                luchador_id=luchador.id,
                                titulo_id=int(titulo_id),
                                fecha_obtencion=fecha_obtencion,
                                fecha_perdida=fecha_perdida
                            )
                            db.session.add(luchador_titulo)
                
                # Asociar participaciones (tabla intermedia)
                for key in request.form:
                    if key.startswith('lucha_id_'):
                        index = key.split('_')[-1]
                        lucha_id = request.form[key]
                        resultado = request.form[f'resultado_{index}']
                        
                        if lucha_id and resultado:
                            participacion = Participacion(
                                luchador_id=luchador.id,
                                lucha_id=int(lucha_id),
                                resultado=resultado
                            )
                            db.session.add(participacion)
                
                db.session.commit()
                flash('Luchador creado exitosamente!', 'success')
                return redirect(url_for('index'))
            
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear luchador: {str(e)}', 'danger')
    
    return render_template('luchador_form.html', 
                          titulos=titulos_disponibles, 
                          luchas=luchas_disponibles,
                          luchador=None)

@app.route('/luchadores/<int:id>/edit', methods=['GET', 'POST'])
def edit_luchador(id):
    luchador = Luchador.query.get_or_404(id)
    titulos_disponibles = Titulo.query.all()
    luchas_disponibles = db.session.query(Lucha).join(Show).all()
    
    if request.method == 'POST':
        data = request.form
        errors = validate_luchador_form(data)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            try:
                # Actualizar luchador
                luchador.nombre = data['nombre']
                luchador.apodo = data['apodo']
                luchador.peso_kg = float(data['peso_kg'])
                luchador.altura_cm = float(data['altura_cm'])
                luchador.debut = parse_date(data['debut'])
                
                # Eliminar relaciones existentes
                LuchadorTitulo.query.filter_by(luchador_id=id).delete()
                Participacion.query.filter_by(luchador_id=id).delete()
                
                # Asociar títulos
                for key in request.form:
                    if key.startswith('titulo_id_'):
                        index = key.split('_')[-1]
                        titulo_id = request.form[key]
                        fecha_obtencion = parse_date(request.form[f'fecha_obtencion_{index}'])
                        fecha_perdida = parse_date(request.form[f'fecha_perdida_{index}'])
                        
                        if titulo_id and fecha_obtencion:
                            luchador_titulo = LuchadorTitulo(
                                luchador_id=luchador.id,
                                titulo_id=int(titulo_id),
                                fecha_obtencion=fecha_obtencion,
                                fecha_perdida=fecha_perdida
                            )
                            db.session.add(luchador_titulo)
                
                # Asociar participaciones
                for key in request.form:
                    if key.startswith('lucha_id_'):
                        index = key.split('_')[-1]
                        lucha_id = request.form[key]
                        resultado = request.form[f'resultado_{index}']
                        
                        if lucha_id and resultado:
                            participacion = Participacion(
                                luchador_id=luchador.id,
                                lucha_id=int(lucha_id),
                                resultado=resultado
                            )
                            db.session.add(participacion)
                
                db.session.commit()
                flash('Luchador actualizado exitosamente!', 'success')
                return redirect(url_for('index'))
            
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar luchador: {str(e)}', 'danger')
    
    return render_template('luchador_form.html', 
                          luchador=luchador,
                          titulos=titulos_disponibles, 
                          luchas=luchas_disponibles)

@app.route('/luchadores/<int:id>/delete', methods=['POST'])
def delete_luchador(id):
    try:
        luchador = Luchador.query.get_or_404(id)
        db.session.delete(luchador)
        db.session.commit()
        flash('Luchador eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar luchador: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

# Iniciar la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_view()
    app.run(debug=True)