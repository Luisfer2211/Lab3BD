from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint, UniqueConstraint, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import event, DDL
from sqlalchemy.schema import CreateTable, CreateIndex, DropTable, MetaData
from sqlalchemy.sql.ddl import CreateSchema
import os

with open("contraseña.txt", "r", encoding="utf-8") as f:
    password = f.read().strip()

DATABASE_URI = f'postgresql://postgres:{password}@localhost:5432/wwe_db'

Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=True)

# 2. Definición de modelos
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

# 3. Función para generar schema.sql CORREGIDA
def generate_schema_file():
    """Genera el archivo schema.sql con todo el DDL corregido"""
    schema_content = []
    
    # 1. Crear tipos ENUM
    schema_content.append("-- Creación de tipos ENUM personalizados")
    schema_content.append("CREATE TYPE tipo_show AS ENUM ('PPV', 'Semanal');")
    schema_content.append("CREATE TYPE tipo_lucha AS ENUM ('Singles', 'Tag Team', 'Royal Rumble');")
    schema_content.append("CREATE TYPE resultado_enum AS ENUM ('Ganó', 'Perdió', 'Empate');\n")
    
    # 2. Crear tablas con todas las restricciones
    schema_content.append("-- Creación de tablas con restricciones")
    tables = [
        Luchador.__table__,
        Show.__table__,
        Titulo.__table__,
        Lucha.__table__,
        Participacion.__table__,
        LuchadorTitulo.__table__
    ]
    
    for table in tables:
        # Generar CREATE TABLE con todas las constraints
        create_table = str(CreateTable(table).compile(engine)).strip()
        schema_content.append(create_table + ";")
        
        # Añadir índices adicionales (CORRECCIÓN: obtener nombres de columnas)
        for constraint in table.constraints:
            if isinstance(constraint, UniqueConstraint):
                # Obtener nombres de columnas en lugar de objetos
                column_names = [col.name for col in constraint.columns]
                schema_content.append(
                    f"ALTER TABLE {table.name} ADD CONSTRAINT {constraint.name} "
                    f"UNIQUE ({', '.join(column_names)};"
                )
    
    # 3. Crear vista
    schema_content.append("\n-- Creación de vista para el índice")
    schema_content.append("""
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
""")
    
    # 4. Escribir a archivo
    with open('schema.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(schema_content))
    
    print("✅ Archivo schema.sql generado exitosamente!")

# 4. Crear la vista en la base de datos
@event.listens_for(Base.metadata, 'after_create')
def create_view(target, connection, **kw):
    connection.execute(DDL("""
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

# 5. Crear estructura de base de datos
def create_database_structure():
    print("🧩 Creando estructura de base de datos...")
    
    try:
        # Crear todas las tablas
        Base.metadata.create_all(engine)
        
        # Generar archivo schema.sql
        generate_schema_file()
        
        print("✅ ¡Estructura creada exitosamente! Tablas:")
        print("   - luchador")
        print("   - show")
        print("   - titulo")
        print("   - lucha")
        print("   - participacion")
        print("   - luchador_titulo")
        print("   - Vista: luchadores_con_titulos")
        print("   - Archivo schema.sql generado")
    
    except Exception as e:
        print(f"❌ Error durante la creación: {e}")
        import traceback
        traceback.print_exc()

# 6. Ejecutar
if __name__ == "__main__":
    create_database_structure()