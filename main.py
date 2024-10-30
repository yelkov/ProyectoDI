import clientes
import conexion
import conexionserver
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

        #conexionserver.ConexionServer.crear_conexion()
        conexion.Conexion.db_conexion()

        var.uicalendar = Calendar()
        var.dlgAbrir = FileDialogAbrir()
        var.dlggestion = dlg_Tipo_prop()


        self.setStyleSheet(styles.load_stylesheet())
        eventos.Eventos.cargarProv()
        eventos.Eventos.cargaMunicli(var.ui.cmbProvcli.currentText())
        eventos.Eventos.cargaMuniprop(var.ui.cmbProvprop.currentText())
        eventos.Eventos.cargarTipoprop()

        '''
        zona de eventos de tablas
        '''
        var.ui.tablaClientes.setAlternatingRowColors(True)
        clientes.Clientes.cargaTablaClientes()
        eventos.Eventos.resizeTablaClientes()
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)

        '''
        zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_propiedades.triggered.connect(eventos.Eventos.abrirTipoprop)

        '''
        zona de eventos de botones
        '''
        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnAltaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1,0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))
        var.ui.btnBajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1,1))
        var.ui.btnModifcli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)


        '''
        zona de eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDniCli(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmailCli(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda : clientes.Clientes.checkMovilCli(var.ui.txtMovilcli.text()))
        '''
        zona eventos comboBox
        '''
        var.ui.cmbProvcli.currentIndexChanged.connect(lambda : eventos.Eventos.cargaMunicli(var.ui.cmbProvcli.currentText()))
        var.ui.cmbProvprop.currentIndexChanged.connect(lambda : eventos.Eventos.cargaMuniprop(var.ui.cmbProvprop.currentText()))

        '''
        zona eventos toolBar
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionbarAltaTipoprop.triggered.connect(eventos.Eventos.abrirTipoprop)
        '''
        zona eventos checkbox
        '''
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())