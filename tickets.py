from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import mm

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime

import sqlite3

import os

import win32api

import win32print


# =========================================
# FUENTES
# =========================================

try:

    pdfmetrics.registerFont(
        TTFont(
            'TicketBold',
            'arialbd.ttf'
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            'Ticket',
            'arial.ttf'
        )
    )

    FUENTE_NORMAL = "Ticket"
    FUENTE_BOLD = "TicketBold"

except:

    FUENTE_NORMAL = "Helvetica"
    FUENTE_BOLD = "Helvetica-Bold"


# =========================================
# IMPRIMIR PDF
# =========================================
def imprimir_pdf(nombre_pdf):

    try:

        impresora = win32print.GetDefaultPrinter()

        win32api.ShellExecute(
            0,
            "printto",
            nombre_pdf,
            f'"{impresora}"',
            ".",
            0
        )

    except Exception as e:

        print("Error al imprimir:", e)

# =========================================
# CONFIGURACION
# =========================================

def obtener_configuracion():

    conexion = sqlite3.connect(
        "parqueadero.db"
    )

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
# ENCABEZADO
# =========================================

def dibujar_encabezado(c, ancho, y):

    nombre, nit, direccion, telefono, mensaje = obtener_configuracion()

    logo_path = "logos/logo.png"

    # =====================================
    # LOGO
    # =====================================

    if os.path.exists(logo_path):

        logo_width = 40 * mm
        logo_height = 25 * mm

        x_logo = (ancho - logo_width) / 2

        c.drawImage(
            logo_path,
            x_logo,
            y - logo_height,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask='auto'
        )

        y -= 27 * mm

    # =====================================
    # NOMBRE
    # =====================================

    c.setFillColorRGB(0, 0, 0)

    c.setFont(
        FUENTE_BOLD,
        11
    )

    c.drawCentredString(
        ancho / 2,
        y,
        nombre
    )

    y -= 5 * mm

    # =====================================
    # NIT
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawCentredString(
        ancho / 2,
        y,
        f"NIT: {nit}"
    )

    y -= 4 * mm

    # =====================================
    # DIRECCION
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawCentredString(
        ancho / 2,
        y,
        direccion
    )

    y -= 4 * mm

    # =====================================
    # TELEFONO
    # =====================================

    c.drawCentredString(
        ancho / 2,
        y,
        telefono
    )

    y -= 6 * mm

    return y


# =========================================
# TICKET ENTRADA
# =========================================

def generar_ticket_entrada(placa):

    nombre, nit, direccion, telefono, mensaje = obtener_configuracion()

    # =====================================
    # OBTENER HORA REAL
    # =====================================

    conexion = sqlite3.connect(
        "parqueadero.db"
    )

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

    nombre_pdf = f"ticket_entrada_{placa}.pdf"

    ancho = 58 * mm
    alto = 85 * mm

    c = canvas.Canvas(
        nombre_pdf,
        pagesize=(ancho, alto)
    )

    y = alto - 4 * mm

    # =====================================
    # ENCABEZADO
    # =====================================

    y = dibujar_encabezado(
        c,
        ancho,
        y
    )

    # =====================================
    # TITULO
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        10
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "TICKET ENTRADA"
    )

    y -= 7 * mm

    # =====================================
    # DATOS
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        9
    )

    c.drawString(
        5 * mm,
        y,
        f"PLACA: {placa}"
    )

    y -= 6 * mm

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawString(
        5 * mm,
        y,
        f"ENTRADA: {entrada_texto}"
    )

    y -= 8 * mm

    # =====================================
    # MENSAJE
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawCentredString(
        ancho / 2,
        y,
        mensaje
    )

    c.save()

    imprimir_pdf(nombre_pdf)


# =========================================
# TICKET SALIDA
# =========================================

def generar_ticket_salida(
    placa,
    tiempo,
    total
):

    nombre, nit, direccion, telefono, mensaje = obtener_configuracion()

    # =====================================
    # OBTENER HORAS REALES
    # =====================================

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

    datos_horas = cursor.fetchone()

    conexion.close()

    hora_entrada = datetime.strptime(
        datos_horas[0],
        "%Y-%m-%d %H:%M:%S"
    )

    hora_salida = datetime.strptime(
        datos_horas[1],
        "%Y-%m-%d %H:%M:%S"
    )

    entrada_texto = hora_entrada.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    salida_texto = hora_salida.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    nombre_pdf = f"ticket_salida_{placa}.pdf"

    ancho = 58 * mm
    alto = 100 * mm

    c = canvas.Canvas(
        nombre_pdf,
        pagesize=(ancho, alto)
    )

    y = alto - 4 * mm

    # =====================================
    # ENCABEZADO
    # =====================================

    y = dibujar_encabezado(
        c,
        ancho,
        y
    )

    # =====================================
    # TITULO
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        10
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "TICKET SALIDA"
    )

    y -= 7 * mm

    # =====================================
    # PLACA
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        9
    )

    c.drawString(
        5 * mm,
        y,
        f"PLACA: {placa}"
    )

    y -= 6 * mm

    # =====================================
    # ENTRADA
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawString(
        5 * mm,
        y,
        f"ENTRADA: {entrada_texto}"
    )

    y -= 5 * mm

    # =====================================
    # SALIDA
    # =====================================

    c.drawString(
        5 * mm,
        y,
        f"SALIDA: {salida_texto}"
    )

    y -= 5 * mm

    # =====================================
    # TIEMPO
    # =====================================

    c.drawString(
        5 * mm,
        y,
        f"TIEMPO: {tiempo}"
    )

    y -= 8 * mm

    # =====================================
    # TOTAL
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        11
    )

    c.drawCentredString(
        ancho / 2,
        y,
        f"TOTAL: ${total:,}"
    )

    y -= 8 * mm

    # =====================================
    # MENSAJE
    # =====================================

    c.setFont(
        FUENTE_BOLD,
        8
    )

    c.drawCentredString(
        ancho / 2,
        y,
        mensaje
    )

    c.save()

    imprimir_pdf(nombre_pdf)