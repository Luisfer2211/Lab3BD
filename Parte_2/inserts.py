from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import os

# ------------------------------------------------------------------
# 1. Configuración de conexión y modelos (idénticos a tu archivo "creates")
# ------------------------------------------------------------------

# Cambia esta URI si tu usuario, contraseña o base de datos son distintos
DATABASE_URI = 'postgresql://postgres:lol@localhost:5432/wwe_db'

from sqlalchemy import (
    Column, Integer, String, Date, Numeric,
    ForeignKey, CheckConstraint, UniqueConstraint,
    Boolean, Enum
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)

class Luchador(Base):
    __tablename__ = 'luchador'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apodo = Column(String(100))
    peso_kg = Column(Numeric(5,2), nullable=False)
    altura_cm = Column(Numeric(4,1), nullable=False)
    debut = Column(Date, nullable=False)

    participaciones = relationship('Participacion', back_populates='luchador')
    titulos = relationship('LuchadorTitulo', back_populates='luchador')

    __table_args__ = (
        UniqueConstraint('nombre', 'apodo', name='uix_nombre_apodo'),
        CheckConstraint('peso_kg > 0 AND peso_kg < 300', name='check_peso'),
        CheckConstraint('altura_cm > 100 AND altura_cm < 230', name='check_altura'),
    )

class Show(Base):
    __tablename__ = 'show'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    tipo = Column(Enum('PPV', 'Semanal', name='tipo_show', create_type=True), nullable=False)
    fecha = Column(Date, nullable=False)

    luchas = relationship('Lucha', back_populates='show')

class Titulo(Base):
    __tablename__ = 'titulo'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    vigente = Column(Boolean, nullable=False, default=True)

    luchadores = relationship('LuchadorTitulo', back_populates='titulo')

class Lucha(Base):
    __tablename__ = 'lucha'

    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    tipo = Column(Enum('Singles', 'Tag Team', 'Royal Rumble', name='tipo_lucha', create_type=True), nullable=False)
    estipulacion = Column(String(100))

    show = relationship('Show', back_populates='luchas')
    participaciones = relationship('Participacion', back_populates='lucha')

class Participacion(Base):
    __tablename__ = 'participacion'

    luchador_id = Column(Integer, ForeignKey('luchador.id'), primary_key=True)
    lucha_id = Column(Integer, ForeignKey('lucha.id'), primary_key=True)
    resultado = Column(Enum('Ganó', 'Perdió', 'Empate', name='resultado_enum', create_type=True), nullable=False)

    luchador = relationship('Luchador', back_populates='participaciones')
    lucha = relationship('Lucha', back_populates='participaciones')

    __table_args__ = (
        UniqueConstraint('luchador_id', 'lucha_id', name='uix_luchador_lucha'),
    )

class LuchadorTitulo(Base):
    __tablename__ = 'luchador_titulo'

    id = Column(Integer, primary_key=True)
    luchador_id = Column(Integer, ForeignKey('luchador.id'), nullable=False)
    titulo_id = Column(Integer, ForeignKey('titulo.id'), nullable=False)
    fecha_obtencion = Column(Date, nullable=False)
    fecha_perdida = Column(Date)

    luchador = relationship('Luchador', back_populates='titulos')
    titulo = relationship('Titulo', back_populates='luchadores')

    __table_args__ = (
        UniqueConstraint('luchador_id', 'titulo_id', 'fecha_obtencion', name='uix_luchador_titulo_fecha'),
        CheckConstraint('fecha_perdida IS NULL OR fecha_perdida > fecha_obtencion', name='check_fechas_titulo'),
    )

# ------------------------------------------------------------------
# 2. Función para insertar los datos automáticamente vía SQLAlchemy
# ------------------------------------------------------------------

