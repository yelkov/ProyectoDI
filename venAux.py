from datetime import datetime

from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore

import conexion
import dlgGestion
import eventos
import informes
import var
import propiedades
from dlgAbout import Ui_Dialog
from dlgCalendar import *
from dlgGestion import Ui_dlg_tipoprop
from dlgInformeProp import Ui_dlgInformeProp


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        """
        Constructor de la clase Calendar. Usado para abrir un popup con un calendario.
        """
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
        """
        Constructor de la clase FileDialog. Genera una ventana de selección de ficheros en el equipo.
        """
        super(FileDialogAbrir,self).__init__()

class dlg_Tipo_prop(QtWidgets.QDialog):
    def __init__(self):
        """
        Constructor de la clase dlg_Tipo_prop. Genera una ventana emergente para gestionar los tipos de propiedades usadas en la aplicación.
        """
        super(dlg_Tipo_prop,self).__init__()
        self.ui = Ui_dlg_tipoprop()
        self.ui.setupUi(self)
        self.ui.btnAltaTipoprop.clicked.connect(lambda: propiedades.Propiedades.altaTipoPropiedad(self))
        self.ui.btnDelTipoprop.clicked.connect(lambda: propiedades.Propiedades.bajaTipoPropiedad(self))
        propiedades.Propiedades.cargarTipopropGestion(self)
        self.ui.cmbTipopropGestion.activated.connect(lambda: propiedades.Propiedades.seleccionarTipoGestion(self))

class Dlg_About(QtWidgets.QDialog):
    def __init__(self):
        """
        Constructor de la clase Dlg_About. Abre una ventana con datos sobre la aplicación.
        """
        super(Dlg_About,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnAceptar.clicked.connect(self.close)

class Dlg_InformeProp(QtWidgets.QDialog):
    def __init__(self):
        """
        Constructor de la clase Dlg_InformeProp. Abre una ventana que permite seleccionar al usuario un municipio para crear un informe sobre las propiedades presentes en ese municipio.
        """
        super(Dlg_InformeProp,self).__init__()
        self.ui = Ui_dlgInformeProp()
        self.ui.setupUi(self)
        propiedades.Propiedades.cargaMuniInformeProp(self)
        self.ui.btnInformeProp.clicked.connect(lambda: informes.Informes.reportPropiedades(self.ui.cmbInformeMuniProp.currentText()))
