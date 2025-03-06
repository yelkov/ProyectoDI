import datetime

import locale

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QHBoxLayout, QWidget

import eventos
import informes
import var
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class Alquileres:
    @staticmethod
    def altaAlquiler():
        """

        Método para insertar un nuevo contrato de alquiler y generar las mensualidades en función de la fecha de inicio y de final

        """
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
                eventos.Eventos.limpiarPanelAlquileres()
            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error inesperado y no es posible generar un nuevo contrato de alquiler.")

        except Exception as e:
            print("Error alta alquiler en alquileres",str(e))


    @staticmethod
    def hasCamposObligatorios(registro):
        """

        :param registro: datos de contrato de alquiler
        :type registro: list
        :return: si contiene o no todos los campos obligatorios
        :rtype: bool

        Método para comprobar que el contrato de alquiler contiene los datos obligatorios

        """
        for dato in registro:
            if dato is None or dato == '':
                return False
            else:
                return True

    @staticmethod
    def cargarTablaContratos():
        """

        Método para cargar la tabla de contratos de alquiler

        """
        try:
            listado = var.claseConexion.listadoAlquileres()
            var.ui.tablacontratosalq.setRowCount(len(listado))

            index = 0
            for registro in listado:
                var.ui.tablacontratosalq.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idContrato
                var.ui.tablacontratosalq.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1]))) #dniCliente
                var.ui.tablacontratosalq.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablacontratosalq.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                var.botonDelContrato = QtWidgets.QPushButton()
                var.botonDelContrato.setFixedSize(25,25)
                var.botonDelContrato.setIconSize(QtCore.QSize(25, 25))
                var.botonDelContrato.setObjectName("botonEliminar")
                var.botonDelContrato.setIcon(QtGui.QIcon('./img/basura.png'))

                #creamos layout para centrar el boton
                layout = QHBoxLayout()
                layout.addWidget(var.botonDelContrato)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

                # Crear un widget contenedor para el layout y agregarlo a la celda
                container = QWidget()
                container.setLayout(layout)
                var.ui.tablacontratosalq.setCellWidget(index, 2, container)
                var.botonDelContrato.clicked.connect(lambda checked, idAlquiler=registro[0],: Alquileres.eliminarAlquiler(idAlquiler))


                index += 1
        except Exception as e:
            print("Error al cargar tablaContratos",str(e))

    @staticmethod
    def cargaOneContrato():
        """

        Método para cargar los datos de un contrato en los cuadros de texto correspondientes y las mensualidades en la tabla

        """
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
        """

        :param registro: datos de un contrato de alquiler
        :type registro: list
        :return: éxito o no al generar las mensualidades
        :rtype: bool

        Método que a partir de la fecha de inicio y de final de contrato genera las mensualidades de ese contrato

        """
        try:
            codPropiedad = registro[0]
            dniCliente = registro[1]
            fechaInicioStr = registro[2]
            fechaFinalStr = registro[3]
            idAlquiler = var.claseConexion.idOneAlquiler(codPropiedad,dniCliente)

            fechaInicio = datetime.datetime.strptime(fechaInicioStr, "%d/%m/%Y")
            fechaFinal = datetime.datetime.strptime(fechaFinalStr, "%d/%m/%Y")

            while fechaInicio <= fechaFinal:
                mes = fechaInicio.strftime("%B").capitalize()
                mes_anio = f"{mes} {fechaInicio.year}"
                registro = [idAlquiler,mes_anio,0]
                if not var.claseConexion.altaMensualidad(registro):
                    return False
                fechaInicio = Alquileres.sumar_un_mes(fechaInicio)
            return True

        except ValueError as e:
            print("Error: Las fechas no tienen el formato correcto o no son válidas.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return

    @staticmethod
    def sumar_un_mes(fecha):
        """

        :param fecha: fecha
        :type fecha: datetime
        :return: fecha con un mes más añadido
        :rtype: datetime

        Método para sumar un mes a una fecha determinada. Como no registramos el día del mes en las mensualidades, este método cambia el día a 1 para evitar problemas en la suma con febrero y meses de 30 días

        """
        mes = fecha.month + 1
        año = fecha.year
        if mes > 12:
            mes = 1
            año += 1
        dia = 1
        return fecha.replace(year=año,month=mes,day=dia)

    @staticmethod
    def cargarTablaMensualidades(idAlquiler, codPropiedad, precio):
        """

        :param idAlquiler: el id del contrato de alquiler
        :type idAlquiler: int
        :param codPropiedad: el id de la propiedad
        :type codPropiedad: int
        :param precio: precio mensual de alquiler
        :type precio: float

        Método para cargar todas las mensualidades en la tabla

        """
        try:
            var.ui.btnModificarContrato.setDisabled(False)
            listado = var.claseConexion.listadoMensualidades(idAlquiler)
            var.ui.tablaMensualidades.setRowCount(len(listado))

            index = 0
            for registro in listado:
                var.ui.tablaMensualidades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #idMensualidad
                var.ui.tablaMensualidades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(codPropiedad)))
                var.ui.tablaMensualidades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaMensualidades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio) + " €"))
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
                var.botonAlq.clicked.connect(lambda checked, checkbox = var.botonAlq, idMensualidad=registro[0],: Alquileres.pagarMensualidad(idMensualidad,checked,checkbox))

                #Creamos un boton para generar el informe
                var.botonInforme = QtWidgets.QPushButton()
                var.botonInforme.setFixedSize(20,20)
                var.botonInforme.setIconSize(QtCore.QSize(20, 20))
                #var.botonInforme.setObjectName("botonEliminar")
                var.botonInforme.setIcon(QtGui.QIcon('./img/informe.png'))

                #creamos layout para centrar el boton
                layout2 = QHBoxLayout()
                layout2.addWidget(var.botonInforme)
                layout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout2.setContentsMargins(0, 0, 0, 0)
                layout2.setSpacing(0)

                container2 = QWidget()
                container2.setLayout(layout2)
                var.ui.tablaMensualidades.setCellWidget(index, 5, container2)
                var.botonInforme.clicked.connect( lambda checked, idMensualidad=registro[0], idAlquilerInforme = idAlquiler: informes.Informes.reportReciboMes(idAlquilerInforme,idMensualidad))



                index += 1
        except Exception as e:
            print("Error al cargar tablaContratos",str(e))

    @staticmethod
    def pagarMensualidad(idMensualidad, checked,checkbox):
        """

        :param idMensualidad: identificador de la mensualidad
        :type idMensualidad: int
        :param checked: si esta marcado o no el botón checkbox de la tabla mensualidades
        :type checked: bool
        :param checkbox: referencia al boton checkbox de la tabla mensualidades
        :type checkbox: checkbox button

        Método para registrar como pagada una mensualidad y mostrar los cambios en la tabla

        """
        if not checked:
            eventos.Eventos.crearMensajeError("Error", "No se puede modificar un recibo ya pagado.")
            checkbox.setChecked(True)
        else:
            mbox = eventos.Eventos.crearMensajeConfirmacion("Aviso","Se va a pagar un recibo. Esta acción es irreversible. ¿Desea realizarla?")
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if var.claseConexion.pagarMensualidad(idMensualidad):
                    eventos.Eventos.crearMensajeInfo("Aviso","Se ha registrado el pago mensual.")
                else:
                    eventos.Eventos.crearMensajeError("Error","Se ha producido un error.")
            else:
                checkbox.setChecked(False)

    @staticmethod
    def modificarContrato():
        """

        Método para modificar un contrato existente en caso de aumentar o recortar la fecha de fin de contrato

        """
        registro = [var.ui.txtcodpropalq.text(),var.ui.txtdniclialq.text(),var.ui.txtfechainicioalq.text(),var.ui.txtfechafinalq.text(),var.ui.txtidvenalq.text()]
        nuevaFechaFinStr = registro[3]
        idContrato = var.ui.lblnumalq.text()

        datosContrato = var.claseConexion.datosOneAlquiler(idContrato)
        fechaFinRegistradaStr = datosContrato[2]

        nuevaFechaFin = datetime.datetime.strptime(nuevaFechaFinStr, "%d/%m/%Y")
        fechaFinRegistrada = datetime.datetime.strptime(fechaFinRegistradaStr, "%d/%m/%Y")

        if nuevaFechaFin == fechaFinRegistrada:
            eventos.Eventos.crearMensajeError("Error","La nueva fecha de fin de contrato es la misma que está registrada. No se ha modificado el contrato.")
        elif nuevaFechaFin > fechaFinRegistrada:
            if Alquileres.ampliarMensualidades(idContrato,fechaFinRegistrada,nuevaFechaFin) :
                eventos.Eventos.crearMensajeInfo("Aviso","Se han añadido nuevas mensualidades.")
                Alquileres.cargarTablaMensualidades(idContrato,datosContrato[7],datosContrato[9])
        elif nuevaFechaFin < fechaFinRegistrada:
            if Alquileres.eliminarMensualidades(idContrato, nuevaFechaFin):
                eventos.Eventos.crearMensajeInfo("Aviso","Se han actualizado correctamente los meses y se ha recortado el contrato.")
                Alquileres.cargarTablaMensualidades(idContrato,datosContrato[7],datosContrato[9])
            else:
                eventos.Eventos.crearMensajeError("Atención","Es posible que haya meses que no se han eliminado al detectarse pagos en el contrato. Es posible que se haya producido un error.")
                Alquileres.cargarTablaMensualidades(idContrato,datosContrato[7],datosContrato[9])
        else:
            eventos.Eventos.crearMensajeError("Error","Se ha producido un error inesperado.")

    @staticmethod
    def ampliarMensualidades(idAlquiler, fechaInicio, nuevaFechaFin):
        """

        :param idAlquiler: identificar de un contrato de alquiler
        :type idAlquiler: int
        :param fechaInicio: fecha de inicio a partir de la cual se van a añadir mensualidades
        :type fechaInicio: datetime
        :param nuevaFechaFin: fecha de finalización hasta la que se van a añadir mensualidades
        :type nuevaFechaFin: datetime
        :return: éxito al añadir mensualidades
        :rtype: bool

        Método para ampliar las mensualidades de un contrato existente

        """
        try:

            fechaInicio = Alquileres.sumar_un_mes(fechaInicio)

            while fechaInicio <= nuevaFechaFin:
                mes = fechaInicio.strftime("%B").capitalize()
                mes_anio = f"{mes} {fechaInicio.year}"
                registro = [idAlquiler,mes_anio,0]
                if not var.claseConexion.altaMensualidad(registro):
                    return False
                fechaInicio = Alquileres.sumar_un_mes(fechaInicio)

            nuevaFechaFin = nuevaFechaFin.strftime("%d/%m/%Y")
            var.claseConexion.modificarFechaFinContrato(idAlquiler,nuevaFechaFin)
            return True

        except ValueError as e:
            print("Error: Las fechas no tienen el formato correcto o no son válidas.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False


    @staticmethod
    def eliminarMensualidades(idAlquiler, nuevaFechaFin):
        """

        :param idAlquiler: identicador de un contrato de alquiler
        :type idAlquiler: int
        :param nuevaFechaFin: nueva fecha de finalización de un contrato de alquiler
        :type nuevaFechaFin: datetime
        :return: éxito al eliminar mensualidades de un contrato de alquiler
        :rtype: bool

        Método para reducir las mensualidades de un contrato de alquiler ya registrado

        """
        try:

            mensualidades = var.claseConexion.listadoMensualidades(idAlquiler)
            for i in range(len(mensualidades)-1, -1, -1):
                idMensualidad = mensualidades[i][0]
                mesStr = mensualidades[i][1]
                mes = datetime.datetime.strptime(mesStr, "%B %Y")
                isPagado = mensualidades[i][2]

                if nuevaFechaFin < mes and not isPagado:
                    var.claseConexion.eliminarMensualidad(idMensualidad)
                elif nuevaFechaFin > mes:
                    break;
                elif isPagado:
                    return False

            nuevaFechaFin = nuevaFechaFin.strftime("%d/%m/%Y")
            var.claseConexion.modificarFechaFinContrato(idAlquiler, nuevaFechaFin)
            return True
        except Exception as e:
            print("Error eliminando mensualidades en alquileres", str(e))


    @staticmethod
    def eliminarAlquiler(idAlquiler):
        """

        :param idAlquiler: identificador de contrato de alquiler
        :type idAlquiler: int

        Método para eliminar un contrato de alquiler si este no tiene mensualidades ya pagadas

        """
        try:
            codProp = var.ui.txtcodpropalq.text()
            precio = var.ui.txtprecioalq.text()
            hasMensualidadesPagadas = False
            mensualidades = var.claseConexion.listadoMensualidades(idAlquiler)
            for mensualidad in mensualidades:
                isPagado = mensualidad[2]
                if isPagado:
                    hasMensualidadesPagadas = True
                    break

            mbox = eventos.Eventos.crearMensajeConfirmacion('Eliminar contrato', "¿Desea eliminar el contrato de alquiler seleccionado? Tenga en cuenta que la acción es irreversible.")
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if hasMensualidadesPagadas:
                    Alquileres.eliminarMensualidades(idAlquiler, datetime.datetime.now())
                    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
                    var.claseConexion.finalizarContrato(idAlquiler,codProp,fecha_hoy)
                    Alquileres.cargarTablaMensualidades(idAlquiler,codProp,precio)
                    eventos.Eventos.crearMensajeInfo("Aviso","Se han eliminado las mensualidades pendientes. El contrato no se puede eliminar, ya existen mensualidades pagadas.")
                elif not hasMensualidadesPagadas and var.claseConexion.eliminarContratoAlquiler(idAlquiler):
                    eventos.Eventos.crearMensajeInfo("Aviso","Se ha eliminado el contrato de alquiler.")
                    Alquileres.cargarTablaContratos()
                    Alquileres.cargarTablaMensualidades(0,0,0)
                else:
                    eventos.Eventos.crearMensajeError("Error","Se ha producido un error y no se ha eliminado el contrato de alquiler.")

        except Exception as e:
            print("Error al eliminar un alquiler en alquileres", str(e))
