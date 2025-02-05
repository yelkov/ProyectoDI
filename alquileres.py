import datetime
import locale

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from dateutil.relativedelta import relativedelta

import eventos
import var
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class Alquileres:
    @staticmethod
    def altaAlquiler():
        try:
            registro = [var.ui.txtcodpropalq.text(),var.ui.txtdniclialq.text(),var.ui.txtfechainicioalq.text(),var.ui.txtfechafinalq.text(),var.ui.txtidvenalq.text()]
            isAlquilada = var.claseConexion.propiedadIsAlquilada(var.ui.txtcodpropalq.text())
            isVendida = var.claseConexion.propiedadIsVendida(var.ui.txtcodpropalq.text())
            precio = var.ui.txtprecioalq.text()
            if isAlquilada or isVendida:
                eventos.Eventos.crearMensajeError("Error","La propiedad seleccionada ya se encuentra alquilada. No es posible crear el contrato.")
            elif not Alquileres.hasCamposObligatorios(registro):
                eventos.Eventos.crearMensajeError("Error","No se ha podido crear el contrato. Alguno de los campos necesarios está vacío. Recuerde seleccionar una propiedad, un cliente, un vendedor y fecha de inicio y fin de contrato.")
            elif precio == "":
                eventos.Eventos.crearMensajeError("Error","La propiedad seleccionada no está disponible para alquiler. Se debe modificar la actual o seleccionar otra disponible para alquiler.")
            elif var.claseConexion.altaAlquiler(registro) and Alquileres.generarMensualidades(registro):
                eventos.Eventos.crearMensajeInfo("Aviso","Se ha creado un nuevo contrato de alquiler.")
                eventos.Eventos.limpiarPanel()
            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error inesperado y no es posible generar un nuevo contrato de alquiler.")

        except Exception as e:
            print("Error alta alquiler en alquileres",str(e))


    @staticmethod
    def hasCamposObligatorios(registro):
        for dato in registro:
            if dato is None or dato == '':
                return False
            else:
                return True

    @staticmethod
    def cargarTablaContratos():
        try:
            listado = var.claseConexion.listadoAlquileres()
            var.ui.tablacontratosalq.setRowCount(len(listado))

            index = 0
            for registro in listado:
                var.ui.tablacontratosalq.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idContrato
                var.ui.tablacontratosalq.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1]))) #dniCliente
                var.ui.tablacontratosalq.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablacontratosalq.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
        except Exception as e:
            print("Error al cargar tablaContratos",str(e))

    @staticmethod
    def cargaOneContrato():
        try:
            var.ui.btnCrearContrato.setDisabled(True)
            fila = var.ui.tablacontratosalq.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOneAlquiler(str(datos[0]))

            listado = [var.ui.lblnumalq,var.ui.txtfechainicioalq, var.ui.txtfechafinalq, var.ui.txtidvenalq, var.ui.txtdniclialq, var.ui.txtnomeclialq, var.ui.txtapelclialq, var.ui.txtcodpropalq, var.ui.txttipopropalq, var.ui.txtprecioalq, var.ui.txtmunipropalq, var.ui.txtdirpropalq]
            var.ui.txtprecioalq.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')

            for i in range (len(listado)):
                if i != 9:
                    listado[i].setText(str(registro[i]))
                else:
                    precioAlq = f"{registro[i]:,.1f} €"
                    listado[i].setText(precioAlq)
            idAlquiler = registro[0]
            codPropiedad = registro[7]
            precio = registro[9]
            Alquileres.cargarTablaMensualidades(idAlquiler, codPropiedad, precio)


        except Exception as e:
            print("Error al cargar un contrato",str(e))


    @staticmethod
    def generarMensualidades(registro):
        try:
            codPropiedad = registro[0]
            dniCliente = registro[1]
            fechaInicioStr = registro[2]
            fechaFinalStr = registro[3]
            idAlquiler = var.claseConexion.idOneAlquiler(codPropiedad,dniCliente)

            fechaInicio = datetime.datetime.strptime(fechaInicioStr, "%d/%m/%Y")
            fechaFinal = datetime.datetime.strptime(fechaFinalStr, "%d/%m/%Y")

            while fechaInicio.year <= fechaFinal.year and (fechaInicio.year < fechaFinal.year or fechaInicio.month <= fechaFinal.month):
                mes = fechaInicio.strftime("%B").capitalize()
                mes_anio = f"{mes} {fechaInicio.year}"
                registro = [idAlquiler,mes_anio,0]
                if not var.claseConexion.altaMensualidad(registro):
                    return False
                fechaInicio += relativedelta(months=1)

            return True

        except ValueError as e:
            print("Error: Las fechas no tienen el formato correcto o no son válidas.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False

    @staticmethod
    def cargarTablaMensualidades(idAlquiler, codPropiedad, precio):
        try:
            listado = var.claseConexion.listadoMensualidades(idAlquiler)
            var.ui.tablaMensualidades.setRowCount(len(listado))

            index = 0
            for registro in listado:
                var.ui.tablaMensualidades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idMensualidad
                var.ui.tablaMensualidades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(codPropiedad)))
                var.ui.tablaMensualidades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaMensualidades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                var.ui.tablaMensualidades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                #creamos el boton
                var.botonAlq = QtWidgets.QCheckBox()
                var.botonAlq.setFixedSize(20,20)
                var.botonAlq.setIconSize(QtCore.QSize(20, 20))


                #creamos layout para centrar el boton
                layout = QHBoxLayout()
                layout.addWidget(var.botonAlq)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

                # Crear un widget contenedor para el layout y agregarlo a la celda
                container = QWidget()
                container.setLayout(layout)
                var.ui.tablaMensualidades.setCellWidget(index, 4, container)
                var.botonAlq.setChecked(registro[2] == 1)
                var.botonAlq.clicked.connect(lambda checked, idMensualidad=registro[0],: Alquileres.pagarMensualidad(idMensualidad))


                index += 1
        except Exception as e:
            print("Error al cargar tablaContratos",str(e))

    @staticmethod
    def pagarMensualidad(idMensualidad):
        if var.claseConexion.pagarMensualidad(idMensualidad):
            eventos.Eventos.crearMensajeInfo("Aviso","Se ha registrado el pago del mes.")
        else:
            eventos.Eventos.crearMensajeError("Error","Se ha producido un error.")