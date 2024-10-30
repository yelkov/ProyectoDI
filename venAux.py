from datetime import datetime

from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore

import conexion
import eventos
import var
import propiedades
from dlgCalendar import *
from dlgGestion import Ui_dlg_tipoprop


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate(QtCore.QDate(ano,mes,dia))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir,self).__init__()

class dlg_Tipo_prop(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_Tipo_prop,self).__init__()
        self.ui = Ui_dlg_tipoprop()
        self.ui.setupUi(self)
        self.ui.btnAltaTipoprop.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.ui.btnDelTipoprop.clicked.connect(propiedades.Propiedades.bajaTipoPropiedad)
        eventos.Eventos.cargarTipopropGestion()
        #self.ui.cmbTipopropGestion.currentIndexChanged.connect()
