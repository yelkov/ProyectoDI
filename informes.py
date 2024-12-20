from dataclasses import dataclass
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
import os, shutil

import var

class Informes:
    @staticmethod
    def reportClientes():
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Clientes"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['DNI','APELLIDOS','NOMBRE','MOVIL','PROVINCIA','MUNICIPIO']
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,700,str(items[0]))
            var.report.drawString(100,700,str(items[1]))
            var.report.drawString(190, 700, str(items[2]))
            var.report.drawString(285, 700, str(items[3]))
            var.report.drawString(360, 700, str(items[4]))
            var.report.drawString(450, 700, str(items[5]))
            var.report.line(50, 695, 525, 695)

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    def topInforme(titulo):
        try:
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
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                var.report.drawString(230, 720, titulo)
                var.report.line(50, 715, 525, 715)


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

    def footInforme(titulo):
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)

if __name__ == '__main__':
    Informes.reportClientes()