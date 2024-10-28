import var


class Propiedades():

    @staticmethod
    def altaTipoPropiedad():
        tipo = var.dlggestion.txtTipoprop.text().title()
        print(str(tipo))

    @staticmethod
    def altaPropiedad():
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.txtCpprop.text(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioVentaprop.text(), var.ui.txtPrecioAlquilerprop.text(),var.ui.areatxtDescriprop.toPlainText(),
                         var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]
            print(propiedad)
        except Exception as e:
            print(str(e))