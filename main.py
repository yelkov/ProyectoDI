import clientes
import conexion
import eventos
import styles
from venAux import *
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        conexion.Conexion.db_conexion()
        self.setStyleSheet(styles.load_stylesheet())
        eventos.Eventos.cargarProv()
        eventos.Eventos.cargaMunicli(var.ui.cmbProvcli.currentText())
        clientes.Clientes.cargaTablaClientes()
        eventos.Eventos.resizeTablaClientes()

        '''
        zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        zona de eventos de botones
        '''
        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        '''
        zona de eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDniCli(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmailCli(var.ui.txtEmailcli.text()))
        '''
        zona eventos comboBox
        '''
        var.ui.cmbProvcli.currentIndexChanged.connect(lambda : eventos.Eventos.cargaMunicli(var.ui.cmbProvcli.currentText()))



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())