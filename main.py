import conexion
import eventos
import styles
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        conexion.Conexion.db_conexion(self)
        self.setStyleSheet(styles.load_stylesheet())
        eventos.Eventos.cargarProv(self)

        '''
        zona de eventos del menubar
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())