import sys
import time
import re

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHeaderView

import conexion
import var
from PyQt6 import QtWidgets, QtGui

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
        var.ui.cmbProvcli.addItems(listado)

    @staticmethod
    def cargaMunicli(provincia):
        var.ui.cmbMunicli.clear()
        listado = conexion.Conexion.listaMunicipio(provincia)
        var.ui.cmbMunicli.addItems(listado)

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
    def cargarTick():
        pixmap = QPixmap("img/tick.svg")
        return pixmap

    @staticmethod
    def cargarCruz():
        pixmap = QPixmap("img/cruz.svg")
        return pixmap

    @staticmethod
    def abrirCalendar(op):
        try:
            var.panel = op
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == var.ui.panPrincipal.currentIndex():
                var.ui.txtAltacli.setText(str(data))
            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail):
            return True
        else:
            return False

    @staticmethod
    def resizeTablaClientes():
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i not in (2,5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)