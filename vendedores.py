import eventos
import var


class Vendedores():

    @staticmethod
    def checkDniVen(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVen.setText(str(dni))
            check = eventos.Eventos.isDniValido(dni)
            if check:
                var.ui.txtDniVen.setStyleSheet('border: 1px solid #41AD48; border-radius: 5px;')
            else:
                var.ui.txtDniVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtDniVen.setText(None)
                var.ui.txtDniVen.setPlaceholderText("dni no válido")
                var.ui.txtDniVen.setFocus()

        except Exception as e:
            print("Error check clientes" + e)

    @staticmethod
    def checkMovilVen(movil):
        try:
            if eventos.Eventos.isMovilValido(movil):
                var.ui.txtMovilVen.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilVen.setText(None)
                var.ui.txtMovilVen.setPlaceholderText("móvil no válido")
                var.ui.txtMovilVen.setFocus()
        except Exception as e:
            print("error check movil", e)

    @staticmethod
    def checkEmailVen(mail):
        try:
            if eventos.Eventos.isMailValido(mail):
                var.ui.txtEmailVen.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailVen.setText(mail.lower())

            else:
                var.ui.txtEmailVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtEmailVen.setText(None)
                var.ui.txtEmailVen.setPlaceholderText("correo no válido")
                var.ui.txtEmailVen.setFocus()

        except Exception as error:
            print("error check email", error)

    @staticmethod
    def altaVendedor():
        print("Hola")