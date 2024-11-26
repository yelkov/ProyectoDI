from xml.dom.minidom import Notation

from PyQt6.QtCore import QLocale, QRegularExpression, QDate, Qt
from PyQt6.QtGui import QIcon, QDoubleValidator, QIntValidator, QRegularExpressionValidator

import clientes
import conexion
import conexionserver
import eventos
import propiedades
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

        conexionserver.ConexionServer.crear_conexion()
        #conexion.Conexion.db_conexion()

        var.uicalendar = Calendar()
        var.dlgAbrir = FileDialogAbrir()
        #var.dlggestion = dlg_Tipo_prop()
        var.dlgabout = Dlg_About()


        self.setStyleSheet(styles.load_stylesheet())
        eventos.Eventos.cargarProv()
        eventos.Eventos.cargaMunicli()
        eventos.Eventos.cargaMuniprop()
        propiedades.Propiedades.cargarTipoprop()
        var.ui.rbtAlquilprop.setEnabled(False)
        var.ui.rbtVentaprop.setEnabled(False)

        '''
        validadores
        '''
        validadorNumerosReales = QRegularExpressionValidator(QRegularExpression(r"^(?:[1-9]\d{0,9}|0)(?:\.\d{2})?$"))
        var.ui.txtSuperprop.setValidator(validadorNumerosReales)
        var.ui.txtPrecioVentaprop.setValidator(validadorNumerosReales)
        var.ui.txtPrecioAlquilerprop.setValidator(validadorNumerosReales)
        validadorCP = QIntValidator(10000,99999,self)
        var.ui.txtCpprop.setValidator(validadorCP)
        validadorMovil = QIntValidator(0,999999999,self)
        var.ui.txtMovilcli.setValidator(validadorMovil)
        var.ui.txtMovilprop.setValidator(validadorMovil)
        validadorFechas = QRegularExpressionValidator(QRegularExpression(r"^(0?[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"))
        var.ui.txtAltaprop.setValidator(validadorFechas)
        var.ui.txtBajaprop.setValidator(validadorFechas)
        var.ui.txtAltacli.setValidator(validadorFechas)
        var.ui.txtBajacli.setValidator(validadorFechas)

        '''
        zona de eventos de tablas
        '''
        var.ui.tablaClientes.setAlternatingRowColors(True)
        var.ui.tablaProp.setAlternatingRowColors(True)

        clientes.Clientes.cargaTablaClientes()
        eventos.Eventos.resizeTablaClientes()
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)

        propiedades.Propiedades.cargarTablaPropiedades()
        eventos.Eventos.resizeTablaPropiedades()
        var.ui.tablaProp.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        '''
        zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_propiedades.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVprop)
        var.ui.actionExportar_Propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONprop)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrir_about)
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
        var.ui.btnBuscarDni.clicked.connect(clientes.Clientes.buscaOneCliente)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifprop.clicked.connect(propiedades.Propiedades.modifProp)
        var.ui.btnDelprop.clicked.connect(propiedades.Propiedades.bajaProp)
        var.ui.btnBuscaTipoProp.clicked.connect(propiedades.Propiedades.cargarTablaPropiedades)


        '''
        zona de eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDniCli(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmailCli(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda : clientes.Clientes.checkMovilCli(var.ui.txtMovilcli.text()))
        var.ui.txtMovilprop.editingFinished.connect(lambda : propiedades.Propiedades.checkMovilProp(var.ui.txtMovilprop.text()))
        var.ui.txtBajaprop.textChanged.connect(propiedades.Propiedades.cambiarAvailableRbt)
        var.ui.txtPrecioVentaprop.textChanged.connect(propiedades.Propiedades.activarCheckPrecios)
        var.ui.txtPrecioAlquilerprop.textChanged.connect(propiedades.Propiedades.activarCheckPrecios)
        '''
        zona eventos comboBox
        '''
        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargaMunicli)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargaMuniprop)

        var.ui.cmbMuniprop.setEditable(True)
        var.ui.cmbProvprop.setEditable(True)
        var.ui.cmbMunicli.setEditable(True)
        var.ui.cmbProvcli.setEditable(True)

        completer = QtWidgets.QCompleter(var.provincias, var.ui.cmbProvprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbProvprop.setCompleter(completer)

        completer = QtWidgets.QCompleter(var.provincias, var.ui.cmbProvcli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbProvcli.setCompleter(completer)

        var.ui.cmbProvprop.lineEdit().editingFinished.connect(eventos.Eventos.checkProvinciaProp)
        var.ui.cmbMuniprop.lineEdit().editingFinished.connect(eventos.Eventos.checkMunicipioProp)
        var.ui.cmbProvcli.lineEdit().editingFinished.connect(eventos.Eventos.checkProvinciaCli)
        var.ui.cmbMunicli.lineEdit().editingFinished.connect(eventos.Eventos.checkMunicipioCli)



        var.ui.cmbTipoprop.currentIndexChanged.connect(propiedades.Propiedades.cargarTablaPropiedades)
        var.ui.cmbMuniprop.currentIndexChanged.connect(propiedades.Propiedades.cargarTablaPropiedades)

        '''
        zona eventos toolBar
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionbarAltaTipoprop.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionFiltrar.triggered.connect(propiedades.Propiedades.filtrar)

        '''
        zona eventos checkbox
        '''
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriaprop.stateChanged.connect(propiedades.Propiedades.historicoProp)






if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())