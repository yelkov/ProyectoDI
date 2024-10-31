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
                Propiedades.cargarTablaPropiedades()
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

    @staticmethod
    def cargarTablaPropiedades():
        try:
            listado = conexion.Conexion.listadoPropiedades()
            index = 0
            for registro in listado:
                var.ui.tablaProp.setRowCount(index + 1)
                var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #codigo
                var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[4])) #municipio
                var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[6])) #tipo_provincia
                var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7]))) #num_habitaciones
                var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8]))) #num_baños

                precio_alquiler = f"{registro[10]:,.1f} €" if registro[10] != ""  else ""
                var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(precio_alquiler)) #precio_alqui

                precio_venta = f"{registro[11]:,.1f} €" if registro[11] != ""  else ""
                var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(precio_venta)) #precio_venta

                tipo_operacion = registro[14].replace('[', '').replace(']', '').replace("'","")
                var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(tipo_operacion)) #tipo_operacion
                index += 1

        except Exception as e:
            print("Error al cargar propiedades en la tabla cargarTablaPropiedades", e)

    @staticmethod
    def cargaOnePropiedad():
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            listado = [var.ui.lblProp,var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,var.ui.cmbProvprop,
                       var.ui.cmbMuniprop,var.ui.cmbTipoprop,
                       var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop,var.ui.txtPrecioAlquilerprop,
                       var.ui.txtPrecioVentaprop,
                       var.ui.txtCpprop,var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,var.ui.rbtVentaprop,var.ui.chkInterprop,
                       var.ui.chkAlquilprop,var.ui.chkVentaprop,var.ui.txtNomeprop,var.ui.txtMovilprop]
            for i in range(len(listado)):
                if i in (4,5,6):
                    listado[i].setCurrentText(registro[i])
                elif i in (7,8):
                    listado[i].setValue(int(registro[i]))
                elif i == 13:
                    listado[i].setPlainText(registro[i])
                elif i == 14:
                    listado[i].setChecked(registro[15] == "Disponible")
                elif i == 15:
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17,18,19):
                    listado[17].setChecked("Venta" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Intercambio" in registro[14])
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(registro[i])

        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)