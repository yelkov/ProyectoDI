import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtGui


class Propiedades():

    @staticmethod
    def altaTipoPropiedad():
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad añadida.")
                mbox.exec()
            else:
                mbox = eventos.Eventos.crearMensajeError("Aviso", "Error al añadir tipo de propiedad añadida.")
                mbox.exec()
            var.dlggestion.ui.txtTipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)

    @staticmethod
    def bajaTipoPropiedad():
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            if conexion.Conexion.bajaTipoprop(tipo):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad eliminada.")
                mbox.exec()
                eventos.Eventos.cargarTipoprop()
                var.dlggestion.ui.txtTipoprop.setText("")
            else:
                mbox = eventos.Eventos.crearMensajeError("Aviso","Error al eliminar tipo de propiedad.")
                mbox.exec()
        except Exception as e:
            print("Error baja tipo propiedad" + e)


    @staticmethod
    def altaPropiedad():
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.txtCpprop.text(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioVentaprop.text(), var.ui.txtPrecioAlquilerprop.text(),var.ui.areatxtDescriprop.toPlainText(),
                         var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]
            tipoOper = []
            if var.ui.rbtAlquilprop.isChecked():
                tipoOper.append(var.ui.rbtAlquilprop.text())
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

            conexion.Conexion.altaPropiedad(propiedad)
        except Exception as e:
            print(str(e))