import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFrame,
    QPushButton
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        # ==================================
        # ESTILOS GENERALES
        # ==================================

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25,25,25,25)
        self.layout.setSpacing(20)

        # ==================================
        # TITULO
        # ==================================

        titulo = QLabel("📊 Dashboard")

        titulo.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            color:#0f172a;
        """)

        self.layout.addWidget(titulo)

        # ==================================
        # BOTON RECARGAR
        # ==================================

        boton_recargar = QPushButton("🔄 Recargar Dashboard")

        boton_recargar.setStyleSheet("""
            QPushButton{
                background:#2563eb;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#1d4ed8;
            }
        """)

        boton_recargar.clicked.connect(self.recargar_dashboard)

        self.layout.addWidget(boton_recargar)

        # ==================================
        # TARJETAS
        # ==================================

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        dinero_hoy, motos_hoy = self.obtener_datos_hoy()
        dinero_mes, motos_mes = self.obtener_datos_mes()

        self.card_hoy = self.crear_card(
            "INGRESOS HOY",
            f"${dinero_hoy:,}",
            f"{motos_hoy} motos"
        )

        self.card_mes = self.crear_card(
            "INGRESOS MES",
            f"${dinero_mes:,}",
            f"{motos_mes} motos"
        )

        cards_layout.addWidget(self.card_hoy)
        cards_layout.addWidget(self.card_mes)

        self.layout.addLayout(cards_layout)

        # ==================================
        # GRAFICAS
        # ==================================

        graficas_layout = QHBoxLayout()
        graficas_layout.setSpacing(20)

        self.canvas_dia = self.crear_grafica_dia()
        self.canvas_mes = self.crear_grafica_mes()

        graficas_layout.addWidget(self.canvas_dia)
        graficas_layout.addWidget(self.canvas_mes)

        self.layout.addLayout(graficas_layout)

        self.setLayout(self.layout)

    # ======================================
    # CREAR CARD
    # ======================================

    def crear_card(self, titulo, dinero, motos):

     card = QFrame()

     card.setMinimumHeight(170)

     card.setStyleSheet("""
        QFrame{
            background:white;
            border-radius:18px;
            border:1px solid #e2e8f0;
        }
     """)

     layout = QVBoxLayout()
     layout.setContentsMargins(25,25,25,25)

     titulo_label = QLabel(titulo)

     titulo_label.setStyleSheet("""
        font-size:14px;
        color:#64748b;
        font-weight:bold;
     """)

     dinero_label = QLabel(dinero)

     dinero_label.setStyleSheet("""
        font-size:34px;
        font-weight:bold;
        color:#0f172a;
     """)

     motos_label = QLabel(motos)

     motos_label.setStyleSheet("""
        font-size:18px;
        color:#475569;
     """)

     layout.addWidget(titulo_label)
     layout.addSpacing(10)
     layout.addWidget(dinero_label)
     layout.addSpacing(10)
     layout.addWidget(motos_label)

     card.setLayout(layout)

    # GUARDAR LABELS
     card.dinero_label = dinero_label
     card.motos_label = motos_label

     return card

    # ======================================
    # DATOS HOY
    # ======================================

    def obtener_datos_hoy(self):

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT 
            COUNT(*),
            IFNULL(SUM(total),0)
        FROM vehiculos
        WHERE DATE(hora_entrada)=DATE('now','localtime')
        AND estado='FINALIZADO'
        """)

        datos = cursor.fetchone()

        conexion.close()

        motos = datos[0]
        dinero = datos[1]

        return dinero, motos

    # ======================================
    # DATOS MES
    # ======================================

    def obtener_datos_mes(self):

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT 
            COUNT(*),
            IFNULL(SUM(total),0)
        FROM vehiculos
        WHERE strftime('%m',hora_entrada)=strftime('%m', 'now', 'localtime')
        AND estado='FINALIZADO'
        """)

        datos = cursor.fetchone()

        conexion.close()

        motos = datos[0]
        dinero = datos[1]

        return dinero, motos

    # ======================================
    # GRAFICA DIA
    # ======================================

    def crear_grafica_dia(self):

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT 
            strftime('%H',hora_entrada),
            COUNT(*)
        FROM vehiculos
        WHERE DATE(hora_entrada)=DATE('now','localtime')
        AND estado='FINALIZADO'
        GROUP BY strftime('%H',hora_entrada)
        """)

        datos = cursor.fetchall()

        conexion.close()

        horas = [d[0] for d in datos]
        cantidades = [d[1] for d in datos]

        figura = Figure(figsize=(5,4))
        figura.patch.set_facecolor("#ffffff")

        canvas = FigureCanvas(figura)

        ax = figura.add_subplot(111)

        ax.plot(
            horas,
            cantidades,
            linewidth=3,
            marker="o"
        )

        ax.set_title(
            "Vehículos por Hora",
            fontsize=14
        )

        ax.grid(True)

        ax.set_facecolor("#ffffff")

        canvas.setStyleSheet("""
            background:white;
            border-radius:18px;
            border:1px solid #e2e8f0;
        """)

        return canvas

    # ======================================
    # GRAFICA MES
    # ======================================

    def crear_grafica_mes(self):

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT 
            DATE(hora_entrada),
            IFNULL(SUM(total),0)
        FROM vehiculos
        WHERE estado='FINALIZADO'
        GROUP BY DATE(hora_entrada)
        """)

        datos = cursor.fetchall()

        conexion.close()

        fechas = [d[0] for d in datos]
        totales = [d[1] for d in datos]

        figura = Figure(figsize=(5,4))
        figura.patch.set_facecolor("#ffffff")

        canvas = FigureCanvas(figura)

        ax = figura.add_subplot(111)

        ax.bar(
            fechas,
            totales
        )

        ax.set_title(
            "Ingresos por Día",
            fontsize=14
        )

        ax.grid(True)

        ax.set_facecolor("#ffffff")

        canvas.setStyleSheet("""
            background:white;
            border-radius:18px;
            border:1px solid #e2e8f0;
        """)

        return canvas

    # ======================================
    # RECARGAR DASHBOARD
    # ======================================

    def recargar_dashboard(self):

     dinero_hoy, motos_hoy = self.obtener_datos_hoy()
     dinero_mes, motos_mes = self.obtener_datos_mes()

    # ACTUALIZAR CARDS

     self.card_hoy.dinero_label.setText(
        f"${dinero_hoy:,}"
     )

     self.card_hoy.motos_label.setText(
        f"{motos_hoy} motos"
     )

     self.card_mes.dinero_label.setText(
        f"${dinero_mes:,}"
     )

     self.card_mes.motos_label.setText(
        f"{motos_mes} motos"
     )