import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
    QLineEdit,
    QSpinBox,
    QGridLayout
)

from PyQt5.QtCore import Qt


class VentanaConfiguracion(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(40,40,40,40)

        # =========================================
        # TITULO
        # =========================================

        titulo = QLabel("⚙️ Configuración")

        titulo.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#0f172a;
        """)

        layout.addWidget(titulo)

        # =========================================
        # CARD
        # =========================================

        card = QFrame()

        card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:22px;
                border:1px solid #e2e8f0;
            }
        """)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(35,35,35,35)

        card_layout.setSpacing(20)

        # =========================================
        # GRID
        # =========================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(15)

        # =========================================
        # INPUTS
        # =========================================

        self.nombre = QLineEdit()

        self.nombre.setPlaceholderText(
            "Nombre parqueadero"
        )

        self.nit = QLineEdit()

        self.nit.setPlaceholderText(
            "NIT"
        )

        self.direccion = QLineEdit()

        self.direccion.setPlaceholderText(
            "Dirección"
        )

        self.telefono = QLineEdit()

        self.telefono.setPlaceholderText(
            "Teléfono"
        )

        self.mensaje = QLineEdit()

        self.mensaje.setPlaceholderText(
            "Mensaje ticket"
        )

        self.tarifa = QSpinBox()

        self.tarifa.setMaximum(1000000)

        self.tarifa.setSuffix(" COP")

        inputs = [
            self.nombre,
            self.nit,
            self.direccion,
            self.telefono,
            self.mensaje
        ]

        for i in inputs:

            i.setMinimumHeight(55)

            i.setStyleSheet("""
                QLineEdit{
                    border:2px solid #cbd5e1;
                    border-radius:14px;
                    padding:12px;
                    font-size:15px;
                    background:white;
                    color:#0f172a;
                }

                QLineEdit:focus{
                    border:2px solid #2563eb;
                }
            """)

        self.tarifa.setStyleSheet("""
            QSpinBox{
                border:2px solid #cbd5e1;
                border-radius:14px;
                padding:10px;
                font-size:16px;
                background:white;
                color:#0f172a;
            }

            QSpinBox:focus{
                border:2px solid #2563eb;
            }
        """)

        self.tarifa.setMinimumHeight(55)

        # =========================================
        # LABELS
        # =========================================

        estilo_label = """
            font-size:14px;
            font-weight:bold;
            color:#334155;
        """

        lbl_nombre = QLabel("Nombre")
        lbl_nombre.setStyleSheet(estilo_label)

        lbl_nit = QLabel("NIT")
        lbl_nit.setStyleSheet(estilo_label)

        lbl_direccion = QLabel("Dirección")
        lbl_direccion.setStyleSheet(estilo_label)

        lbl_telefono = QLabel("Teléfono")
        lbl_telefono.setStyleSheet(estilo_label)

        lbl_mensaje = QLabel("Mensaje Ticket")
        lbl_mensaje.setStyleSheet(estilo_label)

        lbl_tarifa = QLabel("Tarifa Hora")
        lbl_tarifa.setStyleSheet(estilo_label)

        # =========================================
        # AGREGAR GRID
        # =========================================

        grid.addWidget(lbl_nombre, 0, 0)
        grid.addWidget(self.nombre, 1, 0)

        grid.addWidget(lbl_nit, 0, 1)
        grid.addWidget(self.nit, 1, 1)

        grid.addWidget(lbl_direccion, 2, 0, 1, 2)
        grid.addWidget(self.direccion, 3, 0, 1, 2)

        grid.addWidget(lbl_telefono, 4, 0)
        grid.addWidget(self.telefono, 5, 0)

        grid.addWidget(lbl_tarifa, 4, 1)
        grid.addWidget(self.tarifa, 5, 1)

        grid.addWidget(lbl_mensaje, 6, 0, 1, 2)
        grid.addWidget(self.mensaje, 7, 0, 1, 2)

        card_layout.addLayout(grid)

        # =========================================
        # BOTON
        # =========================================

        boton = QPushButton("Guardar Configuración")

        boton.setCursor(Qt.PointingHandCursor)

        boton.setMinimumHeight(58)

        boton.setStyleSheet("""
            QPushButton{
                background:#f59e0b;
                color:white;
                border:none;
                border-radius:16px;
                font-size:17px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#d97706;
            }
        """)

        boton.clicked.connect(
            self.guardar_configuracion
        )

        card_layout.addWidget(boton)

        card.setLayout(card_layout)

        layout.addWidget(card)

        self.setLayout(layout)

        self.cargar_configuracion()

    # =========================================
    # CARGAR
    # =========================================

    def cargar_configuracion(self):

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        cursor.execute("""
        SELECT nombre,
               nit,
               direccion,
               telefono,
               mensaje_ticket,
               tarifa_hora
        FROM configuracion
        WHERE id=1
        """)

        datos = cursor.fetchone()

        conexion.close()

        if datos:

            self.nombre.setText(datos[0])
            self.nit.setText(datos[1])
            self.direccion.setText(datos[2])
            self.telefono.setText(datos[3])
            self.mensaje.setText(datos[4])
            self.tarifa.setValue(datos[5])

    # =========================================
    # GUARDAR
    # =========================================

    def guardar_configuracion(self):

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE configuracion
        SET nombre=?,
            nit=?,
            direccion=?,
            telefono=?,
            mensaje_ticket=?,
            tarifa_hora=?
        WHERE id=1
        """, (

            self.nombre.text(),

            self.nit.text(),

            self.direccion.text(),

            self.telefono.text(),

            self.mensaje.text(),

            self.tarifa.value()
        ))

        conexion.commit()

        conexion.close()

        QMessageBox.information(
            self,
            "Correcto",
            "Configuración guardada correctamente"
        )