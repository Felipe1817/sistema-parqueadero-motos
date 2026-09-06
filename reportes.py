import sqlite3
import pandas as pd

from functools import partial

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QDateEdit,
    QFrame,
    QMessageBox,
    QHeaderView
)

from PyQt5.QtCore import QDate, Qt

from ui.tickets_directo import (
    generar_ticket_entrada_directo,
    generar_ticket_salida_directo
)


class VentanaReportes(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }

            QLineEdit,QDateEdit{
                padding:10px;
                border-radius:10px;
                border:1px solid #cbd5e1;
                background:white;
                font-size:14px;
            }

            QPushButton{
                background:#2563eb;
                color:white;
                border:none;
                padding:12px;
                border-radius:10px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#1d4ed8;
            }

            QTableWidget{
                background:white;
                border-radius:15px;
                border:1px solid #cbd5e1;
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
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25,25,25,25)
        layout.setSpacing(20)

        titulo = QLabel("📋 Reportes")

        titulo.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            color:#0f172a;
        """)

        layout.addWidget(titulo)

        filtros = QHBoxLayout()

        self.fecha_inicio = QDateEdit()
        self.fecha_fin = QDateEdit()

        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_fin.setCalendarPopup(True)

        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_fin.setDate(QDate.currentDate())

        self.buscar_input = QLineEdit()

        self.buscar_input.setPlaceholderText(
            "Buscar placa..."
        )

        btn_buscar = QPushButton("Buscar")
        btn_excel = QPushButton("Exportar Excel")

        filtros.addWidget(self.fecha_inicio)
        filtros.addWidget(self.fecha_fin)
        filtros.addWidget(self.buscar_input)
        filtros.addWidget(btn_buscar)
        filtros.addWidget(btn_excel)

        layout.addLayout(filtros)

        # =========================================
        # CARDS
        # =========================================

        cards = QHBoxLayout()

        self.card_vehiculos = QFrame()
        self.card_ingresos = QFrame()

        self.card_vehiculos.setStyleSheet("""
            background:white;
            border-radius:18px;
        """)

        self.card_ingresos.setStyleSheet("""
            background:white;
            border-radius:18px;
        """)

        layout_card1 = QVBoxLayout()
        layout_card2 = QVBoxLayout()

        texto1 = QLabel("Vehículos Finalizados")
        texto2 = QLabel("Ingresos")

        self.lbl_cantidad = QLabel("0")
        self.lbl_ingresos = QLabel("$0")

        self.lbl_cantidad.setStyleSheet("""
            font-size:36px;
            font-weight:bold;
            color:#0f172a;
        """)

        self.lbl_ingresos.setStyleSheet("""
            font-size:36px;
            font-weight:bold;
            color:#16a34a;
        """)

        layout_card1.addWidget(texto1)
        layout_card1.addWidget(self.lbl_cantidad)

        layout_card2.addWidget(texto2)
        layout_card2.addWidget(self.lbl_ingresos)

        self.card_vehiculos.setLayout(layout_card1)
        self.card_ingresos.setLayout(layout_card2)

        cards.addWidget(self.card_vehiculos)
        cards.addWidget(self.card_ingresos)

        layout.addLayout(cards)

        # =========================================
        # TABLA
        # =========================================

        self.tabla = QTableWidget()

        # AHORA 10 COLUMNAS
        self.tabla.setColumnCount(10)

        self.tabla.setHorizontalHeaderLabels([
            "DESCRIPCIÓN",
            "PLACA",
            "TIPO",
            "ENTRADA",
            "SALIDA",
            "TIEMPO",
            "TOTAL",
            "ESTADO",
            "TICKET ENTRADA",
            "TICKET SALIDA"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )

        self.tabla.setWordWrap(False)

        self.tabla.setColumnWidth(0, 300)
        self.tabla.setColumnWidth(1, 120)
        self.tabla.setColumnWidth(2, 140)
        self.tabla.setColumnWidth(3, 180)
        self.tabla.setColumnWidth(4, 180)
        self.tabla.setColumnWidth(5, 150)
        self.tabla.setColumnWidth(6, 120)
        self.tabla.setColumnWidth(7, 120)
        self.tabla.setColumnWidth(8, 160)
        self.tabla.setColumnWidth(9, 160)

        self.tabla.verticalHeader().setDefaultSectionSize(50)

        self.tabla.setAlternatingRowColors(True)

        layout.addWidget(self.tabla)

        # =========================================
        # TOTAL GENERAL
        # =========================================

        self.lbl_total = QLabel("💰 Total: $0")

        self.lbl_total.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#16a34a;
        """)

        layout.addWidget(self.lbl_total)

        self.setLayout(layout)

        btn_buscar.clicked.connect(self.buscar)
        btn_excel.clicked.connect(self.exportar_excel)

        self.tabla.itemChanged.connect(
            self.guardar_descripcion
        )

        self.buscar()

    # =========================================
    # BUSCAR
    # =========================================

    def buscar(self):

        self.tabla.blockSignals(True)

        inicio = self.fecha_inicio.date().toString(
            "yyyy-MM-dd"
        )

        fin = self.fecha_fin.date().toString(
            "yyyy-MM-dd"
        )

        placa = self.buscar_input.text()

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        query = """
        SELECT 
            id,
            descripcion,
            placa,
            tipo,
            hora_entrada,
            hora_salida,
            tiempo,
            total,
            estado
        FROM vehiculos
        WHERE estado='FINALIZADO'
        AND DATE(hora_entrada)
        BETWEEN ? AND ?
        """

        parametros = [inicio, fin]

        if placa != "":

            query += " AND placa LIKE ?"

            parametros.append(f"%{placa}%")

        query += " ORDER BY id DESC"

        df = pd.read_sql_query(
            query,
            conexion,
            params=parametros
        )

        self.df_actual = df

        self.tabla.setRowCount(len(df))

        total_general = 0

        for fila in range(len(df)):

            id_vehiculo = int(df.iloc[fila]["id"])

            descripcion = str(
                df.iloc[fila]["descripcion"]
            )

            item_descripcion = QTableWidgetItem(
                descripcion
            )

            item_descripcion.setData(
                Qt.UserRole,
                id_vehiculo
            )

            self.tabla.setItem(
                fila,
                0,
                item_descripcion
            )

            datos_fila = [
                df.iloc[fila]["placa"],
                df.iloc[fila]["tipo"],
                df.iloc[fila]["hora_entrada"],
                df.iloc[fila]["hora_salida"],
                df.iloc[fila]["tiempo"],
                f"${df.iloc[fila]['total']:,}",
                df.iloc[fila]["estado"]
            ]

            for coluna_tabla, valor in enumerate(datos_fila, start=1):

                item = QTableWidgetItem(str(valor))

                item.setTextAlignment(Qt.AlignCenter)

                self.tabla.setItem(
                    fila,
                    coluna_tabla,
                    item
                )

            self.tabla.setRowHeight(
                fila,
                50
            )

            # =========================================
            # BOTON TICKET ENTRADA
            # =========================================

            placa_ticket = df.iloc[fila]["placa"]

            btn_entrada = QPushButton("🖨️ Entrada")

            btn_entrada.setStyleSheet("""
                QPushButton{
                    background:#2563eb;
                    color:white;
                    border:none;
                    border-radius:8px;
                    padding:8px;
                    font-size:12px;
                    font-weight:bold;
                }

                QPushButton:hover{
                    background:#1d4ed8;
                }
            """)

            btn_entrada.clicked.connect(
                partial(
                    self.generar_ticket_entrada_pdf,
                    placa_ticket
                )
            )

            self.tabla.setCellWidget(
                fila,
                8,
                btn_entrada
            )

            # =========================================
            # BOTON TICKET SALIDA
            # =========================================

            btn_salida = QPushButton("🖨️ Salida")

            btn_salida.setStyleSheet("""
                QPushButton{
                    background:#16a34a;
                    color:white;
                    border:none;
                    border-radius:8px;
                    padding:8px;
                    font-size:12px;
                    font-weight:bold;
                }

                QPushButton:hover{
                    background:#15803d;
                }
            """)

            btn_salida.clicked.connect(
                partial(
                    self.generar_ticket_salida_pdf,
                    id_vehiculo
                )
            )

            self.tabla.setCellWidget(
                fila,
                9,
                btn_salida
            )

            try:

                total_general += int(
                    df.iloc[fila]["total"]
                )

            except:
                pass

        self.lbl_total.setText(
            f"💰 Total General: ${total_general:,}"
        )

        self.lbl_cantidad.setText(
            str(len(df))
        )

        self.lbl_ingresos.setText(
            f"${total_general:,}"
        )

        conexion.close()

        self.tabla.blockSignals(False)

    # =========================================
    # GUARDAR DESCRIPCION
    # =========================================

    def guardar_descripcion(self, item):

        if item.column() != 0:
            return

        descripcion = item.text()

        id_vehiculo = item.data(Qt.UserRole)

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE vehiculos
        SET descripcion=?
        WHERE id=?
        """, (
            descripcion,
            id_vehiculo
        ))

        conexion.commit()

        conexion.close()

    # =========================================
    # GENERAR TICKET ENTRADA
    # =========================================

    def generar_ticket_entrada_pdf(
        self,
        placa
    ):

        generar_ticket_entrada_directo(placa)

    # =========================================
    # GENERAR TICKET SALIDA
    # =========================================

    def generar_ticket_salida_pdf(
        self,
        id_vehiculo,
        checked=False
    ):

        conexion = sqlite3.connect(
            "parqueadero.db"
        )

        cursor = conexion.cursor()

        cursor.execute("""
        SELECT placa,
               tiempo,
               total
        FROM vehiculos
        WHERE id=?
        """, (int(id_vehiculo),))

        datos = cursor.fetchone()

        conexion.close()

        if datos:

            placa = datos[0]
            tiempo = datos[1]
            total = datos[2]

            generar_ticket_salida_directo(
             placa,
             tiempo,
             total
            )

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Vehículo no encontrado"
            )

    # =========================================
    # EXPORTAR EXCEL
    # =========================================

    def exportar_excel(self):

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            "reporte_parqueadero.xlsx",
            "Excel (*.xlsx)"
        )

        if archivo:

            self.df_actual.to_excel(
                archivo,
                index=False
            )

            QMessageBox.information(
                self,
                "Excel",
                "Reporte exportado correctamente"
            )