def insert_data():
    session = SessionLocal()

    # 2.1. Insertar 10 luchadores
    luchadores = [
        Luchador(nombre='John Cena', apodo='El Rapero Mayor', peso_kg=114.0, altura_cm=185.0, debut=date(2000,6,27)),
        Luchador(nombre='Randy Orton', apodo='La Víbora', peso_kg=113.0, altura_cm=196.0, debut=date(2002,4,25)),
        Luchador(nombre='The Rock', apodo='La Piedra', peso_kg=118.0, altura_cm=196.0, debut=date(1996,3,10)),
        Luchador(nombre='Stone Cold Steve Austin', apodo='Serpiente Cascabel', peso_kg=114.0, altura_cm=188.0, debut=date(1995,12,18)),
        Luchador(nombre='Triple H', apodo='The Game', peso_kg=116.0, altura_cm=193.0, debut=date(1995,4,30)),
        Luchador(nombre='Undertaker', apodo='El Enterrador', peso_kg=136.0, altura_cm=208.0, debut=date(1990,11,22)),
        Luchador(nombre='Rey Mysterio', apodo='El Ultimate Underdog', peso_kg=79.0, altura_cm=168.0, debut=date(1992,4,1)),
        Luchador(nombre='Brock Lesnar', apodo='La Bestia', peso_kg=130.0, altura_cm=191.0, debut=date(2000,3,19)),
        Luchador(nombre='Roman Reigns', apodo='El Jefe Tribal', peso_kg=120.0, altura_cm=191.0, debut=date(2010,8,19)),
        Luchador(nombre='Seth Rollins', apodo='El Visionario', peso_kg=98.0, altura_cm=185.0, debut=date(2005,9,1)),
    ]
    session.add_all(luchadores)
    session.flush()  # para asignar IDs

    # 2.2. Insertar 5 shows
    shows = [
        Show(nombre='WrestleMania 30', tipo='PPV', fecha=date(2014,4,6)),
        Show(nombre='SummerSlam 2015', tipo='PPV', fecha=date(2015,8,23)),
        Show(nombre='Royal Rumble 2016', tipo='PPV', fecha=date(2016,1,24)),
        Show(nombre='Survivor Series 2017', tipo='PPV', fecha=date(2017,11,19)),
        Show(nombre='Monday Night Raw', tipo='Semanal', fecha=date(2020,1,6)),
    ]
    session.add_all(shows)
    session.flush()

    # 2.3. Insertar 8 títulos
    titulos = [
        Titulo(nombre='Campeonato Mundial Peso Pesado', vigente=True),
        Titulo(nombre='Campeonato de los Estados Unidos', vigente=True),
        Titulo(nombre='Campeonato Intercontinental', vigente=True),
        Titulo(nombre='Campeonato en Parejas', vigente=True),
        Titulo(nombre='Campeonato de la División Femenina', vigente=True),
        Titulo(nombre='Campeonato de Europa', vigente=False),
        Titulo(nombre='Campeonato Hardcore', vigente=False),
        Titulo(nombre='Campeonato de la WWE', vigente=True),
    ]
    session.add_all(titulos)
    session.flush()

    # 2.4. Insertar 15 luchas
    # Para asignar show_id, asumo que los shows se insertaron en orden y sus IDs corresponden a 1..5
    luchas = [
        Lucha(show_id=1, tipo='Singles', estipulacion='Sin descalificación'),
        Lucha(show_id=1, tipo='Tag Team', estipulacion='Eliminación'),
        Lucha(show_id=1, tipo='Singles', estipulacion='Ladder match'),
        Lucha(show_id=2, tipo='Singles', estipulacion=None),
        Lucha(show_id=2, tipo='Tag Team', estipulacion='Tornado'),
        Lucha(show_id=2, tipo='Singles', estipulacion='Iron Man'),
        Lucha(show_id=3, tipo='Royal Rumble', estipulacion='30-man Royal Rumble'),
        Lucha(show_id=3, tipo='Singles', estipulacion=None),
        Lucha(show_id=3, tipo='Singles', estipulacion='Last Man Standing'),
        Lucha(show_id=4, tipo='Tag Team', estipulacion='Eliminación por equipos'),
        Lucha(show_id=4, tipo='Singles', estipulacion=None),
        Lucha(show_id=4, tipo='Singles', estipulacion='Falls Count Anywhere'),
        Lucha(show_id=5, tipo='Singles', estipulacion=None),
        Lucha(show_id=5, tipo='Tag Team', estipulacion=None),
        Lucha(show_id=5, tipo='Singles', estipulacion='Cage match'),
    ]
    session.add_all(luchas)
    session.flush()

    # 2.5. Insertar 30 participaciones
    # Asumo que los IDs de luchador y lucha corresponden a su orden de inserción
    participaciones_data = [
        # John Cena (luchador_id=1)
        (1, 1, 'Ganó'),
        (1, 3, 'Perdió'),
        (1, 7, 'Ganó'),
        (1, 10, 'Perdió'),
        (1, 14, 'Ganó'),
        # Randy Orton (luchador_id=2)
        (2, 1, 'Perdió'),
        (2, 5, 'Ganó'),
        (2, 8, 'Empate'),
        (2, 12, 'Perdió'),
        # The Rock (luchador_id=3)
        (3, 2, 'Ganó'),
        (3, 4, 'Perdió'),
        (3, 9, 'Ganó'),
        # Stone Cold (luchador_id=4)
        (4, 2, 'Ganó'),
        (4, 6, 'Perdió'),
        (4, 11, 'Empate'),
        # Triple H (luchador_id=5)
        (5, 2, 'Perdió'),
        (5, 6, 'Ganó'),
        (5, 13, 'Perdió'),
        # Undertaker (luchador_id=6)
        (6, 3, 'Ganó'),
        (6, 7, 'Perdió'),
        (6, 15, 'Ganó'),
        # Rey Mysterio (luchador_id=7)
        (7, 5, 'Perdió'),
        (7, 9, 'Ganó'),
        (7, 14, 'Perdió'),
        # Brock Lesnar (luchador_id=8)
        (8, 4, 'Ganó'),
        (8, 10, 'Perdió'),
        (8, 15, 'Perdió'),
        # Roman Reigns (luchador_id=9)
        (9, 7, 'Perdió'),
        # Seth Rollins (luchador_id=10)
        (10, 14, 'Ganó'),
    ]

    participaciones = [
        Participacion(luchador_id=lut_id, lucha_id=luc_id, resultado=res) 
        for (lut_id, luc_id, res) in participaciones_data
    ]
    session.add_all(participaciones)
    session.flush()

    # 2.6. Insertar 20 posesiones de títulos
    posesiones_data = [
        # John Cena (luchador_id=1)
        (1, 1, date(2005,4,3), date(2005,6,26)),
        (1, 1, date(2006,1,29), date(2006,4,30)),
        (1, 2, date(2004,7,4), date(2004,10,3)),
        (1, 8, date(2013,10,27), date(2014,4,6)),
        (1, 8, date(2014,6,29), date(2015,3,29)),
        # Randy Orton (luchador_id=2)
        (2, 1, date(2004,12,14), date(2005,1,9)),
        (2, 3, date(2003,12,14), date(2004,3,14)),
        (2, 8, date(2007,10,7), date(2008,4,27)),
        (2, 8, date(2013,8,18), date(2013,12,15)),
        # The Rock (luchador_id=3)
        (3, 1, date(1998,12,29), date(1999,1,24)),
        (3, 8, date(2000,4,30), date(2000,6,25)),
        (3, 8, date(2001,4,1), date(2001,7,23)),
        # Stone Cold (luchador_id=4)
        (4, 1, date(1997,8,3), date(1997,10,5)),
        (4, 8, date(1998,3,29), date(1999,3,28)),
        (4, 8, date(2001,4,1), date(2001,4,2)),
        # Triple H (luchador_id=5)
        (5, 1, date(2002,3,17), date(2002,8,25)),
        (5, 4, date(2009,6,28), date(2009,9,13)),
        (5, 8, date(2002,9,2), date(2003,12,14)),
        # Undertaker (luchador_id=6)
        (6, 1, date(1997,8,3), date(1997,10,5)),
        (6, 8, date(2007,4,1), date(2008,3,30)),
    ]

    posesiones = [
        LuchadorTitulo(
            luchador_id=lut_id,
            titulo_id=tit_id,
            fecha_obtencion=fec_obt,
            fecha_perdida=fec_per
        )
        for (lut_id, tit_id, fec_obt, fec_per) in posesiones_data
    ]
    session.add_all(posesiones)

    # Finalmente, commit de todo
    session.commit()
    session.close()
    print("✅ Inserción de datos completada.")

