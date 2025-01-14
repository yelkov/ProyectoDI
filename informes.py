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
            nomepdfcli = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
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
                        items = ['CODIGO','DIRECCION','TIPO PROP','OPERACION','PRECIO ALQUILER','PRECIO COMPRA']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 700, str(items[0]))
                        var.report.drawString(100, 700, str(items[1]))
                        var.report.drawString(200, 700, str(items[2]))
                        var.report.drawString(285, 700, str(items[3]))
                        var.report.drawString(360, 700, str(items[4]))
                        var.report.drawString(450, 700, str(items[5]))
                        var.report.line(40, 695, 540, 695)
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
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def getMaxElementosPpag(ymax, ymin, ystep, numRegistros):
        numPpagina = math.ceil(numRegistros/(ymax - ymin) / ystep)
        return numPpagina

    def topInforme(titulo, municipio):
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
                var.report.drawImage(ruta_letras, 230, 790, width=120, height=60)
                var.report.line(40, 800, 540, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                if municipio:
                    var.report.drawString(230, 725, titulo)
                    var.report.drawCentredString(300, 705, municipio)
                else:
                    var.report.drawString(230, 715, titulo)
                var.report.line(40, 695, 540, 695)


                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 750, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(230, 772, 'CIF: A12345678')
                var.report.drawString(55, 772, 'Avda. Galicia - 101')
                var.report.drawString(55, 757, 'Vigo - 36216 - España')
                var.report.drawString(360, 772, 'Teléfono: 986 132 456')
                var.report.drawString(360, 757, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo} o en {ruta_letras}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo, paginas):
        try:
            total_pages = 0
            var.report.line(40, 50, 540, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber() + '/' + str(paginas)))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)




if __name__ == '__main__':
    Informes.reportClientes()