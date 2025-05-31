-- Creación de tipos ENUM personalizados
CREATE TYPE tipo_show AS ENUM ('PPV', 'Semanal');
CREATE TYPE tipo_lucha AS ENUM ('Singles', 'Tag Team', 'Royal Rumble');
CREATE TYPE resultado_enum AS ENUM ('Ganó', 'Perdió', 'Empate');

-- Creación de tablas con restricciones
CREATE TABLE luchador (
	id SERIAL NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	apodo VARCHAR(100), 
	peso_kg NUMERIC(5, 2) NOT NULL, 
	altura_cm NUMERIC(4, 1) NOT NULL, 
	debut DATE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uix_nombre_apodo UNIQUE (nombre, apodo), 
	CONSTRAINT check_peso CHECK (peso_kg > 0 AND peso_kg < 300), 
	CONSTRAINT check_altura CHECK (altura_cm > 100 AND altura_cm < 230)
);
ALTER TABLE luchador ADD CONSTRAINT uix_nombre_apodo UNIQUE (nombre, apodo;
CREATE TABLE show (
	id SERIAL NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	tipo tipo_show NOT NULL, 
	fecha DATE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);
ALTER TABLE show ADD CONSTRAINT None UNIQUE (nombre;
CREATE TABLE titulo (
	id SERIAL NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	vigente BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);
ALTER TABLE titulo ADD CONSTRAINT None UNIQUE (nombre;
CREATE TABLE lucha (
	id SERIAL NOT NULL, 
	show_id INTEGER NOT NULL, 
	tipo tipo_lucha NOT NULL, 
	estipulacion VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(show_id) REFERENCES show (id)
);
CREATE TABLE participacion (
	luchador_id INTEGER NOT NULL, 
	lucha_id INTEGER NOT NULL, 
	resultado resultado_enum NOT NULL, 
	PRIMARY KEY (luchador_id, lucha_id), 
	CONSTRAINT uix_luchador_lucha UNIQUE (luchador_id, lucha_id), 
	FOREIGN KEY(luchador_id) REFERENCES luchador (id), 
	FOREIGN KEY(lucha_id) REFERENCES lucha (id)
);
ALTER TABLE participacion ADD CONSTRAINT uix_luchador_lucha UNIQUE (luchador_id, lucha_id;
CREATE TABLE luchador_titulo (
	id SERIAL NOT NULL, 
	luchador_id INTEGER NOT NULL, 
	titulo_id INTEGER NOT NULL, 
	fecha_obtencion DATE NOT NULL, 
	fecha_perdida DATE, 
	PRIMARY KEY (id), 
	CONSTRAINT uix_luchador_titulo_fecha UNIQUE (luchador_id, titulo_id, fecha_obtencion), 
	CONSTRAINT check_fechas_titulo CHECK (fecha_perdida IS NULL OR fecha_perdida > fecha_obtencion), 
	FOREIGN KEY(luchador_id) REFERENCES luchador (id), 
	FOREIGN KEY(titulo_id) REFERENCES titulo (id)
);
ALTER TABLE luchador_titulo ADD CONSTRAINT uix_luchador_titulo_fecha UNIQUE (luchador_id, titulo_id, fecha_obtencion;

-- Creación de vista para el índice

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
