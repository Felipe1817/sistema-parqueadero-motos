import sqlite3

from datetime import datetime

from functools import partial

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QComboBox,
    QFrame,
    QHeaderView
)

from PyQt5.QtCore import Qt

from ui.tickets_directo import generar_ticket_entrada_directo

# =========================================
# NUEVA VENTANA COBRO
# =========================================

from ui.ventana_cobro import VentanaCobro


class Parqueadero(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25,25,25,25)
        layout.setSpacing(20)

        # =========================================
        # TITULO
        # =========================================

        titulo = QLabel("🏍️ Gestión de Vehículos")

        titulo.setStyleSheet("""
            font-size:32px;
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
                border-radius:18px;
                border:1px solid #e2e8f0;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20,20,20,20)

        # =========================================
        # FORMULARIO
        # =========================================

        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)

        # =========================================
        # INPUT PLACA
        # =========================================

        self.input_placa = QLineEdit()

        self.input_placa.setPlaceholderText(
            "Ingrese placa"
        )

        estilo_inputs = """
            QLineEdit{
                padding:12px;
                border-radius:12px;
                border:2px solid #cbd5e1;
                font-size:15px;
                background:white;
            }

            QLineEdit:focus{
                border:2px solid #2563eb;
            }
        """

        self.input_placa.setStyleSheet(estilo_inputs)

        # =========================================
        # BUSCADOR
        # =========================================

        self.buscar_input = QLineEdit()

        self.buscar_input.setPlaceholderText(
            "Buscar placa..."
        )

        self.buscar_input.setStyleSheet(estilo_inputs)

        self.buscar_input.textChanged.connect(
            self.cargar_vehiculos
        )

        # =========================================
        # TIPO VEHICULO
        # =========================================

        self.tipo = QComboBox()

        self.tipo.addItems([
            "Moto",
            "Bicicleta",
            "Moto Eléctrica"
        ])

        self.tipo.setStyleSheet("""
            QComboBox{
                padding:12px;
                border-radius:12px;
                border:2px solid #cbd5e1;
                font-size:15px;
                background:white;
            }
        """)

        # =========================================
        # BOTON ENTRADA
        # =========================================

        self.btn_entrada = QPushButton(
            "Registrar Entrada"
        )

        self.btn_entrada.setCursor(Qt.PointingHandCursor)

        self.btn_entrada.setStyleSheet("""
            QPushButton{
                background:#16a34a;
                color:white;
                padding:12px;
                border:none;
                border-radius:12px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#15803d;
            }
        """)

        # =========================================
        # BOTON SALIDA
        # =========================================

        self.btn_salida = QPushButton(
            "Registrar Salida"
        )

        self.btn_salida.setCursor(Qt.PointingHandCursor)

        self.btn_salida.setStyleSheet("""
            QPushButton{
                background:#dc2626;
                color:white;
                padding:12px;
                border:none;
                border-radius:12px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#b91c1c;
            }
        """)

        form_layout.addWidget(self.input_placa)
        form_layout.addWidget(self.tipo)
        form_layout.addWidget(self.buscar_input)
        form_layout.addWidget(self.btn_entrada)
        form_layout.addWidget(self.btn_salida)

        card_layout.addLayout(form_layout)

        # =========================================
        # TABLA
        # =========================================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(7)

        self.tabla.setHorizontalHeaderLabels([
            "Descripción",
            "Placa",
            "Tipo",
            "Hora Entrada",
            "Estado",
            "Entrada",
            "Cobrar"
        ])

        # =========================================
        # TAMAÑOS COLUMNAS
        # =========================================

        header = self.tabla.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.Fixed
        )

        header.setSectionResizeMode(
            6,
            QHeaderView.Fixed
        )

        self.tabla.setColumnWidth(5, 110)
        self.tabla.setColumnWidth(6, 100)

        self.tabla.setStyleSheet("""
            QTableWidget{
                background:white;
                border:none;
                border-radius:12px;
                font-size:13px;
                gridline-color:#e2e8f0;
            }

            QHeaderView::section{
                background:#0f172a;
                color:white;
                padding:10px;
                border:none;
                font-size:13px;
                font-weight:bold;
            }

            QTableWidget::item{
                padding:8px;
            }

            QTableWidget::item:selected{
                background:#bfdbfe;
                color:black;
            }
        """)

        self.tabla.setAlternatingRowColors(True)

        self.tabla.verticalHeader().setDefaultSectionSize(55)

        self.tabla.itemChanged.connect(
            self.actualizar_descripcion
        )

        card_layout.addWidget(self.tabla)

        card.setLayout(card_layout)

        layout.addWidget(card)

        self.setLayout(layout)

        # =========================================
        # EVENTOS
        # =========================================

        self.btn_entrada.clicked.connect(
            self.registrar_entrada
        )

        self.btn_salida.clicked.connect(
            self.registrar_salida
        )

        self.cargar_vehiculos()

    # =========================================
    # REGISTRAR ENTRADA
    # =========================================

    def registrar_entrada(self):

        placa = self.input_placa.text().upper().strip()

        tipo = self.tipo.currentText()

        if placa == "":

            QMessageBox.warning(
                self,
                "Error",
                "Ingrese una placa"
            )

            return

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT *
        FROM vehiculos
        WHERE placa=?
        AND estado='ACTIVO'
        """, (placa,))

        existe = cursor.fetchone()

        if existe:

            QMessageBox.warning(
                self,
                "Error",
                "Este vehículo ya está activo"
            )

            conexion.close()

            return

        hora_entrada = datetime.now()

        cursor.execute("""
        INSERT INTO vehiculos(
            descripcion,
            placa,
            tipo,
            hora_entrada,
            estado
        )
        VALUES(?,?,?,?,?)
        """, (
            "",
            placa,
            tipo,
            hora_entrada.strftime("%Y-%m-%d %H:%M:%S"),
            "ACTIVO"
        ))

        conexion.commit()
        conexion.close()

        QMessageBox.information(
            self,
            "Correcto",
            "Entrada registrada correctamente"
        )

        self.input_placa.clear()

        self.cargar_vehiculos()

    # =========================================
    # REGISTRAR SALIDA
    # =========================================

    def registrar_salida(self):

        placa = self.input_placa.text().upper().strip()

        self.abrir_cobro_por_placa(placa)

    # =========================================
    # ABRIR COBRO
    # =========================================

    def abrir_cobro_por_placa(self, placa):

        if placa == "":

            QMessageBox.warning(
                self,
                "Error",
                "Ingrese una placa"
            )

            return

        conexion = sqlite3.connect("parqueadero.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id,
               hora_entrada
        FROM vehiculos
        WHERE placa=?
        AND estado='ACTIVO'
        """, (placa,))

        vehiculo = cursor.fetchone()

        if not vehiculo:

            QMessageBox.warning(
                self,
                "Error",
                "Vehículo no encontrado"
            )

            conexion.close()

            return

        id_vehiculo = vehiculo[0]

        hora_entrada = datetime.strptime(
            vehiculo[1],
            "%Y-%m-%d %H:%M:%S"
        )

        hora_salida = datetime.now()

        tiempo = hora_salida - hora_entrada

        minutos = tiempo.total_seconds() / 60

        cursor.execute("""
        SELECT tarifa_hora
        FROM configuracion
        WHERE id=1
        """)

        tarifa_hora = cursor.fetchone()[0]

        conexion.close()

        valor_minuto = tarifa_hora / 60

        total_sugerido = round(
            minutos * valor_minuto
        )

        horas = int(minutos // 60)

        minutos_restantes = int(minutos % 60)

        tiempo_texto = (
            f"{horas} hora(s) "
            f"{minutos_restantes} minuto(s)"
        )

        self.ventana_cobro = VentanaCobro(
            id_vehiculo,
            placa,
            hora_entrada,
            tiempo_texto,
            total_sugerido,
            self.finalizar_salida
        )

        self.ventana_cobro.show()

    # =========================================
    # FINALIZAR SALIDA
    # =========================================

    def finalizar_salida(
        self,
        id_vehiculo,
        placa,
        tiempo_texto,
        total_final
    ):

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        hora_salida = datetime.now()

        cursor.execute("""
        UPDATE vehiculos
        SET hora_salida=?,
            tiempo=?,
            total=?,
            estado='FINALIZADO'
        WHERE id=?
        """, (
            hora_salida.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            tiempo_texto,
            total_final,
            id_vehiculo
        ))

        conexion.commit()

        conexion.close()

        QMessageBox.information(
            self,
            "Salida registrada",
            f"""
Tiempo: {tiempo_texto}

Total pagado: ${total_final:,}
            """
        )

        self.input_placa.clear()

        self.cargar_vehiculos()

    # =========================================
    # IMPRIMIR TICKET ENTRADA
    # =========================================

    def imprimir_ticket_entrada(
        self,
        placa
    ):

        generar_ticket_entrada_directo(placa)

    # =========================================
    # CARGAR VEHICULOS
    # =========================================

    def cargar_vehiculos(self):

        self.tabla.blockSignals(True)

        self.tabla.setRowCount(0)

        conexion = sqlite3.connect("parqueadero.db")

        cursor = conexion.cursor()

        placa_busqueda = self.buscar_input.text()

        query = """
        SELECT descripcion,
               placa,
               tipo,
               hora_entrada,
               estado
        FROM vehiculos
        WHERE estado='ACTIVO'
        """

        parametros = []

        if placa_busqueda != "":

            query += " AND placa LIKE ?"

            parametros.append(
                f"%{placa_busqueda}%"
            )

        query += " ORDER BY id DESC"

        cursor.execute(query, parametros)

        datos = cursor.fetchall()

        conexion.close()

        self.tabla.setRowCount(len(datos))

        for fila_numero, fila_datos in enumerate(datos):

            for columna_numero, dato in enumerate(fila_datos):

                item = QTableWidgetItem(str(dato))

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.tabla.setItem(
                    fila_numero,
                    columna_numero,
                    item
                )

            placa = fila_datos[1]

            # =========================================
            # BOTON ENTRADA
            # =========================================

            btn_ticket = QPushButton("🖨️")

            btn_ticket.setCursor(
                Qt.PointingHandCursor
            )

            btn_ticket.setStyleSheet("""
                QPushButton{
                    background:#2563eb;
                    color:white;
                    border:none;
                    border-radius:8px;
                    font-size:12px;
                    font-weight:bold;
                    padding:6px;
                }

                QPushButton:hover{
                    background:#1d4ed8;
                }
            """)

            btn_ticket.clicked.connect(
                partial(
                    self.imprimir_ticket_entrada,
                    placa
                )
            )

            self.tabla.setCellWidget(
                fila_numero,
                5,
                btn_ticket
            )

            # =========================================
            # BOTON COBRAR
            # =========================================

            btn_cobrar = QPushButton("💰")

            btn_cobrar.setCursor(
                Qt.PointingHandCursor
            )

            btn_cobrar.setStyleSheet("""
                QPushButton{
                    background:#16a34a;
                    color:white;
                    border:none;
                    border-radius:8px;
                    font-size:12px;
                    font-weight:bold;
                    padding:6px;
                }

                QPushButton:hover{
                    background:#15803d;
                }
            """)

            btn_cobrar.clicked.connect(
                partial(
                    self.abrir_cobro_por_placa,
                    placa
                )
            )

            self.tabla.setCellWidget(
                fila_numero,
                6,
                btn_cobrar
            )

        self.tabla.blockSignals(False)

    # =========================================
    # ACTUALIZAR DESCRIPCION
    # =========================================

    def actualizar_descripcion(self, item):

        columna = item.column()

        if columna != 0:
            return

        descripcion = item.text()

        placa_item = self.tabla.item(
            item.row(),
            1
        )

        placa = placa_item.text()

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE vehiculos
        SET descripcion=?
        WHERE placa=?
        AND estado='ACTIVO'
        """, (
            descripcion,
            placa
        ))

        conexion.commit()

        conexion.close()