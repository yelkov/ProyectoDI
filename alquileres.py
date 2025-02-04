from PyQt6 import QtWidgets, QtCore

import eventos
import var


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
            elif var.claseConexion.altaAlquiler(registro):
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


        except Exception as e:
            print("Error al cargar un contrato",str(e))

