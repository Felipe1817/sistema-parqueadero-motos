import sqlite3

conexion = sqlite3.connect("parqueadero.db")

cursor = conexion.cursor()

# =========================================
# TABLA VEHICULOS
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehiculos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    descripcion TEXT,

    placa TEXT,

    tipo TEXT,

    hora_entrada TEXT,

    hora_salida TEXT,

    tiempo TEXT,

    total INTEGER,

    estado TEXT
)
""")

# =========================================
# TABLA CONFIGURACION
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracion(

    id INTEGER PRIMARY KEY,

    nombre TEXT,

    direccion TEXT,

    telefono TEXT,

    nit TEXT,

    propietario TEXT,

    mensaje_ticket TEXT,

    tarifa_hora INTEGER
)
""")

# =========================================
# INSERTAR CONFIGURACION
# =========================================

cursor.execute("""
SELECT * FROM configuracion
WHERE id=1
""")

existe = cursor.fetchone()

if not existe:

    cursor.execute("""
    INSERT INTO configuracion(
        id,
        nombre,
        direccion,
        telefono,
        nit,
        propietario,
        mensaje_ticket,
        tarifa_hora
    )
    VALUES(1,?,?,?,?,?,?,?)
    """, (

        "PARQUEADERO MOTOS LA 11",

        "Calle 11 #5-79 Neiva Huila",

        "+57 3232752006",

        "901234567-1",

        "Juan David Pastrana Santos",

        "Gracias por preferirnos",

        2400
    ))

conexion.commit()

conexion.close()

print("Base de datos creada correctamente")