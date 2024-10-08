from PyQt6 import QtWidgets

import conexion
import eventos
import var

class Clientes:
    @staticmethod
    def altaCliente():
        nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(),var.ui.cmbMunicli.currentText()]
        conexion.Conexion.altaCliente(nuevoCli)

    @staticmethod
    def checkDniCli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('border: 1px solid #41AD48; border-radius: 5px;')
                Clientes.cargarTickcli()
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB; border: 1px solid #de6767; border-radius: 5px;')
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
                var.ui.lblTickcli.clear()

        except Exception as e:
            print("Error check clientes" + e)

    @staticmethod
    def cargarTickcli():
        pixmap = eventos.Eventos.cargarTick()
        var.ui.lblTickcli.setPixmap(pixmap)
        var.ui.lblTickcli.setScaledContents(True)

    @staticmethod
    def checkEmailCli(mail):
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(254, 255, 210);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)