import sqlite3
from datetime import datetime
import win32print
from PIL import Image, ImageFilter

# =========================================
# CONFIGURACION
# =========================================

def obtener_configuracion():

    conexion = sqlite3.connect("parqueadero.db")

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT nombre,
           nit,
           direccion,
           telefono,
           mensaje_ticket
    FROM configuracion
    WHERE id=1
    """)

    datos = cursor.fetchone()

    conexion.close()

    return datos


# =========================================
# IMPRIMIR RAW
# =========================================

def imprimir_directo(datos):

    impresora = win32print.GetDefaultPrinter()

    hprinter = win32print.OpenPrinter(
        impresora
    )

    try:

        win32print.StartDocPrinter(
            hprinter,
            1,
            ("Ticket", None, "RAW")
        )

        win32print.StartPagePrinter(
            hprinter
        )

        win32print.WritePrinter(
            hprinter,
            datos
        )

        win32print.EndPagePrinter(
            hprinter
        )

        win32print.EndDocPrinter(
            hprinter
        )

    finally:

        win32print.ClosePrinter(
            hprinter
        )

# =========================================
# TICKET ENTRADA
# =========================================

def generar_ticket_entrada_directo(placa):

    nombre, nit, direccion, telefono, mensaje = obtener_configuracion()

    conexion = sqlite3.connect("parqueadero.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT hora_entrada
    FROM vehiculos
    WHERE placa=?
    ORDER BY id DESC
    LIMIT 1
    """, (placa,))

    datos = cursor.fetchone()

    conexion.close()

    hora_entrada = datetime.strptime(
        datos[0],
        "%Y-%m-%d %H:%M:%S"
    )

    entrada_texto = hora_entrada.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    ticket = bytearray()

    # Inicializar impresora
    ticket += b'\x1b\x40'

    # ------------------------------------
    # TITULO SUPERIOR (REEMPLAZA EL LOGO)
    # ------------------------------------

    ticket += b'\x1b\x61\x01'      # Centrado

    ticket += b'\x1d\x21\x11'      # Texto grande (doble ancho y alto)

    ticket += b'PARQUEADERO\n'

    ticket += b'MOTOS LA 11\n'

    ticket += b'\x1d\x21\x00'      # Volver a tamaño normal

    ticket += b'\n'

    # Centrado
    ticket += b'\x1b\x61\x01'

    # Nombre grande
    ticket += b'\x1d\x21\x00'

    ticket += f"{nombre}\n".encode(
        "cp850",
        errors="replace"
    )

    # Normal
    ticket += b'\x1d\x21\x00'

    ticket += f"NIT: {nit}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"{direccion}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"{telefono}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'--------------------------------\n'

    # Título
    ticket += b'\x1d\x21\x00'
    ticket += b'TICKET ENTRADA\n'
    ticket += b'\x1d\x21\x00'

    ticket += b'--------------------------------\n'

    # Placa
    ticket += b'PLACA\n'

    ticket += b'\x1b\x61\x01'
    ticket += b'\x1d\x21\x01'

    ticket += f"{placa}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'\x1d\x21\x00'

    ticket += b'--------------------------------\n'

    ticket += f"ENTRADA\n{entrada_texto}\n\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'--------------------------------\n'

    ticket += mensaje.encode(
        "cp850",
        errors="replace"
    )

    ticket += b'\n\n'

    # Corte
    ticket += b'\x1d\x56\x00'

    imprimir_directo(ticket)
# =========================================
# TICKET SALIDA
# =========================================

def generar_ticket_salida_directo(
    placa,
    tiempo,
    total
):

    nombre, nit, direccion, telefono, mensaje = obtener_configuracion()

    conexion = sqlite3.connect(
        "parqueadero.db"
    )

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT hora_entrada,
           hora_salida
    FROM vehiculos
    WHERE placa=?
    ORDER BY id DESC
    LIMIT 1
    """, (placa,))

    datos = cursor.fetchone()

    conexion.close()

    hora_entrada = datetime.strptime(
        datos[0],
        "%Y-%m-%d %H:%M:%S"
    )

    hora_salida = datetime.strptime(
        datos[1],
        "%Y-%m-%d %H:%M:%S"
    )

    entrada_texto = hora_entrada.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    salida_texto = hora_salida.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    ticket = bytearray()

    # ------------------------------------
    # Inicializar impresora
    # ------------------------------------

    ticket += b'\x1b\x40'

    # ------------------------------------
    # TITULO SUPERIOR (REEMPLAZA EL LOGO)
    # ------------------------------------

    ticket += b'\x1b\x61\x01'      # Centrado

    ticket += b'\x1d\x21\x11'      # Texto grande (doble ancho y alto)

    ticket += b'PARQUEADERO\n'

    ticket += b'MOTOS LA 11\n'

    ticket += b'\x1d\x21\x00'      # Volver a tamaño normal

    ticket += b'\n'

    # ------------------------------------
    # Centrado
    # ------------------------------------

    ticket += b'\x1b\x61\x01'

    # ------------------------------------
    # Nombre grande
    # ------------------------------------

    ticket += b'\x1d\x21\x00'

    ticket += f"{nombre}\n".encode(
        "cp850",
        errors="replace"
    )

    # ------------------------------------
    # Datos empresa
    # ------------------------------------

    ticket += b'\x1d\x21\x00'

    ticket += f"NIT: {nit}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"{direccion}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"{telefono}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'--------------------------------\n'

    # ------------------------------------
    # TITULO
    # ------------------------------------

    ticket += b'\x1d\x21\x01'

    ticket += b'TICKET SALIDA\n'

    ticket += b'\x1d\x21\x00'

    ticket += b'--------------------------------\n'

    # ------------------------------------
    # PLACA
    # ------------------------------------

    ticket += b'PLACA\n'

    ticket += b'\x1d\x21\x01'

    ticket += f"{placa}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'\x1d\x21\x00'

    ticket += b'--------------------------------\n'

    # ------------------------------------
    # HORAS
    # ------------------------------------

    ticket += f"ENTRADA\n{entrada_texto}\n\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"SALIDA\n{salida_texto}\n\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += f"TIEMPO\n{tiempo}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'--------------------------------\n'

    # ------------------------------------
    # TOTAL
    # ------------------------------------

    ticket += b'\x1d\x21\x01'

    ticket += b'TOTAL\n'

    ticket += b'\x1d\x21\x11'

    ticket += f"${total:,}\n".encode(
        "cp850",
        errors="replace"
    )

    ticket += b'\x1d\x21\x00'

    ticket += b'--------------------------------\n'

    # ------------------------------------
    # MENSAJE
    # ------------------------------------

    ticket += mensaje.encode(
        "cp850",
        errors="replace"
    )

    ticket += b'\n\n'

    # ------------------------------------
    # Corte
    # ------------------------------------

    ticket += b'\x1d\x56\x00'

    imprimir_directo(ticket)