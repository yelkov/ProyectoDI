import eventos
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)

        '''
        zona de eventos del menubar
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())