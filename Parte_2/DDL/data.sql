-- Insertar 10 luchadores
INSERT INTO luchador (nombre, apodo, peso_kg, altura_cm, debut) VALUES
('John Cena', 'El Rapero Mayor', 114.0, 185.0, '2000-06-27'),
('Randy Orton', 'La Víbora', 113.0, 196.0, '2002-04-25'),
('The Rock', 'La Piedra', 118.0, 196.0, '1996-03-10'),
('Stone Cold Steve Austin', 'Serpiente Cascabel', 114.0, 188.0, '1995-12-18'),
('Triple H', 'The Game', 116.0, 193.0, '1995-04-30'),
('Undertaker', 'El Enterrador', 136.0, 208.0, '1990-11-22'),
('Rey Mysterio', 'El Ultimate Underdog', 79.0, 168.0, '1992-04-01'),
('Brock Lesnar', 'La Bestia', 130.0, 191.0, '2000-03-19'),
('Roman Reigns', 'El Jefe Tribal', 120.0, 191.0, '2010-08-19'),
('Seth Rollins', 'El Visionario', 98.0, 185.0, '2005-09-01');

-- Insertar 5 shows
INSERT INTO show (nombre, tipo, fecha) VALUES
('WrestleMania 30', 'PPV', '2014-04-06'),
('SummerSlam 2015', 'PPV', '2015-08-23'),
('Royal Rumble 2016', 'PPV', '2016-01-24'),
('Survivor Series 2017', 'PPV', '2017-11-19'),
('Monday Night Raw', 'Semanal', '2020-01-06');

-- Insertar 8 títulos
INSERT INTO titulo (nombre, vigente) VALUES
('Campeonato Mundial Peso Pesado', TRUE),
('Campeonato de los Estados Unidos', TRUE),
('Campeonato Intercontinental', TRUE),
('Campeonato en Parejas', TRUE),
('Campeonato de la División Femenina', TRUE),
('Campeonato de Europa', FALSE),
('Campeonato Hardcore', FALSE),
('Campeonato de la WWE', TRUE);

-- Insertar 15 luchas
INSERT INTO lucha (show_id, tipo, estipulacion) VALUES
(1, 'Singles', 'Sin descalificación'),
(1, 'Tag Team', 'Eliminación'),
(1, 'Singles', 'Ladder match'),
(2, 'Singles', NULL),
(2, 'Tag Team', 'Tornado'),
(2, 'Singles', 'Iron Man'),
(3, 'Royal Rumble', '30-man Royal Rumble'),
(3, 'Singles', NULL),
(3, 'Singles', 'Last Man Standing'),
(4, 'Tag Team', 'Eliminación por equipos'),
(4, 'Singles', NULL),
(4, 'Singles', 'Falls Count Anywhere'),
(5, 'Singles', NULL),
(5, 'Tag Team', NULL),
(5, 'Singles', 'Cage match');

-- Insertar 30 participaciones (demostrando relaciones múltiples)
INSERT INTO participacion (luchador_id, lucha_id, resultado) VALUES
(1, 1, 'Ganó'),
(1, 3, 'Perdió'),
(1, 7, 'Ganó'),
(1, 10, 'Perdió'),
(1, 14, 'Ganó'),
(2, 1, 'Perdió'),
(2, 5, 'Ganó'),
(2, 8, 'Empate'),
(2, 12, 'Perdió'),
(3, 2, 'Ganó'),
(3, 4, 'Perdió'),
(3, 9, 'Ganó'),
(4, 2, 'Ganó'),
(4, 6, 'Perdió'),
(4, 11, 'Empate'),
(5, 2, 'Perdió'),
(5, 6, 'Ganó'),
(5, 13, 'Perdió'),
(6, 3, 'Ganó'),
(6, 7, 'Perdió'),
(6, 15, 'Ganó'),
(7, 5, 'Perdió'),
(7, 9, 'Ganó'),
(7, 14, 'Perdió'),
(8, 4, 'Ganó'),
(8, 10, 'Perdió'),
(8, 15, 'Perdió'),
(9, 7, 'Perdió'),
(10, 14, 'Ganó');

-- Insertar 20 posesiones de títulos (demostrando relaciones múltiples)
INSERT INTO luchador_titulo (luchador_id, titulo_id, fecha_obtencion, fecha_perdida) VALUES
(1, 1, '2005-04-03', '2005-06-26'),
(1, 1, '2006-01-29', '2006-04-30'),
(1, 2, '2004-07-04', '2004-10-03'),
(1, 8, '2013-10-27', '2014-04-06'),
(1, 8, '2014-06-29', '2015-03-29'),
(2, 1, '2004-12-14', '2005-01-09'),
(2, 3, '2003-12-14', '2004-03-14'),
(2, 8, '2007-10-07', '2008-04-27'),
(2, 8, '2013-08-18', '2013-12-15'),
(3, 1, '1998-12-29', '1999-01-24'),
(3, 8, '2000-04-30', '2000-06-25'),
(3, 8, '2001-04-01', '2001-07-23'),
(4, 1, '1997-08-03', '1997-10-05'),
(4, 8, '1998-03-29', '1999-03-28'),
(4, 8, '2001-04-01', '2001-04-02'),
(5, 1, '2002-03-17', '2002-08-25'),
(5, 4, '2009-06-28', '2009-09-13'),
(5, 8, '2002-09-02', '2003-12-14'),
(6, 1, '1997-08-03', '1997-10-05'),
(6, 8, '2007-04-01', '2008-03-30');
