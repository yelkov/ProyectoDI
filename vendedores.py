import eventos
import var
from PyQt6 import QtWidgets, QtCore
from datetime import datetime


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
        try:
            nuevoVendedor = [var.ui.txtDniVen.text(),var.ui.txtNomVen.text(),var.ui.txtAltaVen.text(),var.ui.txtMovilVen.text(),var.ui.txtEmailVen.text(),var.ui.cmbDeleVen.currentText()]

            if Vendedores.isVendedorPresent(nuevoVendedor):
                eventos.Eventos.crearMensajeError("Error","El DNI del vendedor introducido ya existe")
            elif Vendedores.hasCamposObligatorios(nuevoVendedor) and not Vendedores.isVendedorPresent(nuevoVendedor) and var.claseConexion.altaVendedor(nuevoVendedor):
                eventos.Eventos.crearMensajeInfo("Aviso","Vendedor dado de alta en Base de Datos")
                Vendedores.cargaTablaVendedores()
            elif not Vendedores.hasCamposObligatorios(nuevoVendedor):
                eventos.Eventos.crearMensajeError("Error","Algunos campos deben ser cubiertos.")

            else:
                eventos.Eventos.crearMensajeError("Error","Error al grabar vendedor.")

        except Exception as e:
            print("error alta vendedor", e)

    @staticmethod
    def hasCamposObligatorios(nuevoVendedor):
        datos = nuevoVendedor[:]
        fecha_alta = datos.pop(2)
        mail = datos.pop(3)
        for dato in datos:
            if dato == "" or dato == None:
                return False
        return True

    @staticmethod
    def isVendedorPresent(nuevoVendedor):
        registro = var.claseConexion.datosOneVendedor(nuevoVendedor[0],"dniVendedor")
        if registro != []:
            return True
        else:
            return False

    @staticmethod
    def cargaTablaVendedores():
        try:
            listado = var.claseConexion.listadoVendedores()

            var.ui.tablaVendedores.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #id
                var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2])) #nombre
                var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(" " + registro[5] + " ")) #movil
                var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[7])) #movil
                var.ui.tablaVendedores.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[4])) #baja
                var.ui.tablaVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1


        except Exception as e:
            print("Error cargaVendedor en cargaTablaVendedores", e)

    @staticmethod
    def bajaVendedor():
        try:
            dni = var.ui.txtDniVen.text()
            if var.claseConexion.bajaVendedor(dni):
                eventos.Eventos.crearMensajeInfo("Aviso","El vendedor fue dado de baja a fecha de: " + datetime.now().strftime("%d/%m/%Y"))
                Vendedores.cargaTablaVendedores()
            else:
                eventos.Eventos.crearMensajeError("Error","El vendedor no existe o ya ha sido dado de baja.")

        except Exception as e:
            print("Error al dar de baja vendedor", e)

    @staticmethod
    def cargaOneVendedor():
        try:
            fila = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOneVendedor(str(datos[0]))
            listado = [var.ui.lblIdVen,var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                       var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
            for i in range(len(listado)):
                if i == 7:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            var.ui.txtidvenfac.setText(registro[0])
            var.ui.txtidvenalq.setText(registro[0])

        except Exception as e:
            print("Error cargaVendedores en cargaOneVendedor", e)

    @staticmethod
    def historicoVendedores():
        try:
            Vendedores.cargaTablaVendedores()
        except Exception as e:
            print("checkbox historico no funciona correctamente en vendedores", e)

    @staticmethod
    def modifVendedor():
        try:
            modifVendedor = [var.ui.lblIdVen.text(), var.ui.txtNomVen.text(),var.ui.txtAltaVen.text(),var.ui.txtMovilVen.text(),var.ui.txtEmailVen.text(),var.ui.cmbDeleVen.currentText(),var.ui.txtBajaVen.text()]
            if  modifVendedor[6] != "" and not Vendedores.esFechasValidas(modifVendedor):
                eventos.Eventos.crearMensajeError("Aviso","La fecha de baja no puede anterior a la de alta.")
            elif Vendedores.hasCamposObligatorios(modifVendedor[:-1]) and var.claseConexion.modifVendedor(modifVendedor):
                eventos.Eventos.crearMensajeInfo('Aviso',"El vendedor fue modificado correctamente en la base de datos")
                Vendedores.cargaTablaVendedores()
            elif not Vendedores.hasCamposObligatorios(modifVendedor):
                eventos.Eventos.crearMensajeError("Error","El vendedor no está guardado en la base de datos o bien hay campos vacíos.")
            else:
                eventos.Eventos.crearMensajeError("Error","Error al modificar vendedor.")

        except Exception as e:
            print("Error en modifCliente", e)


    @staticmethod
    def esFechasValidas(datosVendedores):
        import datetime

        datos = datosVendedores[:]
        alta = datos[2]
        baja = datos[6]

        fecha_alta = datetime.datetime.strptime(alta,"%d/%m/%Y")
        fecha_baja = datetime.datetime.strptime(baja,"%d/%m/%Y")

        return fecha_alta < fecha_baja #si fecha de alta es posterior a fecha de baja devuelve false


    @staticmethod
    def buscaOneVendedor():
        try:
            movil = var.ui.txtMovilVen.text()
            registro = var.claseConexion.datosOneVendedor(movil,"movilVendedor")
            if registro:
                listado = [var.ui.lblIdVen,var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                           var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
                for i in range(len(listado)):
                    if i == 7:
                        listado[i].setCurrentText(registro[i])
                    else:
                        listado[i].setText(registro[i])
            else:
                eventos.Eventos.crearMensajeError("Error","El vendedor con móvil "+ movil + " no existe en la base de datos")
        except Exception as e:
            print("Error cargaVendedores en cargaOneVendedor", e)