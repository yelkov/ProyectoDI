import math
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
import os, shutil
from PyQt6 import QtSql, QtWidgets, QtCore
import sqlite3

import var

class Informes:
    @staticmethod
    def reportClientes():
        """

        Método que genera un informe en formato pdf de todos los clientes almacenados en la base de datos usando la biblioteca reportlab

        """
        ymax = 660
        ymin = 90
        ystep = 20
        xmin = 60

        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Clientes"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)

            items = ['DNI','APELLIDOS','NOMBRE','MOVIL','PROVINCIA','MUNICIPIO']
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,680,str(items[0]))
            var.report.drawString(100,680,str(items[1]))
            var.report.drawString(200, 680, str(items[2]))
            var.report.drawString(285, 680, str(items[3]))
            var.report.drawString(360, 680, str(items[4]))
            var.report.drawString(450, 680, str(items[5]))
            var.report.line(40, 675, 540, 675)
            query = QtSql.QSqlQuery()
            query.exec("SELECT count(*) FROM clientes")
            if query.next():
                numRegistros = query.value(0)
                paginas = Informes.getMaxElementosPpag(ymax, ymin, ystep,numRegistros)
            Informes.topInforme(titulo, None)
            Informes.footInforme(titulo, paginas)

            query.prepare("SELECT dnicli, apelcli, nomecli, movilcli, provcli, municli from clientes order by apelcli")
            if query.exec():
                x = xmin
                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.setFont('Helvetica-Oblique',size=8)
                        var.report.drawString(450,80,"Página siguiente...")
                        var.report.showPage() #crea una pagina nueva
                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo, None)
                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 680, str(items[0]))
                        var.report.drawString(100, 680, str(items[1]))
                        var.report.drawString(200, 680, str(items[2]))
                        var.report.drawString(285, 680, str(items[3]))
                        var.report.drawString(360, 680, str(items[4]))
                        var.report.drawString(450, 680, str(items[5]))
                        var.report.line(40, 675, 540, 675)
                        x = xmin
                        y = ymax


                    var.report.setFont('Helvetica',size=9)
                    dni = '***' + str(query.value(0)[3:6])  + '***'
                    var.report.drawCentredString(x + 5, y, str(dni))
                    var.report.drawString(x + 40, y, str(query.value(1)))
                    var.report.drawString(x + 140, y, str(query.value(2)))
                    var.report.drawString(x + 215, y, str(query.value(3)))
                    var.report.drawString(x + 300, y, str(query.value(4)))
                    var.report.drawString(x + 380, y, str(query.value(5)))
                    y -= ystep
            else:
                print(query.lastError().text())


            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def reportPropiedades(municipio):
        """

        :param municipio: el municipio del que queremos extraer las propiedades
        :type municipio: str

        Método que genera un informe en pdf de las propiedades almacenadas en la base de datos para un municipio que indique el usuario usando la biblioteca reportlab
        """
        try:
            ymax = 655
            ymin = 90
            ystep = 20
            xmin = 60

            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Propiedades"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfprop = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfprop)
            var.report = canvas.Canvas(pdf_path)

            items = ['COD','DIRECCION','TIPO PROP.','OPERACION','PRECIO ALQ.','PRECIO VENTA']
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,680,str(items[0]))
            var.report.drawString(100,680,str(items[1]))
            var.report.drawString(210, 680, str(items[2]))
            var.report.drawString(295, 680, str(items[3]))
            var.report.drawString(380, 680, str(items[4]))
            var.report.drawString(460, 680, str(items[5]))
            var.report.line(40, 675, 540, 675)
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) FROM propiedades WHERE municipio = :municipio")
            query.bindValue(":municipio", municipio)
            if query.exec():
                if query.next():
                    numRegistros = query.value(0)
                    paginas = Informes.getMaxElementosPpag(ymax, ymin, ystep,numRegistros)
            Informes.topInforme(titulo, municipio)
            Informes.footInforme(titulo, paginas)


            query.prepare("SELECT codigo, direccion,tipo_propiedad, tipo_operacion, precio_alquiler, precio_venta from propiedades where municipio = :municipio order by municipio")
            query.bindValue(":municipio", str(municipio))
            if query.exec():
                x = xmin
                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.setFont('Helvetica-Oblique',size=8)
                        var.report.drawString(450,80,"Página siguiente...")
                        var.report.showPage() #crea una pagina nueva
                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo, municipio)
                        items = ['COD','DIRECCION','TIPO PROP.','OPERACION','PRECIO ALQ.','PRECIO VENTA']
                        var.report.setFont('Helvetica-Bold',size=10)
                        var.report.drawString(55,680,str(items[0]))
                        var.report.drawString(100,680,str(items[1]))
                        var.report.drawString(210, 680, str(items[2]))
                        var.report.drawString(295, 680, str(items[3]))
                        var.report.drawString(380, 680, str(items[4]))
                        var.report.drawString(460, 680, str(items[5]))
                        var.report.line(40, 675, 540, 675)
                        x = xmin
                        y = ymax


                    var.report.setFont('Helvetica',size=9)
                    var.report.drawString(x + 5, y, str(query.value(0)))
                    var.report.drawString(x + 40, y, str(query.value(1)))
                    var.report.drawString(x + 150, y, str(query.value(2)))
                    operacion = query.value(3).replace("[","").replace("]","").replace("'","")
                    var.report.drawString(x + 240, y, str(operacion))
                    alquiler = "-" if not str(query.value(4)) else str(query.value(4))
                    var.report.drawRightString(x + 380, y, alquiler+" €")
                    compra = "-" if not str(query.value(5)) else str(query.value(5))
                    var.report.drawRightString(x + 470, y, compra+" €")
                    y -= ystep
            else:
                print(query.lastError().text())


            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfprop):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def reportFactura(idFactura):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            ano = datetime.now().year
            titulo = "FACTURA FAC"+str(ano)+"/"+idFactura
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdffac = fecha + "_factura_"+str(ano)+"-"+idFactura+".pdf"
            pdf_path = os.path.join(rootPath, nomepdffac)
            var.report = canvas.Canvas(pdf_path)

            items = ['ID VENTA', 'COD. PROP.', 'DIRECCIÓN', 'MUNICIPIO', 'TIPO', 'PRECIO VENTA']
            var.report.line(40, 633, 540, 633)
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(45, 620, str(items[0]))
            var.report.drawString(100, 620, str(items[1]))
            var.report.drawString(200, 620, str(items[2]))
            var.report.drawString(310, 620, str(items[3]))
            var.report.drawString(410, 620, str(items[4]))
            var.report.drawString(460, 620, str(items[5]))
            var.report.line(40, 615, 540, 615)
            datos_factura = var.claseConexion.datosOneFactura(idFactura)

            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 690, "ID factura: " + str(datos_factura[0]))
            var.report.drawString(55, 670, "Fecha: " + str(datos_factura[1]))

            dni_cliente = datos_factura[2]
            datos_cliente = var.claseConexion.datosOneCliente(dni_cliente)
            var.report.drawCentredString(300, 690, "Cliente: " + str(datos_cliente[3]) + " " + str(datos_cliente[2]))
            var.report.drawCentredString(300,670,"Dirección: " + str(datos_cliente[6]))
            var.report.drawRightString(540,690,"DNI: " + str(dni_cliente))
            var.report.drawRightString(540,670,"Localidad: " + str(datos_cliente[8]))

            listado_ventas = var.claseConexion.listadoVentas(idFactura)
            y = 600
            for venta in listado_ventas:
                var.report.drawCentredString(65,y,str(venta[0]))
                var.report.drawCentredString(120,y,str(venta[1]))
                var.report.drawCentredString(230,y,str(venta[2]))
                var.report.drawCentredString(335,y,str(venta[3]))
                var.report.drawCentredString(420,y,str(venta[4]))
                precio_alquiler = f"{venta[5]:,.1f} €"
                var.report.drawCentredString(510,y,precio_alquiler)
                y -= 20


            var.report.line(40,130,540,130)
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(350,110, "Subtotal: ")
            var.report.drawString(350,90, "IVA (10%): ")
            var.report.setFont('Helvetica-Bold', size=12)
            var.report.drawString(350,60, "Total: ")
            var.report.drawRightString(540,60, str(var.ui.lblTotal.text()))
            var.report.setFont('Helvetica', size=10)
            var.report.drawRightString(540,110, str(var.ui.lblSubtotal.text()))
            var.report.drawRightString(540,90, str(var.ui.lblIva.text()))


            Informes.topInforme(titulo, None)
            Informes.footInforme(titulo, 1)





            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdffac):
                    os.startfile(pdf_path)

        except Exception as e:
            print("Error al generar informe de facturas", str(e))

    @staticmethod
    def getMaxElementosPpag(ymax, ymin, ystep, numRegistros):
        """

        :param ymax: altura máxima donde comenzará a mostrarse el elemento
        :type ymax: int
        :param ymin: altura mínima hasta donde se mostrarán elementos en el informe
        :type ymin: int
        :param ystep: diferencia de altura entre distintos elementos
        :type ystep: int
        :param numRegistros: cantidad de registros que hay de un tipo en la base de datos
        :type numRegistros: int
        :return: el número de elementos que se van a mostrar por página
        :rtype: int

        Método para calcular el número de elementos que se van a mostrar como máximo en una página teniendo en cuenta la altura total a mostrar y la cantidad de elementos que caben en ese espacio

        """
        numPpagina = math.ceil(numRegistros/(ymax - ymin) / ystep)
        return numPpagina

    def topInforme(titulo, municipio):
        """

        :param titulo: titulo del informe
        :type titulo: str
        :param municipio: nombre del municipio sobre el que vamos a crear el informe
        :type municipio: str

        Método para crear una cabecera genérica para todos los informes en pdf. Si se le pasa el parámetro municipio, se añade a la cabecera del informe

        """
        try:
            if municipio:
                municipio = municipio.upper()
            ruta_logo = '.\\img\\icono.png'
            logo = Image.open(ruta_logo)

            ruta_letras = '.\\img\\nombre-02.png'
            letras = Image.open(ruta_letras)
            # drawing = svg2rlg(svg_file)  PARA FICHERO SVG
            # renderP.drawToFile(drawing, "temp_image.png", fmt="PNG")
            # logo = QPixmap("temp_image.png")

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image) and isinstance(letras, Image.Image):
                var.report.drawImage(ruta_letras, 240, 790, width=120, height=60)
                var.report.line(40, 800, 540, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 782, 'InmoTeis S.L.')
                if municipio:
                    var.report.drawCentredString(300, 725, titulo)
                    var.report.drawCentredString(300, 705, municipio)
                    var.report.line(40, 695, 540, 695)
                else:
                    var.report.drawCentredString(300, 715, titulo)
                    var.report.line(40, 710, 540, 710)



                # Dibuja la imagen del logo en el informe
                var.report.drawImage(ruta_logo, 507, 758, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawCentredString(300, 780, 'CIF: A12345678')
                var.report.drawCentredString(300, 765, 'www.inmoteis.es')
                var.report.drawString(55, 767, 'Avda. Galicia - 101')
                var.report.drawString(55, 752, 'Vigo - 36216 - España')
                var.report.drawString(380, 780, 'Teléfono: 986 132 456')
                var.report.drawString(380, 765, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo} o en {ruta_letras}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo, paginas):
        """
        :param titulo: titulo del informe
        :type titulo: str
        :param paginas: número de páginas que va a contener el informe
        :type paginas: int

        Método para generar un pie de informes genérico en pdf, indicando la página actual del informe respecto del total de páginas que contenga este

        """
        try:
            total_pages = 0
            var.report.line(40, 50, 540, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawCentredString(300, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber() + '/' + str(paginas)))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)




if __name__ == '__main__':
    Informes.reportClientes()