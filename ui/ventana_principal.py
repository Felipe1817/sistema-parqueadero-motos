from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame
)

from PyQt5.QtCore import Qt

from ui.dashboard import Dashboard
from ui.vehiculos import Parqueadero
from reportes import VentanaReportes
from ui.configuracion import VentanaConfiguracion


class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Parqueadero")
        self.resize(1450, 850)

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }
        """)

        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0,0,0,0)
        layout_principal.setSpacing(0)

        # ==================================================
        # MENU LATERAL
        # ==================================================

        menu_widget = QFrame()

        menu_widget.setFixedWidth(280)

        menu_widget.setStyleSheet("""
            QFrame{
                background:#0f172a;
            }
        """)

        menu = QVBoxLayout()
        menu.setContentsMargins(20,30,20,30)
        menu.setSpacing(15)

        # LOGO / TITULO

        logo = QLabel("🏍️")

        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
            font-size:55px;
            color:white;
        """)

        titulo = QLabel("PARQUEADERO\nMOTOS LA 11")

        titulo.setAlignment(Qt.AlignCenter)

        titulo.setStyleSheet("""
            color:white;
            font-size:24px;
            font-weight:bold;
            margin-bottom:20px;
        """)

        menu.addWidget(logo)
        menu.addWidget(titulo)

        # ==================================================
        # BOTONES
        # ==================================================

        btn_dashboard = QPushButton("📊 Dashboard")
        btn_vehiculos = QPushButton("🏍️ Vehículos")
        btn_reportes = QPushButton("📋 Reportes")
        btn_config = QPushButton("⚙️ Configuración")

        botones = [
            btn_dashboard,
            btn_vehiculos,
            btn_reportes,
            btn_config
        ]

        for boton in botones:

            boton.setCursor(Qt.PointingHandCursor)

            boton.setMinimumHeight(55)

            boton.setStyleSheet("""
                QPushButton{
                    background:#1e293b;
                    color:white;
                    border:none;
                    border-radius:14px;
                    padding-left:20px;
                    text-align:left;
                    font-size:17px;
                    font-weight:bold;
                }

                QPushButton:hover{
                    background:#f59e0b;
                }
            """)

            menu.addWidget(boton)

        menu.addStretch()

        # FOOTER

        footer = QLabel("Sistema de Parqueadero\nVersión 1.0")

        footer.setAlignment(Qt.AlignCenter)

        footer.setStyleSheet("""
            color:#94a3b8;
            font-size:12px;
            margin-top:20px;
        """)

        menu.addWidget(footer)

        menu_widget.setLayout(menu)

        # ==================================================
        # PAGINAS
        # ==================================================

        self.paginas = QStackedWidget()

        self.dashboard = Dashboard()
        self.vehiculos = Parqueadero()
        self.reportes = VentanaReportes()
        self.configuracion = VentanaConfiguracion()

        self.paginas.addWidget(self.dashboard)
        self.paginas.addWidget(self.vehiculos)
        self.paginas.addWidget(self.reportes)
        self.paginas.addWidget(self.configuracion)

        # ==================================================
        # EVENTOS
        # ==================================================

        btn_dashboard.clicked.connect(
            lambda: self.paginas.setCurrentWidget(self.dashboard)
        )

        btn_vehiculos.clicked.connect(
            lambda: self.paginas.setCurrentWidget(self.vehiculos)
        )

        btn_reportes.clicked.connect(
            lambda: self.paginas.setCurrentWidget(self.reportes)
        )

        btn_config.clicked.connect(
            lambda: self.paginas.setCurrentWidget(self.configuracion)
        )

        # ==================================================
        # AGREGAR
        # ==================================================

        layout_principal.addWidget(menu_widget)
        layout_principal.addWidget(self.paginas)

        self.setLayout(layout_principal)