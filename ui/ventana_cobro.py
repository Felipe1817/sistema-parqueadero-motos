from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QFrame
)

from PyQt5.QtCore import Qt


class VentanaCobro(QWidget):

    def __init__(
        self,
        id_vehiculo,
        placa,
        hora_entrada,
        tiempo_texto,
        total_sugerido,
        funcion_finalizar
    ):

        super().__init__()

        # =====================================
        # VARIABLES
        # =====================================

        self.id_vehiculo = id_vehiculo
        self.placa = placa
        self.tiempo_texto = tiempo_texto
        self.total_sugerido = total_sugerido
        self.funcion_finalizar = funcion_finalizar

        # =====================================
        # CONFIG VENTANA
        # =====================================

        self.setWindowTitle(
            "💰 Cobro de Parqueadero"
        )

        self.resize(650, 420)

        self.setStyleSheet("""
            QWidget{
                background:#f1f5f9;
                font-family:Segoe UI;
            }

            QFrame{
                background:white;
                border-radius:20px;
                border:1px solid #e2e8f0;
            }

            QLabel{
                color:#0f172a;
            }

            QLineEdit{
                padding:14px;
                border-radius:12px;
                border:2px solid #cbd5e1;
                background:white;
                font-size:18px;
            }

            QLineEdit:focus{
                border:2px solid #2563eb;
            }

            QPushButton{
                padding:14px;
                border:none;
                border-radius:12px;
                font-size:15px;
                font-weight:bold;
            }
        """)

        # =====================================
        # LAYOUT PRINCIPAL
        # =====================================

        layout_principal = QVBoxLayout()

        layout_principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        # =====================================
        # CARD
        # =====================================

        card = QFrame()

        card_layout = QVBoxLayout()

        card_layout.setSpacing(18)

        # =====================================
        # TITULO
        # =====================================

        titulo = QLabel(
            "💰 Registrar Cobro"
        )

        titulo.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#0f172a;
        """)

        titulo.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(titulo)

        # =====================================
        # PLACA
        # =====================================

        lbl_placa = QLabel(
            f"🏍️ Vehículo: {placa}"
        )

        lbl_placa.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#2563eb;
        """)

        lbl_placa.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(lbl_placa)

        # =====================================
        # TIEMPO
        # =====================================

        lbl_tiempo = QLabel(
            f"⏱️ Tiempo: {tiempo_texto}"
        )

        lbl_tiempo.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        lbl_tiempo.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(lbl_tiempo)

        # =====================================
        # COSTO SUGERIDO
        # =====================================

        lbl_sugerido = QLabel(
            f"💵 Costo sugerido: ${total_sugerido:,}"
        )

        lbl_sugerido.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#16a34a;
        """)

        lbl_sugerido.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(lbl_sugerido)

        # =====================================
        # INPUTS
        # =====================================

        fila_inputs = QHBoxLayout()

        # =====================================
        # COSTO FINAL
        # =====================================

        columna1 = QVBoxLayout()

        lbl_total = QLabel(
            "Costo final"
        )

        lbl_total.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.input_total = QLineEdit()

        self.input_total.setText(
            str(total_sugerido)
        )

        columna1.addWidget(lbl_total)
        columna1.addWidget(self.input_total)

        # =====================================
        # PAGO CLIENTE
        # =====================================

        columna2 = QVBoxLayout()

        lbl_pago = QLabel(
            "Pago cliente"
        )

        lbl_pago.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.input_pago = QLineEdit()

        self.input_pago.textChanged.connect(
            self.calcular_cambio
        )

        columna2.addWidget(lbl_pago)
        columna2.addWidget(self.input_pago)

        fila_inputs.addLayout(columna1)
        fila_inputs.addLayout(columna2)

        card_layout.addLayout(fila_inputs)

        # =====================================
        # CAMBIO
        # =====================================

        self.lbl_cambio = QLabel(
            "🪙 Cambio: $0"
        )

        self.lbl_cambio.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#dc2626;
        """)

        self.lbl_cambio.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.lbl_cambio)

        # =====================================
        # BOTONES
        # =====================================

        botones = QHBoxLayout()

        # =====================================
        # BOTON COBRAR
        # =====================================

        btn_cobrar = QPushButton(
            "✅ Cobrar"
        )

        btn_cobrar.setCursor(
            Qt.PointingHandCursor
        )

        btn_cobrar.setStyleSheet("""
            QPushButton{
                background:#16a34a;
                color:white;
            }

            QPushButton:hover{
                background:#15803d;
            }
        """)

        # =====================================
        # BOTON CANCELAR
        # =====================================

        btn_cancelar = QPushButton(
            "❌ Cancelar"
        )

        btn_cancelar.setCursor(
            Qt.PointingHandCursor
        )

        btn_cancelar.setStyleSheet("""
            QPushButton{
                background:#dc2626;
                color:white;
            }

            QPushButton:hover{
                background:#b91c1c;
            }
        """)

        botones.addWidget(btn_cobrar)
        botones.addWidget(btn_cancelar)

        card_layout.addLayout(botones)

        card.setLayout(card_layout)

        layout_principal.addWidget(card)

        self.setLayout(layout_principal)

        # =====================================
        # EVENTOS
        # =====================================

        btn_cobrar.clicked.connect(
            self.cobrar
        )

        btn_cancelar.clicked.connect(
            self.close
        )

    # =====================================
    # CALCULAR CAMBIO
    # =====================================

    def calcular_cambio(self):

        try:

            total = int(
                self.input_total.text()
            )

            pago = int(
                self.input_pago.text()
            )

            cambio = pago - total

            self.lbl_cambio.setText(
                f"🪙 Cambio: ${cambio:,}"
            )

            # COLOR VERDE SI HAY CAMBIO

            if cambio >= 0:

                self.lbl_cambio.setStyleSheet("""
                    font-size:28px;
                    font-weight:bold;
                    color:#16a34a;
                """)

            else:

                self.lbl_cambio.setStyleSheet("""
                    font-size:28px;
                    font-weight:bold;
                    color:#dc2626;
                """)

        except:

            self.lbl_cambio.setText(
                "🪙 Cambio: $0"
            )

    # =====================================
    # COBRAR
    # =====================================

    def cobrar(self):

        try:

            total_final = int(
                self.input_total.text()
            )

        except:

            QMessageBox.warning(
                self,
                "Error",
                "Ingrese un valor válido"
            )

            return

        self.funcion_finalizar(
            self.id_vehiculo,
            self.placa,
            self.tiempo_texto,
            total_final
        )

        self.close()