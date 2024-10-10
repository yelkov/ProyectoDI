from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import eventos
import var

class Clientes:
    @staticmethod
    def altaCliente():
        try:
            nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(),var.ui.cmbMunicli.currentText()]

            if Clientes.checkDatosVaciosCli(nuevoCli) and conexion.Conexion.altaCliente(nuevoCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Cliente Alta en Base de Datos")

                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

            elif not Clientes.checkDatosVaciosCli(nuevoCli):
                QtWidgets.QMessageBox.critical(None, 'Error', 'Algunos campos deben ser cubiertos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'Error al grabar cliente.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        except Exception as e:
            print("error alta cliente", e)

    @staticmethod
    def checkDniCli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('border: 1px solid #41AD48; border-radius: 5px; background-color: rgb(254, 255, 210)')
                Clientes.cargarTickcli()
            else:
                var.ui.txtDnicli.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; background-color: rgb(254, 255, 210)')
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
                Clientes.cargarCruzcli()

        except Exception as e:
            print("Error check clientes" + e)

    @staticmethod
    def cargarTickcli():
        pixmap = eventos.Eventos.cargarTick()
        var.ui.lblTickcli.setPixmap(pixmap)
        var.ui.lblTickcli.setScaledContents(True)

    @staticmethod
    def cargarCruzcli():
        pixmap = eventos.Eventos.cargarCruz()
        var.ui.lblTickcli.setPixmap(pixmap)
        var.ui.lblTickcli.setScaledContents(True)

    @staticmethod
    def checkEmailCli(mail):
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)


    @staticmethod
    def checkDatosVaciosCli(datosClientes):
        datos = datosClientes[:]
        emailCli = datos.pop(4)
        for dato in datos:
            if dato == "" or dato == None:
                return False
        return True

    @staticmethod
    def cargaTablaClientes():
        try:
            listado = conexion.Conexion.listadoClientes()
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[2])) #apellido
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[3])) #nombre
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem("  " + registro[5] + "  ")) #movil
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[7])) #provincia
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[8])) #municipio
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[9])) #baja
                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1


        except Exception as e:
            print("Error cargaClientes", e)
