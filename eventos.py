import csv
import json
import os
import sys
import time
import re
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHeaderView, QCompleter
from PyQt6.QtWidgets import QHeaderView

import locale

import clientes
import conexion
import conexionserver
import var
from PyQt6 import QtWidgets, QtGui, QtCore
import zipfile
import shutil

import vendedores

#Establecer configuracion regional

locale.setlocale(locale.LC_TIME,'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY,'es_ES.UTF-8')

class Eventos():
    @staticmethod
    def mensajeSalir():
        """

        Método que crea un mensaje de salida cuando queremos cerrar el programa, pidiendo confirmación. Si se confirma cierra el programa.

        """
        mbox = Eventos.crearMensajeConfirmacion('Salir', "¿Desea salir?")

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def crearMensajeConfirmacion(titulo_ventana, mensaje):
        """

        :param titulo_ventana: nombre de la ventana a crear
        :type titulo_ventana: str
        :param mensaje: mensaje de aviso en la ventana
        :type mensaje: str
        :return: devuelve la ventana de confirmación
        :rtype: QMessageBox

        Método que crea una ventana emergente que permite al usuario confirmar una acción crítica

        """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/icono.png'))
        mbox.setText(mensaje)
        mbox.setWindowTitle(titulo_ventana)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox

    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        """

        :param titulo_ventana: nombre de la ventana a crear
        :type titulo_ventana: str
        :param mensaje: mensaje de aviso en la ventana
        :type mensaje: str

        Método que ejecuta una ventana de información con un aviso

        """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        """

        :param titulo_ventana: nombre de la ventana a crear
        :type titulo_ventana: str
        :param mensaje: mensaje de aviso en la ventana
        :type mensaje: str

        Método que ejecuta una ventana de error con un aviso

        """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def cargarProv():
        """

        Método que carga todas las provincias en los diferentes comboBox del programa destinados a ellas

        """
        var.ui.cmbProvcli.clear()
        var.ui.cmbProvprop.clear()
        var.ui.cmbDeleVen.clear()
        listado = var.claseConexion.listaProv()
        var.provincias = listado

        var.ui.cmbProvcli.addItems(listado)
        var.ui.cmbProvprop.addItems(listado)
        var.ui.cmbDeleVen.addItems(listado)


    @staticmethod
    def cargaMunicli():
        """

        Método que carga los municipios de una provincia seleccionada en el panel de clientes y añade un completer al comboBox para facilitar la selección del municipio

        """
        var.ui.cmbMunicli.clear()
        provinciaCli = var.ui.cmbProvcli.currentText()
        listado = var.claseConexion.listaMunicipio(provinciaCli)
        var.ui.cmbMunicli.addItems(listado)

        var.municli = listado

        completer = QtWidgets.QCompleter(var.municli, var.ui.cmbMunicli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMunicli.setCompleter(completer)

    @staticmethod
    def cargaMuniprop():
        """

        Método que carga los municipios de una provincia seleccionada en el panel de propiedades y añade un completer al comboBox para facilitar la selección del municipio

        """
        var.ui.cmbMuniprop.clear()
        provinciaProp = var.ui.cmbProvprop.currentText()
        listado = var.claseConexion.listaMunicipio(provinciaProp)
        var.ui.cmbMuniprop.addItems(listado)

        var.muniprop = listado

        completer = QtWidgets.QCompleter(var.muniprop, var.ui.cmbMuniprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMuniprop.setCompleter(completer)

    @staticmethod
    def checkMunicipioCli():
        """

        Método que restablece el primer municipio de la lista en caso de que la opción escrita en el comboBox del panel de clientes no exista

        """
        if var.ui.cmbMunicli.currentText() not in var.municli:
            var.ui.cmbMunicli.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaCli():
        """

        Método que restablece la primera provincia de la lista en caso de que la opción escrita en el comboBox del panel de clientes no exista

        """
        if var.ui.cmbProvcli.currentText() not in var.provincias:
            var.ui.cmbProvcli.setCurrentIndex(0)

    @staticmethod
    def checkMunicipioProp():
        """

        Método que restablece el primer municipio de la lista en caso de que la opción escrita en el comboBox del panel de propiedades no exista

        """
        if var.ui.cmbMuniprop.currentText() not in var.muniprop:
            var.ui.cmbMuniprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaProp():
        """

        Método que restablece la primera provincia de la lista en caso de que la opción escrita en el comboBox del panel de propiedades no exista

        """
        if var.ui.cmbProvprop.currentText() not in var.provincias:
            var.ui.cmbProvprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaVen():
        """

        Método que restablece la primera provincia de la lista en caso de que la opción escrita en el comboBox del panel de vendedores no exista

        """
        if var.ui.cmbDeleVen.currentText() not in var.provincias:
            var.ui.cmbDeleVen.setCurrentIndex(0)

    @staticmethod
    def isDniValido(dni):
        """

        :param dni: el dni de un cliente o un vendedor
        :type dni: str
        :return: éxito si el dato introducido sigue el formato NIF
        :rtype: bool

        Método que comprueba que el dato introducido como Dni sigue el formato NIF

        """
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if dni.isdigit() and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False

        except Exception as error:
            print("error en validar dni ", error)

    @staticmethod
    def isMovilValido(movil):
        """

        :param movil: movil de cliente o de vendedor
        :type movil: int
        :return: éxito si sigue el formato móvil con 9 números empezando por 6 o 7
        :rtype: bool
        """
        regex = r"^[67]\d{8}$"
        return re.fullmatch(regex, movil)

    @staticmethod
    def cargarTick():
        """

        :return: devuelve la imagen de un tick verde
        :rtype: QPixmap

        Método que crea un pixmap con la imagen de un tick verde y la devuelve

        """
        pixmap = QPixmap("img/tick.svg")
        return pixmap

    @staticmethod
    def cargarCruz():
        """

        :return: devuelve la imagen de una cruz roja
        :rtype: QPixmap

        Método que crea un pixmap con la imagen de una cruz roja y la devuelve

        """
        pixmap = QPixmap("img/cruz.svg")
        return pixmap

    @staticmethod
    def abrirCalendar(pan, btn):
        """

        :param pan: panel actual
        :type pan: int
        :param btn: boton correspondiente en el panel
        :type btn: int

        Método que abre una ventana de calendario y setea el botón seleccionado y el panel actual

        """
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def cargaFecha(qDate):
        """

        :param qDate: día seleccionado
        :type qDate: datetime
        :return: datos formateados del día seleccionado
        :rtype: str

        Método que formatea el día seleccionado en el calendario y lo setea en el campo del panel corresponiente donde se haya llamado al calendario

        """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.panel == 1 and var.btn == 0:
                var.ui.txtAltaprop.setText(str(data))
            elif var.panel == 2 and var.btn == 0:
                var.ui.txtAltaVen.setText(str(data))
            elif var.panel == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.panel == 1 and var.btn == 1:
                var.ui.txtBajaprop.setText(str(data))
            elif var.panel == 2 and var.btn == 1:
                var.ui.txtBajaVen.setText(str(data))
            elif var.panel == 3 and var.btn == 0:
                var.ui.txtFechaFactura.setText(str(data))
            elif var.panel == 4 and var.btn == 0:
                var.ui.txtfechainicioalq.setText(str(data))
            elif var.panel == 4 and var.btn == 1:
                var.ui.txtfechafinalq.setText(str(data))

            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def isMailValido(mail):
        """

        :param mail: el email de un cliente o un vendedor
        :type mail: str
        :return: éxito al seguir el formato de un mail (una o más palabras separadas por un punto, seguidas por una arroba, seguida de al menos dos palabras separadas por punto)
        :rtype: bool

        Método que comprueba que un email sigue un formato específico

        """
        mail = mail.lower()
        regex = r'^([a-z0-9]+[\._])*[a-z0-9]+[@](\w+[.])*\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False

    @staticmethod
    def resizeTablaClientes():
        """

        Método que formatea la cabecera de la tabla de clientes

        """
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,3,6):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)


    @staticmethod
    def resizeTablaPropiedades():
        """

        Método que formatea la cabecera de la tabla de propiedades

        """
        try:
            header = var.ui.tablaProp.horizontalHeader()
            for i in range(header.count()):
                if i in (1,2,7):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaProp.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla propiedades ", e)

    @staticmethod
    def resizeTablaVendedores():
        """

        Método que formatea la cabecera de la tabla de vendedores

        """
        try:
            header = var.ui.tablaVendedores.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,2,4):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaVendedores.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla vendedores ", e)

    @staticmethod
    def resizeTablaFacturas():
        """

        Método que formatea la cabecera de la tabla de facturas

        """
        try:
            header = var.ui.tablaFacturas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaFacturas.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla facturas ", e)

    @staticmethod
    def resizeTablaVentas():
        """

        Método que formatea la cabecera de la tabla de ventas

        """
        try:
            header = var.ui.tablaVentas.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,1):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaVentas.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla ventas ", e)

    @staticmethod
    def resizeTablaContratos():
        """

        Método que formatea la cabecera de la tabla de ventas

        """
        try:
            header = var.ui.tablacontratosalq.horizontalHeader()
            for i in range(header.count()):
                if i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablacontratosalq.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla contratos ", e)

    @staticmethod
    def resizeTablaMensualidades():
        """

        Método que formatea la cabecera de la tabla de ventas

        """
        try:
            header = var.ui.tablaMensualidades.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,1):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaMensualidades.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla mensualidades ", e)

    @staticmethod
    def crearBackup():
        """

        Método para crear una copia de la base de datos en un directorio seleccionado por el usuario

        """
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia = str(fecha)+'_backup.zip'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, '.zip')
            if var.dlgAbrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, 'w')
                fichzip.write("bbdd.sqlite",os.path.basename("bbdd.sqlite"),zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)

                mbox = Eventos.crearMensajeInfo('Copia de seguridad',"Copia de seguridad creada.")
                mbox.exec()

        except Exception as error:
            print("error en crear backup: ", error)



    @staticmethod
    def restaurarBackup():
        """

        Método que restablece la base de datos seleccionada por el usuario

        """
        try:
            filename= var.dlgAbrir.getOpenFileName(None, "Restaurar Copia Seguridad","","*.zip;;All Files (*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = Eventos.crearMensajeInfo('Copia de seguridad',"Copia de seguridad restaurada.")
                mbox.exec()
                conexion.Conexion.db_conexion()
                Eventos.cargarProv()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        """

        Método que limpia todos los campos de datos del programa o los restablece a su opción por defecto

        """
        panelActual = var.ui.panPrincipal.currentIndex()
        if panelActual == 0:
            Eventos.limpiarPanelClientes()
        elif panelActual == 1:
            Eventos.limpiarPanelPropiedades()
        elif panelActual == 2:
            Eventos.limpiarPanelVendedores()
        elif panelActual == 3:
            Eventos.limpiarPanelVentas()
        elif panelActual == 4:
            Eventos.limpiarPanelAlquileres()

    @staticmethod
    def limpiarPanelAlquileres():
        """
        Método que limpia todos los campos de datos del panel de alquileres o los restablece a su opción por defecto

        """
        import alquileres
        objetosPanelAlquileres = [var.ui.lblnumalq, var.ui.txtnomeclialq, var.ui.txtapelclialq, var.ui.txtdniclialq,
                                  var.ui.txtidvenalq, var.ui.txtcodpropalq, var.ui.txtdirpropalq, var.ui.txtmunipropalq,
                                  var.ui.txttipopropalq, var.ui.txtprecioalq, var.ui.txtfechainicioalq,
                                  var.ui.txtfechafinalq]
        for dato in objetosPanelAlquileres:
            dato.setText("")
        var.ui.txtprecioalq.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')
        alquileres.Alquileres.cargarTablaContratos()
        var.ui.btnCrearContrato.setDisabled(False)
        alquileres.Alquileres.cargarTablaMensualidades(0, 0, 0)
        var.ui.btnModificarContrato.setDisabled(True)

    @staticmethod
    def limpiarPanelVentas():
        """
        Método que limpia todos los campos de datos del panel de ventas o los restablece a su opción por defecto

        """
        import facturas

        var.ui.txtFechaFactura.setText(datetime.now().strftime("%d/%m/%Y"))
        objetosPanelVentas = [var.ui.lblNumFactura, var.ui.txtdniclifac, var.ui.txtnomeclifac, var.ui.txtapelclifac,
                              var.ui.txtidvenfac, var.ui.txtcodpropfac, var.ui.txttipopropfac, var.ui.txtpreciofac,
                              var.ui.txtmunipropfac, var.ui.txtdirpropfac, var.ui.lblSubtotal, var.ui.lblIva,
                              var.ui.lblTotal]
        for dato in objetosPanelVentas:
            dato.setText("")
        var.ui.txtpreciofac.setStyleSheet('border-bottom: 1px solid black; background-color: rgb(255, 255, 255);')
        facturas.Facturas.cargaTablaVentas(0)
        var.ui.btnGrabarVenta.setDisabled(True)
        var.ui.btnInformeFactura.setDisabled(True)

    @staticmethod
    def limpiarPanelVendedores():
        """
        Método que limpia todos los campos de datos del panel de vendedores o los restablece a su opción por defecto

        """
        objetosPanelVendedores = [var.ui.lblIdVen, var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen,
                                  var.ui.txtBajaVen,
                                  var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
        for i, dato in enumerate(objetosPanelVendedores):
            if i == 7:
                pass
            else:
                dato.setText("")
        Eventos.cargarProv()
        var.ui.chkHistoriaVen.setChecked(False)
        vendedores.Vendedores.cargaTablaVendedores()

    @staticmethod
    def limpiarPanelPropiedades():
        """
        Método que limpia todos los campos de datos del panel de propiedades o los restablece a su opción por defecto

        """
        import propiedades
        objetosPanelProp = [var.ui.lblProp, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                            var.ui.cmbProvprop,
                            var.ui.cmbMuniprop, var.ui.cmbTipoprop,
                            var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop,
                            var.ui.txtPrecioVentaprop,
                            var.ui.txtCpprop, var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,
                            var.ui.chkVentaprop, var.ui.chkInterprop,
                            var.ui.chkAlquilprop, var.ui.rbtVentaprop, var.ui.txtNomeprop, var.ui.txtMovilprop]
        for i, dato in enumerate(objetosPanelProp):
            if i in (4, 5, 6):
                pass
            elif i in (7, 8):
                dato.setValue(0)
            elif i == 13:
                dato.setPlainText("")
            elif i == 14:
                dato.setChecked(True)
            elif i in (15, 16, 17, 18, 19):
                dato.setChecked(False)
            else:
                dato.setText("")
        var.ui.btnBuscaTipoProp.setChecked(False)
        propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def limpiarPanelClientes():
        """
        Método que limpia todos los campos de datos del panel de clientes o los restablece a su opción por defecto

        """
        objetosPanelCli = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                           var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,
                           var.ui.cmbMunicli, var.ui.txtBajacli]
        for i, dato in enumerate(objetosPanelCli):
            if i in (7, 8):
                pass
            else:
                dato.setText("")
        var.ui.lblTickcli.clear()
        var.ui.txtDnicli.setStyleSheet(
            'border: 1px solid black; border-radius: 5px; background-color: rgb(254, 255, 210)')
        var.ui.txtDnicli.setPlaceholderText("")
        var.ui.txtMovilcli.setPlaceholderText("")
        var.ui.txtMovilcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')
        var.ui.txtEmailcli.setPlaceholderText("")
        var.ui.txtEmailcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')

    @staticmethod
    def abrirTipoprop():
        """

        Método que muestra la ventana de gestión de tipo de propiedades

        """
        try:
            var.dlggestion.show()
        except Exception as e:
            print("error en abrir tipo prop: ", e)

    @staticmethod
    def exportCSVprop():
        """

        Método para exportar en formato csv los datos de las propiedades presentes en la base de datos

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha)+'_DatosPropiedades.csv'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a CSV", file, '.csv')
            if fichero:
                registros = var.claseConexion.cargarAllPropiedadesBD()
                with open(fichero, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Dirección","Provincia","Municipio","Tipo","Nº habitaciones","Nº Baños","Superficie","Precio Alquiler","Precio Compra","Código postal", "Observaciones","Operación","Estado","Propietario","Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                Eventos.crearMensajeError("Error","Se ha producido un error al exportar los datos en formato CSV.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def exportJSONprop():
        """

        Método para exportar en formato JSON los datos de las propiedades presentes en la base de datos

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha)+'_DatosPropiedades.json'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a JSON", file, '.json')
            if fichero:
                keys = ["Codigo","Alta","Baja","Dirección","Provincia","Municipio","Tipo","Nº habitaciones","Nº Baños","Superficie","Precio Alquiler","Precio Compra","Código postal", "Observaciones","Operación","Estado","Propietario","Móvil"]
                registros = var.claseConexion.cargarAllPropiedadesBD()
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonFile:
                    json.dump(lista_propiedades, jsonFile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                Eventos.crearMensajeError("Error","Se ha producido un error al exportar los datos en formato JSON.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def abrir_informeProp():
        """

        Método que muestra la ventana emergente para seleccionar municipio al crear un informe de propiedades

        """
        try:
            var.dlgInformeProp.show()
        except Exception as e:
            print("error en abrir informe propiedades: ", e)


    @staticmethod
    def abrir_about():
        """

        Método que muestra la ventana emergente con datos sobre el programa

        """
        try:
            var.dlgabout.show()
        except Exception as e:
            print("error en abrir about: ", e)


    @staticmethod
    def siguienteCli():
        """
        Método para actualizar el índice de la página actual en el panel de clientes a la siguiente

        """
        var.paginaActualCli += 1
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def anteriorCli():
        """
        Método para actualizar el índice de la página actual en el panel de clientes a la anterior

        """
        if var.paginaActualCli > 0:
            var.paginaActualCli -= 1
            clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def siguienteProp():
        """
        Método para actualizar el índice de la página actual en el panel de propiedades a la siguiente

        """
        import propiedades
        var.paginaActualProp += 1
        propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def anteriorProp():
        """
        Método para actualizar el índice de la página actual en el panel de propiedades a la anterior

        """
        import propiedades
        if var.paginaActualProp > 0:
            var.paginaActualProp -= 1
            propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def cambiarCliMaxpPagina():
        """

        Método que se encarga de que el número máximo de clientes por página que se establece no pase de 15

        """
        var.paginaActualCli = 0
        var.maxClientesPagina = int(var.ui.spinClipPag.text())
        if var.maxClientesPagina > 15:
            var.maxClientesPagina = 15
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def cambiarPropMaxpPagina():
        """

        Método que se encarga de que el número máximo de propiedades por página que se establece no pase de 10

        """
        import propiedades
        var.paginaActualProp = 0
        var.maxPropPagina = int(var.ui.spinProppPag.text())
        if var.maxPropPagina > 10:
            var.maxPropPagina = 10
        propiedades.Propiedades.cargarTablaPropiedades()


    @staticmethod
    def exportJSONven():
        """

        Método para exportar los datos de vendedores en formato JSON

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha)+'_DatosVendedores.json'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a JSON", file, '.json')
            if fichero:
                keys = ["Id","Dni","Nombre","Alta","Baja","Movil","Email","Delegacion"]
                registros = var.claseConexion.cargarAllVendedoresBD()
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonFile:
                    json.dump(lista_propiedades, jsonFile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                Eventos.crearMensajeError("Error","Se ha producido un error al exportar los datos en formato JSON.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)