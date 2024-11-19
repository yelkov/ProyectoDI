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
import eventos
import clientes
import conexion
import conexionserver
import var
from PyQt6 import QtWidgets, QtGui, QtCore
import zipfile
import shutil

#Establecer configuracion regional

locale.setlocale(locale.LC_TIME,'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY,'es_ES.UTF-8')

class Eventos():
    @staticmethod
    def mensajeSalir():
        mbox = Eventos.crearMensajeSalida('Salir',"¿Desea salir?")

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
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
        var.ui.cmbProvcli.clear()
        var.ui.cmbProvprop.clear()
        listado = conexion.Conexion.listaProv()
        #listado = conexionserver.ConexionServer.listaProv()
        var.provincias = listado

        var.ui.cmbProvcli.addItems(listado)
        var.ui.cmbProvprop.addItems(listado)

    @staticmethod
    def cargaMunicli():
        var.ui.cmbMunicli.clear()
        provinciaCli = var.ui.cmbProvcli.currentText()
        listado = conexion.Conexion.listaMunicipio(provinciaCli)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicli.addItems(listado)

        var.municli = listado

        completer = QtWidgets.QCompleter(var.municli, var.ui.cmbMunicli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMunicli.setCompleter(completer)

    @staticmethod
    def cargaMuniprop():
        var.ui.cmbMuniprop.clear()
        provinciaProp = var.ui.cmbProvprop.currentText()
        listado = conexion.Conexion.listaMunicipio(provinciaProp)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMuniprop.addItems(listado)

        var.muniprop = listado

        completer = QtWidgets.QCompleter(var.muniprop, var.ui.cmbMuniprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMuniprop.setCompleter(completer)

    @staticmethod
    def checkMunicipioCli():
        if var.ui.cmbMunicli.currentText() not in var.municli:
            var.ui.cmbMunicli.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaCli():
        if var.ui.cmbProvcli.currentText() not in var.provincias:
            var.ui.cmbProvcli.setCurrentIndex(0)

    @staticmethod
    def checkMunicipioProp():
        if var.ui.cmbMuniprop.currentText() not in var.muniprop:
            var.ui.cmbMuniprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaProp():
        if var.ui.cmbProvprop.currentText() not in var.provincias:
            var.ui.cmbProvprop.setCurrentIndex(0)

    @staticmethod
    def isDniValido(dni):
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
        regex = r"^[67]\d{8}$"
        return re.fullmatch(regex, movil)

    @staticmethod
    def cargarTick():
        pixmap = QPixmap("img/tick.svg")
        return pixmap

    @staticmethod
    def cargarCruz():
        pixmap = QPixmap("img/cruz.svg")
        return pixmap

    @staticmethod
    def abrirCalendar(pan, btn):
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.panel == 1 and var.btn == 0:
                var.ui.txtAltaprop.setText(str(data))
            elif var.panel == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.panel == 1 and var.btn == 1:
                var.ui.txtBajaprop.setText(str(data))
            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def isMailValido(mail):
        mail = mail.lower()
        regex = r'^([a-z0-9]+[\._])*[a-z0-9]+[@](\w+[.])*\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False

    @staticmethod
    def resizeTablaClientes():
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
            print("error en resize tabla clientes ", e)

    @staticmethod
    def crearBackup():
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
                eventos.Eventos.cargarProv()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        import propiedades
        objetosPanelCli = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                   var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,var.ui.cmbMunicli,var.ui.txtBajacli]
        for i, dato in enumerate(objetosPanelCli):
            if i in (7,8):
                pass
            else:
                dato.setText("")

        var.ui.lblTickcli.clear()
        var.ui.txtDnicli.setStyleSheet('border: 1px solid black; border-radius: 5px; background-color: rgb(254, 255, 210)')
        var.ui.txtDnicli.setPlaceholderText("")
        var.ui.txtMovilcli.setPlaceholderText("")
        var.ui.txtMovilcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')
        var.ui.txtEmailcli.setPlaceholderText("")
        var.ui.txtEmailcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')

        objetosPanelProp = [var.ui.lblProp, var.ui.txtAltaprop,var.ui.txtBajaprop,var.ui.txtDirprop,var.ui.cmbProvprop,
                            var.ui.cmbMuniprop,var.ui.cmbTipoprop,
                            var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop,var.ui.txtPrecioAlquilerprop,
                            var.ui.txtPrecioVentaprop,
                            var.ui.txtCpprop,var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,var.ui.chkVentaprop,var.ui.chkInterprop,
                            var.ui.chkAlquilprop,var.ui.rbtVentaprop,var.ui.txtNomeprop,var.ui.txtMovilprop]
        for i, dato in enumerate(objetosPanelProp):
            if i in (4,5,6):
                pass
            elif i in (7,8):
                dato.setValue(0)
            elif i == 13:
                dato.setPlainText("")
            elif i == 14:
                dato.setChecked(True)
            elif i in (15,16,17,18,19):
                dato.setChecked(False)
            else:
                dato.setText("")

        eventos.Eventos.cargarProv()
        var.ui.btnBuscaTipoProp.setChecked(False)
        propiedades.Propiedades.cargarTablaPropiedades()


    @staticmethod
    def abrirTipoprop():
        try:
            var.dlggestion.show()
        except Exception as e:
            print("error en abrir tipo prop: ", e)

    @staticmethod
    def exportCSVprop():
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha)+'_DatosPropiedades.csv'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a CSV", file, '.csv')
            if fichero:
                registros = conexion.Conexion.cargarAllPropiedadesBD()
                with open(fichero, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Dirección","Provincia","Municipio","Tipo","Nº habitaciones","Nº Baños","Superficie","Precio Alquiler","Precio Compra","Código postal", "Observaciones","Operación","Estado","Propietario","Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error al exportar los datos en formato CSV.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def exportJSONprop():
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha)+'_DatosPropiedades.json'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a JSON", file, '.json')
            if fichero:
                keys = ["Codigo","Alta","Baja","Dirección","Provincia","Municipio","Tipo","Nº habitaciones","Nº Baños","Superficie","Precio Alquiler","Precio Compra","Código postal", "Observaciones","Operación","Estado","Propietario","Móvil"]
                registros = conexion.Conexion.cargarAllPropiedadesBD()
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonFile:
                    json.dump(lista_propiedades, jsonFile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError("Error","Se ha producido un error al exportar los datos en formato CSV.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def abrir_about():
        try:
            var.dlgabout.show()
        except Exception as e:
            print("error en abrir about: ", e)

