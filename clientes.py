from PyQt6 import QtWidgets

import eventos
import var

class Clientes:
    def altaCliente(self):
        dni = var.ui.txtDnicli.text()
        print(dni)

    def checkDni(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color:#BEEEBA;')
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB; border: 2px solid #de6767; border-radius : 5px')  # y si no un aspa en color rojo
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("Error check clientes" + e)