import datetime

import conexion
import conexionserver
import eventos
import var
import re
from PyQt6 import QtWidgets, QtGui, QtCore

from eventos import Eventos


class Propiedades():

    @staticmethod
    def altaTipoPropiedad(venDialogo):
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            #registro = conexion.Conexion.altaTipoprop(tipo)
            #registro = conexionserver.ConexionServer.altaTipoprop(tipo)
            registro = var.claseConexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad añadida.")

                Propiedades.cargarTipopropGestion(venDialogo)
            else:
                eventos.Eventos.crearMensajeError("Aviso", "Error al añadir tipo de propiedad añadida.")

            var.dlggestion.ui.txtTipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)

    @staticmethod
    def bajaTipoPropiedad(venDialogo):
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            #if conexion.Conexion.bajaTipoprop(tipo):
            #if conexionserver.ConexionServer.bajaTipoprop(tipo):
            if var.claseConexion.bajaTipoprop(tipo):
                eventos.Eventos.crearMensajeInfo("Aviso","Tipo de propiedad eliminada.")
                Propiedades.cargarTipoprop()
                var.dlggestion.ui.txtTipoprop.setText("")
                Propiedades.cargarTipopropGestion(venDialogo)
            else:
                eventos.Eventos.crearMensajeError("Aviso","Error al eliminar tipo de propiedad.")
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

            propiedad.append(var.ui.txtNomeprop.text().title())
            propiedad.append(var.ui.txtMovilprop.text())

            precioAlquiler = propiedad[8]
            precioVenta = propiedad[9]

            #if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and conexion.Conexion.altaPropiedad(propiedad):
            #if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and conexionserver.ConexionServer.altaPropiedad(propiedad):
            if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and var.claseConexion.altaPropiedad(propiedad):
                eventos.Eventos.crearMensajeInfo("Aviso", "Se ha grabado la propiedad en la base de datos.")
                Propiedades.cargarTablaPropiedades()

            elif not Propiedades.hasCamposObligatoriosAlta(propiedad):
                eventos.Eventos.crearMensajeError("Error", "Hay campos vacíos que deben ser cubiertos.")

            elif not Propiedades.checkPrecioAlquiler(precioAlquiler):
                eventos.Eventos.crearMensajeError("Error","Para guardar una propiedad de tipo alquiler debe guardarse un precio y estar marcada la casilla 'Alquiler'.")

            elif not Propiedades.checkPrecioVenta(precioVenta):
                eventos.Eventos.crearMensajeError("Error","Para guardar una propiedad de tipo venta debe guardarse un precio y estar marcada la casilla 'Venta'.")
            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error al grabar la propiedad.")
        except Exception as e:
            print(str(e))

    @staticmethod
    def checkMovilProp(movil):
        try:
            if eventos.Eventos.isMovilValido(movil):
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
            listado = var.claseConexion.listadoPropiedades()
            var.lenPropiedades = len(listado)

            var.ui.spinProppPag.setValue(var.maxPropPagina)

            if len(listado) == 0:
                var.ui.btnSiguienteProp.setDisabled(True)
                var.ui.btnAnteriorProp.setDisabled(True)
                var.ui.tablaProp.setRowCount(4)
                var.ui.tablaProp.setItem(0, 0, QtWidgets.QTableWidgetItem("No hay propiedades con los filtros seleccionados"))
                var.ui.tablaProp.setSpan(0,0,4,9)
                var.ui.tablaProp.item(0,0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.lblPaginasProp.setText("Página 0/0")
            else:
                var.ui.tablaProp.clearSpans()

                inicioListado = var.paginaActualProp * var.maxPropPagina
                sublistado = listado[inicioListado: inicioListado + var.maxPropPagina]

                if listado[0] == sublistado[0]:
                    var.ui.btnAnteriorProp.setDisabled(True)
                else:
                    var.ui.btnAnteriorProp.setDisabled(False)

                if listado[-1] == sublistado[-1]:
                    var.ui.btnSiguienteProp.setDisabled(True)
                else:
                    var.ui.btnSiguienteProp.setDisabled(False)

                numPaginas = (var.lenPropiedades // var.maxPropPagina) + 1
                if len(listado) % var.maxPropPagina == 0:
                    numPaginas -= 1
                var.ui.lblPaginasProp.setText("Página "+str(var.paginaActualProp + 1)+"/"+str(numPaginas))

                var.ui.tablaProp.setRowCount(len(sublistado))
                index = 0
                for registro in sublistado:
                    registro = [x if x != None else '' for x in registro]
                    var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #codigo
                    var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[5])) #municipio
                    var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[6])) #tipo_provincia
                    var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7]))) #num_habitaciones
                    var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8]))) #num_baños

                    if var.claseConexion == conexion.Conexion:
                        precio_alquiler = f"{registro[10]:,.1f} €" if registro[10] != ""  else " - €"
                        var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(precio_alquiler)) #precio_alqui

                        precio_venta = f"{registro[11]:,.1f} €" if registro[11] != ""  else " - €"
                        var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(precio_venta)) #precio_venta

                        tipo_operacion = registro[14].replace('[', '').replace(']', '').replace("'","")
                        var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(tipo_operacion)) #tipo_operacion

                    elif var.claseConexion == conexionserver.ConexionServer:
                        var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[10]) + " €"))
                        var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[11]) + " €"))
                        var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14].replace('[', '').replace(']', '').replace("'",""))))

                    var.ui.tablaProp.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2]))) #fecha de baja

                    var.ui.tablaProp.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1


        except Exception as e:
            print("Error al cargar propiedades en la tabla cargarTablaPropiedades", e)

    @staticmethod
    def cargaOnePropiedad():
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOnePropiedad(str(datos[0]))

            listado = [var.ui.lblProp,var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,var.ui.cmbProvprop,var.ui.cmbMuniprop,var.ui.cmbTipoprop,var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop,var.ui.txtPrecioAlquilerprop,var.ui.txtPrecioVentaprop,var.ui.txtCpprop,var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,var.ui.rbtVentaprop,var.ui.chkInterprop,var.ui.chkAlquilprop,var.ui.chkVentaprop,var.ui.txtNomeprop,var.ui.txtMovilprop]

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
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(registro[i])

            var.ui.txtcodpropfac.setText(registro[0])
            var.ui.txtdirpropfac.setText(registro[3])
            var.ui.txtmunipropfac.setText(registro[5])
            var.ui.txttipopropfac.setText(registro[6])
            precio_venta = registro[11]
            if precio_venta is not None and precio_venta != "":
                precio_venta_float = float(precio_venta)
                precio_venta_formateado = f"{precio_venta_float:,.1f} €"
                var.ui.txtpreciofac.setText(precio_venta_formateado)
                var.ui.txtpreciofac.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtpreciofac.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic; background-color: #de6767')
                var.ui.txtpreciofac.setText(None)




        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)

    @staticmethod
    def modifProp():
        try:
            propiedad = [var.ui.lblProp.text(),var.ui.txtAltaprop.text(),var.ui.txtBajaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),var.ui.cmbMuniprop.currentText(),var.ui.cmbTipoprop.currentText(),var.ui.spinHabprop.text(),var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),var.ui.txtPrecioAlquilerprop.text(),var.ui.txtPrecioVentaprop.text(),var.ui.txtCpprop.text(),var.ui.areatxtDescriprop.toPlainText()]
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

            propiedad.append(var.ui.txtNomeprop.text().title())
            propiedad.append(var.ui.txtMovilprop.text())

            fecha_baja = propiedad[2]
            precioAlquiler = propiedad[10]
            precioVenta = propiedad[11]

            if fecha_baja != "" and not Propiedades.esFechasValidas(propiedad):
                eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")

            elif fecha_baja != "" and var.ui.rbtDisponprop.isChecked():
                eventos.Eventos.crearMensajeError("Error", "No es posible guardar fecha de baja si el estado del inmueble es 'Disponible'.")

            elif Propiedades.hasCamposObligatoriosModif(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and var.claseConexion.modifProp(propiedad):
                eventos.Eventos.crearMensajeInfo("Aviso","Se ha modificado la propiedad correctamente.")
                Propiedades.cargarTablaPropiedades()

            elif not Propiedades.hasCamposObligatoriosModif(propiedad):
                eventos.Eventos.crearMensajeError("Error","Hay algunos campos obligatorios que están vacíos.")

            elif not Propiedades.checkPrecioAlquiler(precioAlquiler):
                eventos.Eventos.crearMensajeError("Error","Para guardar una propiedad de tipo alquiler debe guardarse un precio y estar marcada la casilla 'Alquiler'.")

            elif not Propiedades.checkPrecioVenta(precioVenta):
                eventos.Eventos.crearMensajeError("Error","Para guardar una propiedad de tipo venta debe guardarse un precio y estar marcada la casilla 'Venta'.")

            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error al modificar la propiedad")

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)

    @staticmethod
    def bajaProp():
        propiedad = [var.ui.lblProp.text(),var.ui.txtAltaprop.text(),var.ui.txtBajaprop.text()]
        if var.ui.rbtAlquilprop.isChecked():
            propiedad.append(var.ui.rbtAlquilprop.text())
        elif var.ui.rbtVentaprop.isChecked():
            propiedad.append(var.ui.rbtVentaprop.text())



        if propiedad[2] == "" or propiedad[2] is None:
            eventos.Eventos.crearMensajeError("Error","Es necesario elegir una fecha para dar de baja la propiedad.")

        elif not var.ui.rbtDisponprop.isChecked() and var.claseConexion.bajaProp(propiedad) and Propiedades.esFechasValidas(propiedad):
            eventos.Eventos.crearMensajeInfo("Aviso", "Se ha dado de baja la propiedad.")
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()

        elif var.ui.rbtDisponprop.isChecked():
            eventos.Eventos.crearMensajeError("Error","Para dar de baja el estado de la propiedad no puede ser disponible.")

        elif not Propiedades.esFechasValidas(propiedad):
            eventos.Eventos.crearMensajeError("Error", "La fecha de baja no puede ser anterior a la fecha de alta.")

        else:
            eventos.Eventos.crearMensajeError("Error","Se ha producido un error al dar de baja la propiedad.")


    @staticmethod
    def historicoProp():
        try:
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("checkbox historico no funciona correcatamente", e)

    @staticmethod
    def buscaProp():
        try:
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("búsqueda filtrada no funciona correcatamente", e)

    @staticmethod
    def hasCamposObligatoriosAlta(datosPropiedades):
        datos = datosPropiedades[:]
        descripcion = datos.pop(11)
        precio_alquiler = datos.pop(9)
        precio_venta = datos.pop(8)
        num_banos = datos.pop(6)
        num_habitaciones = datos.pop(5)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    @staticmethod
    def hasCamposObligatoriosModif(datosPropiedades):
        datos = datosPropiedades[:]
        descripcion = datos.pop(13)
        precio_venta = datos.pop(11)
        precio_alquiler = datos.pop(10)
        num_banos = datos.pop(8)
        num_habitaciones = datos.pop(7)
        fecha_baja = datos.pop(2)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    @staticmethod
    def esFechasValidas(datosPropiedades):
        datos = datosPropiedades[:]
        alta = datos[1]
        baja = datos[2]

        try:
            fecha_alta = datetime.datetime.strptime(alta, "%d/%m/%Y")
            fecha_baja = datetime.datetime.strptime(baja, "%d/%m/%Y")

            return fecha_alta < fecha_baja #si fecha de alta es posterior a fecha de baja devuelve false

        except ValueError as e:
            print("Error: La fecha no tiene el formato correcto o no es válida.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False

    @staticmethod
    def is_num(value):
        return bool(re.match(r'^-?\d+(\.\d+)?$', str(value)))

    @staticmethod
    def checkPrecioAlquiler(precioAlquiler):
        if Propiedades.is_num(precioAlquiler) and var.ui.chkAlquilprop.isChecked():
            return True
        elif (precioAlquiler == "" or precioAlquiler is None) and not var.ui.chkAlquilprop.isChecked():
            return True
        else:
            return False

    @staticmethod
    def checkPrecioVenta(precioVenta):
        if Propiedades.is_num(precioVenta) and var.ui.chkVentaprop.isChecked():
            return True
        elif (precioVenta == "" or precioVenta is None) and not var.ui.chkVentaprop.isChecked():
            return True
        else:
            return False


    @staticmethod
    def filtrar():
        checkeado = var.ui.btnBuscaTipoProp.isChecked()
        var.ui.btnBuscaTipoProp.setChecked(not checkeado)
        Propiedades.cargarTablaPropiedades()

    @staticmethod
    def activarCheckPrecios():
        if var.ui.txtPrecioVentaprop.text() != "":
            var.ui.chkVentaprop.setChecked(True)
        else:
            var.ui.chkVentaprop.setChecked(False)

        if var.ui.txtPrecioAlquilerprop.text() != "":
            var.ui.chkAlquilprop.setChecked(True)
        else:
            var.ui.chkAlquilprop.setChecked(False)

    @staticmethod
    def cambiarAvailableRbt():
        if var.ui.txtBajaprop.text() == "" or var.ui.txtBajaprop.text() is None:
            var.ui.rbtDisponprop.setEnabled(True)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setEnabled(False)
            var.ui.rbtDisponprop.setChecked(True)
        else:
            var.ui.rbtAlquilprop.setEnabled(True)
            var.ui.rbtAlquilprop.setChecked(True)
            var.ui.rbtVentaprop.setEnabled(True)
            var.ui.rbtDisponprop.setEnabled(False)


    @staticmethod
    def cargarTipoprop():
        registro = var.claseConexion.cargarTipoprop()
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(registro)

    def seleccionarTipoGestion(self):
        tipo = self.ui.cmbTipopropGestion.currentText()
        self.ui.txtTipoprop.setText(tipo)

    def cargarTipopropGestion(self):
        registro = var.claseConexion.cargarTipoprop()
        self.ui.cmbTipopropGestion.clear()
        self.ui.cmbTipopropGestion.addItems(registro)


    def cargaMuniInformeProp(self):
        registro = var.claseConexion.cargarMunicipios()
        registro.insert(0,"")
        self.ui.cmbInformeMuniProp.setEditable(True)
        self.ui.cmbInformeMuniProp.clear()
        self.ui.cmbInformeMuniProp.addItems(registro)
        completer = QtWidgets.QCompleter(registro, self.ui.cmbInformeMuniProp)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.ui.cmbInformeMuniProp.setCompleter(completer)
