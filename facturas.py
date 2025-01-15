import conexion
import eventos
import var

class Facturas:

    @staticmethod
    def altaFactura():
        try:
            nuevaFactura = [var.ui.txtFechaFactura.text(),var.ui.txtdniclifac.text()]
            if var.ui.txtdniclifac.text() == "" or var.ui.txtdniclifac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","Recuerda seleccionar un cliente antes de grabar una factura")
            if var.ui.txtFechaFactura.text() == "" or var.ui.txtFechaFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","No es posible grabar una factura sin seleccionar una fecha")
            elif conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.crearMensajeInfo("Factura grabada","Se ha grabado una nueva factura")
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido grabar factura")
        except Exception as e:
            print("factura",e)