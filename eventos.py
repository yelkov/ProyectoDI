import os
import sys
import time
import re
from datetime import datetime

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHeaderView

import locale

import clientes
import conexion
import conexionserver
import eventos
import var
from PyQt6 import QtWidgets, QtGui
import zipfile
import shutil


#Establecer configuracion regional

locale.setlocale(locale.LC_TIME,'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY,'es_ES.UTF-8')

class Eventos():
    @staticmethod
    def mensajeSalir():
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/icono.svg'))
        mbox.setText("¿Desea salir?")

        mbox.setWindowTitle('Salir')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def cargarProv():
        var.ui.cmbProvcli.clear()
        listado = conexion.Conexion.listaProv()
        #listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbProvcli.addItems(listado)
        var.ui.cmbProvprop.addItems(listado)

    @staticmethod
    def cargaMunicli(provincia):
        var.ui.cmbMunicli.clear()
        listado = conexion.Conexion.listaMunicipio(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicli.addItems(listado)

    @staticmethod
    def cargaMuniprop(provincia):
        var.ui.cmbMuniprop.clear()
        listado = conexion.Conexion.listaMunicipio(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMuniprop.addItems(listado)

    @staticmethod
    def validarDNI(dni):
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
    def validarMovil(movil):
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
    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
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

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Copia de seguridad')
                mbox.setText("Copia de seguridad creada.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
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
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Copia de seguridad')
                mbox.setText("Copia de seguridad restaurada.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                conexion.Conexion.db_conexion()
                eventos.Eventos.cargarProv()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        objetosPanelCli = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                   var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,var.ui.cmbMunicli,var.ui.txtBajacli]
        for i, dato in enumerate(objetosPanelCli):
            if i in (7,8):
                pass
            else:
                dato.setText("")

        eventos.Eventos.cargarProv()

    @staticmethod
    def abrirTipoprop():
        try:
            var.dlggestion.show()
        except Exception as e:
            print("error en abrir tipo prop: ", e)