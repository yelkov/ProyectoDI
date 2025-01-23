import sys
from idlelib.window import registry

from PyQt6.QtWidgets import QHBoxLayout, QWidget

import conexion
import eventos
import propiedades
import var
from PyQt6 import QtWidgets, QtCore, QtGui

class Facturas:

    @staticmethod
    def altaFactura():
        try:
            nuevaFactura = [var.ui.txtFechaFactura.text(),var.ui.txtdniclifac.text()]
            if var.ui.txtdniclifac.text() == "" or var.ui.txtdniclifac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","Recuerda seleccionar un cliente antes de grabar una factura")
            elif var.ui.txtFechaFactura.text() == "" or var.ui.txtFechaFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","No es posible grabar una factura sin seleccionar una fecha")
            elif conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.crearMensajeInfo("Factura grabada","Se ha grabado una nueva factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido grabar factura")
        except Exception as e:
            print("factura",e)


    @staticmethod
    def cargaTablaFacturas():
        try:
            listado = var.claseConexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idFactura
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1])) #dniCliente
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2])) #fechaFactura
                var.ui.tablaFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                #creamos el boton
                var.botondel = QtWidgets.QPushButton()
                var.botondel.setFixedSize(25,25)
                var.botondel.setIconSize(QtCore.QSize(25, 25))
                var.botondel.setObjectName("botonEliminar")
                var.botondel.setIcon(QtGui.QIcon('./img/basura.png'))

                #creamos layout para centrar el boton
                layout = QHBoxLayout()
                layout.addWidget(var.botondel)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

                # Crear un widget contenedor para el layout y agregarlo a la celda
                container = QWidget()
                container.setLayout(layout)
                var.ui.tablaFacturas.setCellWidget(index, 3, container)
                var.botondel.clicked.connect(lambda checked, idFactura=registro[0]: Facturas.eliminarFactura(idFactura))

                index += 1

        except Exception as e:
            print("Error cargaFacturas en cargaTablaFacturas", e)

    @staticmethod
    def eliminarFactura(idFactura):
        try:
            mbox = eventos.Eventos.crearMensajeConfirmacion('Eliminar factura', "¿Desea eliminar la factura seleccionada? Tenga en cuenta que la acción es irreversible.")
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if var.claseConexion.deleteFactura(idFactura):
                    eventos.Eventos.crearMensajeInfo("Factura eliminada correctamente","Se ha eliminado la factura seleccionada.")
                    Facturas.cargaTablaFacturas()
                    Facturas.cargaTablaVentas(idFactura)
                else:
                    eventos.Eventos.crearMensajeError("Error al eliminar factura","No se ha podido eliminar la factura.")
            else:
                    mbox.hide()

        except Exception as e:
            print("Error al eliminar factura en ",e)

    @staticmethod
    def cargaOneFactura():
        try:
            fila = var.ui.tablaFacturas.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOneFactura(str(datos[0]))
            listado = [var.ui.lblNumFactura,var.ui.txtFechaFactura,var.ui.txtdniclifac]
            for i in range (len(listado)):
                listado[i].setText(str(registro[i]))

            datosCliente = var.claseConexion.datosOneCliente(str(datos[1]))
            var.ui.txtnomeclifac.setText(str(datosCliente[3]))
            var.ui.txtapelclifac.setText(str(datosCliente[4]))

            camposVenta = [var.ui.txtidvenfac,var.ui.txtcodpropfac,var.ui.txtpreciofac, var.ui.txttipopropfac, var.ui.txtmunipropfac, var.ui.txtdirpropfac]

            for i in range (len(camposVenta)):
                camposVenta[i].clear()

            var.ui.txtpreciofac.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')
            Facturas.cargaTablaVentas(registro[0])
        except Exception as e:
            print("Error al cargar una factura en facturas",e)


    @staticmethod
    def altaVenta():
        nuevaVenta = [var.ui.lblNumFactura.text(),var.ui.txtcodpropfac.text(), var.ui.txtidvenfac.text()]
        precio = var.ui.txtpreciofac.text()
        if nuevaVenta[0] == "":
            eventos.Eventos.crearMensajeError("Error","Recuerde seleccionar una factura de la tabla de facturas.")
        elif precio == "":
            eventos.Eventos.crearMensajeError("Error","La propiedad seleccionada no está disponible para venta. Se debe modificar o seleccione otra disponible.")
        elif nuevaVenta[1] == "":
            eventos.Eventos.crearMensajeError("Error","No se posible crear una nueva venta si no se ha seleccionado una propiedad")
        elif nuevaVenta[2] == "":
            eventos.Eventos.crearMensajeError("Error","No es posible crear una nueva venta si no se ha seleccionado a un vendedor previamente.")
        elif var.claseConexion.altaVenta(nuevaVenta) and var.claseConexion.venderPropiedad(nuevaVenta[1]):
            eventos.Eventos.crearMensajeInfo("Aviso","Se ha grabado una venta exitosamente.")
            Facturas.cargaTablaVentas(var.ui.lblNumFactura.text())
            propiedades.Propiedades.cargarTablaPropiedades()
        else:
            eventos.Eventos.crearMensajeError("Error","Se ha producido un error inesperado")

    @staticmethod
    def cargaTablaVentas(idFactura):
        try:
            listado = var.claseConexion.listadoVentas(idFactura)
            var.ui.tablaVentas.setRowCount(len(listado))
            index = 0
            subtotal = 0
            for registro in listado:
                var.ui.tablaVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idVenta
                var.ui.tablaVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1]))) #codigoPropiedad
                var.ui.tablaVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2])) #direccion
                var.ui.tablaVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[3])) #municipio
                var.ui.tablaVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[4])) #tipo
                precio_venta = f"{registro[5]:,.1f} €"
                var.ui.tablaVentas.setItem(index, 5, QtWidgets.QTableWidgetItem(precio_venta)) #precio
                var.ui.tablaVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVentas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVentas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVentas.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVentas.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVentas.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                subtotal += registro[5]

                index += 1

            iva = subtotal * 0.21
            total = subtotal + iva
            subTotalStr = f"{subtotal:,.1f} €"
            ivaStr = f"{iva:,.1f} €"
            totalStr = f"{total:,.1f} €"
            var.ui.lblSubtotal.setText(subTotalStr)
            var.ui.lblIva.setText(ivaStr)
            var.ui.lblTotal.setText(totalStr)

        except Exception as e:
            print("Error cargaVentas en cargaTablaVentas", e)

    @staticmethod
    def cargaOneVenta():
        try:
            fila = var.ui.tablaVentas.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOneVenta(str(datos[0]))
            listado = [var.ui.txtidvenfac,var.ui.txtcodpropfac, var.ui.txttipopropfac, var.ui.txtpreciofac, var.ui.txtmunipropfac, var.ui.txtdirpropfac]
            var.ui.txtpreciofac.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')
            for i in range (len(listado)):
                if i != 3:
                    listado[i].setText(str(registro[i]))
                else:
                    precioVenta = f"{registro[i]:,.1f} €"
                    listado[i].setText(precioVenta)

        except Exception as e:
            print("Error al cargar UNA venta en facturas",e)