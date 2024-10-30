import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtGui

from eventos import Eventos


class Propiedades():

    @staticmethod
    def altaTipoPropiedad(venDialogo):
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad añadida.")
                mbox.exec()
                eventos.Eventos.cargarTipopropGestion(venDialogo)
            else:
                mbox = eventos.Eventos.crearMensajeError("Aviso", "Error al añadir tipo de propiedad añadida.")
                mbox.exec()
            var.dlggestion.ui.txtTipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)

    @staticmethod
    def bajaTipoPropiedad(venDialogo):
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            if conexion.Conexion.bajaTipoprop(tipo):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad eliminada.")
                mbox.exec()
                eventos.Eventos.cargarTipoprop()
                var.dlggestion.ui.txtTipoprop.setText("")
                eventos.Eventos.cargarTipopropGestion(venDialogo)
            else:
                mbox = eventos.Eventos.crearMensajeError("Aviso","Error al eliminar tipo de propiedad.")
                mbox.exec()
        except Exception as e:
            print("Error baja tipo propiedad" + e)


    @staticmethod
    def altaPropiedad():
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),var.ui.txtPrecioAlquilerprop.text(),
                         var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCpprop.text(),var.ui.areatxtDescriprop.toPlainText()]
            tipoOper = []
            if var.ui.chkAlquilprop.isChecked():
                tipoOper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipoOper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipoOper.append(var.ui.chkInterprop.text())
            propiedad.append(tipoOper)
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                propiedad.append(var.ui.rbtVentaprop.text())

            propiedad.append(var.ui.txtNomeprop.text())
            propiedad.append(var.ui.txtMovilprop.text())

            if conexion.Conexion.altaPropiedad(propiedad):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha grabado la propiedad en la base de datos.")
                mbox.exec()
            else:
                mbox = eventos.Eventos.crearMensajeError("Aviso","Se ha producido un error al grabar la propiedad.")
                mbox.exec()
        except Exception as e:
            print(str(e))

    @staticmethod
    def checkMovilProp(movil):
        try:
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilprop.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilprop.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilprop.setText(None)
                var.ui.txtMovilprop.setPlaceholderText("móvil no válido")
                var.ui.txtMovilprop.setFocus()
        except Exception as e:
            print("error check movil", e)