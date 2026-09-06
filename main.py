import sys

from PyQt5.QtWidgets import QApplication

from ui.ventana_principal import VentanaPrincipal


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec_())