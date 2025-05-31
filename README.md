# WWE Wrestlers CRUD Application

Una aplicación CRUD para gestionar luchadores de WWE y sus títulos, desarrollada con Python, Flask y PostgreSQL.

## 🎯 Descripción del Proyecto

Este laboratorio consiste en una aplicación web que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre luchadores de WWE y sus títulos asociados. La aplicación utiliza Flask como framework web, SQLAlchemy como ORM y PostgreSQL como base de datos.

## 📁 Estructura del Proyecto

```
/
├── Fase_1/
│   └── diagrama_bd.pdf
├── Fase_2/
│   ├── contraseña.py
│   ├── contraseña.txt
│   ├── models.py
│   ├── inserts.py
│   ├── app.py
│   ├── DDL/
│       ├── schemas.sql
│       └── inserts.sql
│   └── templates/
│       ├── index.html
│       └── luchador_form.html
├── Fase_3/
│   └── analisis.pdf
└── requirements.txt
```

### Descripción de Archivos

- **Fase_1/diagrama_bd.pdf**: Diagrama Entidad-Relación de la base de datos
- **Fase_2/contraseña.py**: Script para configurar la contraseña de PostgreSQL
- **Fase_2/contraseña.txt**: Archivo generado que almacena la contraseña (no editar manualmente)
- **Fase_2/models.py**: Definición de modelos ORM y generación del esquema
- **Fase_2/inserts.py**: Script para insertar datos de prueba
- **Fase_2/app.py**: Aplicación Flask principal
- **Fase_2/DLL/**: Carpeta con scripts de create tables e inserts
- **Fase_2/templates/**: Plantillas HTML para la interfaz web
- **Fase_3/analisis.pdf**: Análisis reflexivo del proyecto

## 🛠️ Requisitos Previos

- **Python 3.8+**
- **PostgreSQL** (instalado y ejecutándose)
- **pip** para gestión de dependencias
- Usuario de PostgreSQL con privilegios para crear tablas
- **Base de datos `wwe_db` creada previamente**

### Crear la Base de Datos

Antes de ejecutar la aplicación, crear la base de datos en PostgreSQL:

```sql
CREATE DATABASE wwe_db;
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Luisfer2211/Lab3BD.git
cd Lab3BD
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Contraseña de PostgreSQL

```bash
python Fase_2/contraseña.py
```

Este script solicitará tu contraseña de PostgreSQL y generará el archivo `contraseña.txt`.

### 4. Generar Esquema de Base de Datos

```bash
python Fase_2/models.py
```

Esto creará las tablas necesarias en la base de datos `wwe_db` y generará el archivo `schema.sql` (el mismo que está dentro de `DDL/`).

### 5. Insertar Datos de Prueba

```bash
python Fase_2/inserts.py
```
Esto le agregará datos a las tablas necesarias en la base de datos `wwe_db` y generará el archivo `inserts.sql` (el mismo que está dentro de `DDL/`).

### 6. Ejecutar la Aplicación

```bash
python Fase_2/app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📋 Uso de la Aplicación

### Funcionalidades CRUD

1. **Ver Luchadores**: Lista todos los luchadores con sus títulos asociados
2. **Crear Luchador**: Formulario para agregar nuevos luchadores y asignar títulos
3. **Editar Luchador**: Modificar información existente y gestionar títulos
4. **Eliminar Luchador**: Remover luchadores y sus asociaciones

### Navegación

- **Página Principal**: `http://localhost:5000` - Lista de luchadores
- **Agregar Luchador**: Botón "Agregar nuevo luchador"
- **Editar**: Botón "Editar" junto a cada luchador
- **Eliminar**: Botón "Eliminar" junto a cada luchador

## 📦 Dependencias

Las dependencias están listadas en `requirements.txt`:

```
flask
flask-sqlalchemy
psycopg2-binary
```

## 🗄️ Base de Datos

La aplicación utiliza una vista (VIEW) que combina:
- Tabla de luchadores
- Tabla de títulos
- Tabla intermedia (relación muchos a muchos)

Esto permite mostrar eficientemente toda la información relevante en una sola consulta.

## 🔄 Flujo de Ejecución Completo

1. `pip install -r requirements.txt`
2. `python Fase_2/contraseña.py`
3. Verificar que existe la BD `wwe_db`
4. `python Fase_2/models.py`
5. `python Fase_2/inserts.py`
6. `python Fase_2/app.py`
7. Abrir navegador en `http://localhost:5000`

## 👥 Autores

- **Luis Palacios**
- **José Sánchez**

**Universidad del Valle de Guatemala**  
Facultad de Ingeniería – CC3088: Bases de Datos 1, Ciclo 1 2025

## 🔗 Enlaces

- **Repositorio**: [https://github.com/Luisfer2211/Lab3BD](https://github.com/Luisfer2211/Lab3BD)
- **Documentación adicional**: Ver archivos PDF en las carpetas Fase_1 y Fase_3

## 📝 Notas Importantes

- No editar manualmente el archivo `contraseña.txt`
- Asegurar que PostgreSQL esté ejecutándose antes de iniciar la aplicación
- La base de datos `wwe_db` debe existir antes de ejecutar `models.py`
- Los archivos `schema.sql` y `inserts.sql` se generan automáticamente y contienen toda la estructura de la base de datos

---