# ------------------------------------------------------------------
# 3. Función para generar el archivo data.sql con los INSERTs en crudo
# ------------------------------------------------------------------

def generate_data_file():
    """Crea (o sobrescribe) data.sql con todos los INSERTs en crudo."""
    lines = []

    # 3.1. INSERTs para luchador
    lines.append("-- Insertar 10 luchadores")
    lines.append("INSERT INTO luchador (nombre, apodo, peso_kg, altura_cm, debut) VALUES")
    lines.append("('John Cena', 'El Rapero Mayor', 114.0, 185.0, '2000-06-27'),")
    lines.append("('Randy Orton', 'La Víbora', 113.0, 196.0, '2002-04-25'),")
    lines.append("('The Rock', 'La Piedra', 118.0, 196.0, '1996-03-10'),")
    lines.append("('Stone Cold Steve Austin', 'Serpiente Cascabel', 114.0, 188.0, '1995-12-18'),")
    lines.append("('Triple H', 'The Game', 116.0, 193.0, '1995-04-30'),")
    lines.append("('Undertaker', 'El Enterrador', 136.0, 208.0, '1990-11-22'),")
    lines.append("('Rey Mysterio', 'El Ultimate Underdog', 79.0, 168.0, '1992-04-01'),")
    lines.append("('Brock Lesnar', 'La Bestia', 130.0, 191.0, '2000-03-19'),")
    lines.append("('Roman Reigns', 'El Jefe Tribal', 120.0, 191.0, '2010-08-19'),")
    lines.append("('Seth Rollins', 'El Visionario', 98.0, 185.0, '2005-09-01');\n")

    # 3.2. INSERTs para show
    lines.append("-- Insertar 5 shows")
    lines.append("INSERT INTO show (nombre, tipo, fecha) VALUES")
    lines.append("('WrestleMania 30', 'PPV', '2014-04-06'),")
    lines.append("('SummerSlam 2015', 'PPV', '2015-08-23'),")
    lines.append("('Royal Rumble 2016', 'PPV', '2016-01-24'),")
    lines.append("('Survivor Series 2017', 'PPV', '2017-11-19'),")
    lines.append("('Monday Night Raw', 'Semanal', '2020-01-06');\n")

    # 3.3. INSERTs para titulo
    lines.append("-- Insertar 8 títulos")
    lines.append("INSERT INTO titulo (nombre, vigente) VALUES")
    lines.append("('Campeonato Mundial Peso Pesado', TRUE),")
    lines.append("('Campeonato de los Estados Unidos', TRUE),")
    lines.append("('Campeonato Intercontinental', TRUE),")
    lines.append("('Campeonato en Parejas', TRUE),")
    lines.append("('Campeonato de la División Femenina', TRUE),")
    lines.append("('Campeonato de Europa', FALSE),")
    lines.append("('Campeonato Hardcore', FALSE),")
    lines.append("('Campeonato de la WWE', TRUE);\n")

    # 3.4. INSERTs para lucha
    lines.append("-- Insertar 15 luchas")
    lines.append("INSERT INTO lucha (show_id, tipo, estipulacion) VALUES")
    lines.append("(1, 'Singles', 'Sin descalificación'),")
    lines.append("(1, 'Tag Team', 'Eliminación'),")
    lines.append("(1, 'Singles', 'Ladder match'),")
    lines.append("(2, 'Singles', NULL),")
    lines.append("(2, 'Tag Team', 'Tornado'),")
    lines.append("(2, 'Singles', 'Iron Man'),")
    lines.append("(3, 'Royal Rumble', '30-man Royal Rumble'),")
    lines.append("(3, 'Singles', NULL),")
    lines.append("(3, 'Singles', 'Last Man Standing'),")
    lines.append("(4, 'Tag Team', 'Eliminación por equipos'),")
    lines.append("(4, 'Singles', NULL),")
    lines.append("(4, 'Singles', 'Falls Count Anywhere'),")
    lines.append("(5, 'Singles', NULL),")
    lines.append("(5, 'Tag Team', NULL),")
    lines.append("(5, 'Singles', 'Cage match');\n")

    # 3.5. INSERTs para participacion
    lines.append("-- Insertar 30 participaciones (demostrando relaciones múltiples)")
    lines.append("INSERT INTO participacion (luchador_id, lucha_id, resultado) VALUES")
    lines.append("(1, 1, 'Ganó'),")
    lines.append("(1, 3, 'Perdió'),")
    lines.append("(1, 7, 'Ganó'),")
    lines.append("(1, 10, 'Perdió'),")
    lines.append("(1, 14, 'Ganó'),")
    lines.append("(2, 1, 'Perdió'),")
    lines.append("(2, 5, 'Ganó'),")
    lines.append("(2, 8, 'Empate'),")
    lines.append("(2, 12, 'Perdió'),")
    lines.append("(3, 2, 'Ganó'),")
    lines.append("(3, 4, 'Perdió'),")
    lines.append("(3, 9, 'Ganó'),")
    lines.append("(4, 2, 'Ganó'),")
    lines.append("(4, 6, 'Perdió'),")
    lines.append("(4, 11, 'Empate'),")
    lines.append("(5, 2, 'Perdió'),")
    lines.append("(5, 6, 'Ganó'),")
    lines.append("(5, 13, 'Perdió'),")
    lines.append("(6, 3, 'Ganó'),")
    lines.append("(6, 7, 'Perdió'),")
    lines.append("(6, 15, 'Ganó'),")
    lines.append("(7, 5, 'Perdió'),")
    lines.append("(7, 9, 'Ganó'),")
    lines.append("(7, 14, 'Perdió'),")
    lines.append("(8, 4, 'Ganó'),")
    lines.append("(8, 10, 'Perdió'),")
    lines.append("(8, 15, 'Perdió'),")
    lines.append("(9, 7, 'Perdió'),")
    lines.append("(10, 14, 'Ganó');\n")

    # 3.6. INSERTs para luchador_titulo
    lines.append("-- Insertar 20 posesiones de títulos (demostrando relaciones múltiples)")
    lines.append("INSERT INTO luchador_titulo (luchador_id, titulo_id, fecha_obtencion, fecha_perdida) VALUES")
    lines.append("(1, 1, '2005-04-03', '2005-06-26'),")
    lines.append("(1, 1, '2006-01-29', '2006-04-30'),")
    lines.append("(1, 2, '2004-07-04', '2004-10-03'),")
    lines.append("(1, 8, '2013-10-27', '2014-04-06'),")
    lines.append("(1, 8, '2014-06-29', '2015-03-29'),")
    lines.append("(2, 1, '2004-12-14', '2005-01-09'),")
    lines.append("(2, 3, '2003-12-14', '2004-03-14'),")
    lines.append("(2, 8, '2007-10-07', '2008-04-27'),")
    lines.append("(2, 8, '2013-08-18', '2013-12-15'),")
    lines.append("(3, 1, '1998-12-29', '1999-01-24'),")
    lines.append("(3, 8, '2000-04-30', '2000-06-25'),")
    lines.append("(3, 8, '2001-04-01', '2001-07-23'),")
    lines.append("(4, 1, '1997-08-03', '1997-10-05'),")
    lines.append("(4, 8, '1998-03-29', '1999-03-28'),")
    lines.append("(4, 8, '2001-04-01', '2001-04-02'),")
    lines.append("(5, 1, '2002-03-17', '2002-08-25'),")
    lines.append("(5, 4, '2009-06-28', '2009-09-13'),")
    lines.append("(5, 8, '2002-09-02', '2003-12-14'),")
    lines.append("(6, 1, '1997-08-03', '1997-10-05'),")
    lines.append("(6, 8, '2007-04-01', '2008-03-30');\n")

    # Escribir todo al archivo data.sql (lo sobrescribe si ya existe)
    with open('data.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print("✅ Archivo data.sql generado exitosamente.")


# ------------------------------------------------------------------
# 4. Punto de entrada
# ------------------------------------------------------------------

if __name__ == "__main__":
    # 4.1. Primero asegurarse de que la estructura exista (tablas, enums, etc.)
    #      Si aún no ejecutaste tu código de create_all, descomenta la línea siguiente:
    # Base.metadata.create_all(engine)

    # 4.2. Generar data.sql
    generate_data_file()

    # 4.3. Insertar los datos en la base de datos
    insert_data()
