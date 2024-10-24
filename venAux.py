from datetime import datetime

from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore

import eventos
import var
from dlgCalendar import *
from dlgTipoprop import Ui_dlg_tipoprop


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

class dlg_Tipo_prop(QtWidgets.QFileDialog):
    def __init__(self):
        super(dlg_Tipo_prop,self).__init__()
        var.ui.dlggestion = Ui_dlg_tipoprop()
        var.dlggestion.setupUi(self)