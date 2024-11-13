import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtGui, QtCore

import eventos
import var
from eventos import Eventos


class Conexion:

    '''
    @staticmethod
    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    '''

    @staticmethod
    def db_conexion():
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            eventos.Eventos.crearMensajeError("Error",'El archivo de la base de datos no existe.')
            return False

        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                eventos.Eventos.crearMensajeError("Error","Base de datos vacía o no válida.")
                return False

            else:
                eventos.Eventos.crearMensajeInfo("Aviso","Conexión a la Base de Datos realizada")
                return True

        else:
            eventos.Eventos.crearMensajeError("Error","No se pudo abrir la base de datos.")
            return False

    '''
    GESTION DE CLIENTES
    '''

    @staticmethod
    def listaProv():
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMunicipio(provincia):
        try:
            listamunicipio = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipio.append(query.value(1))
            return listamunicipio
        except Exception as e:
            print("error al cargar municipios")

    @staticmethod
    def altaCliente(nuevocli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into clientes (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) values (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta cliente", e)

    @staticmethod
    def listadoClientes():
        try:
            listado = []
            historico = var.ui.chkHistoriacli.isChecked()
            if historico:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is null ORDER BY apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar clientes")


    @staticmethod
    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UN cliente en la tabla.", e)

    @staticmethod
    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UNA propiedad en conexion.", e)


    @staticmethod
    def modifCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1: #verificamos que solo nos devuelve un resultado, la fila para el dni que buscamos

                    query.prepare("UPDATE clientes set altacli= :altacli, apelcli = :apelcli, nomecli= :nomecli, emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli=:provcli, municli=:municli, bajacli = :bajacli WHERE dnicli = :dni")
                    query.bindValue(":dni", str(registro[0]))
                    query.bindValue(":altacli", str(registro[1]))
                    query.bindValue(":apelcli", str(registro[2]))
                    query.bindValue(":nomecli", str(registro[3]))
                    query.bindValue(":emailcli", str(registro[4]))
                    query.bindValue(":movilcli", str(registro[5]))
                    query.bindValue(":dircli", str(registro[6]))
                    query.bindValue(":provcli", str(registro[7]))
                    query.bindValue(":municli", str(registro[8]))
                    if registro[9] == "":
                        query.bindValue(":bajacli",QtCore.QVariant()) #QVariant añade un null a la BD
                    else:
                        query.bindValue(":bajacli", str(registro[9]))

                    if query.exec():
                        return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error al modificar un cliente en conexion.", e)


    @staticmethod
    def bajaCliente(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT COUNT(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:
                    query.prepare("UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dni")
                    query.bindValue(":bajacli", datetime.now().strftime("%d/%m/%Y"))
                    query.bindValue(":dni", str(dni))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error en la conexión al dar de baja cliente", e)

    '''
    GESTION DE PROPIEDADES
    '''
    @staticmethod
    def cargarTipoprop():
        query = QtSql.QSqlQuery()
        query.prepare("SELECT tipo from tipopropiedad ")
        if query.exec():
            registro = []
            while query.next():
                registro.append(str(query.value(0)))
            return registro

    @staticmethod
    def altaTipoprop(tipo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into tipopropiedad (tipo) values (:tipo) ")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                registro = Conexion.cargarTipoprop()
                return registro
            else:
                return registro
        except Exception as e:
            print("Error en conexion al dar de alta tipo propiedad", e)

    @staticmethod
    def bajaTipoprop(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE from tipopropiedad where tipo = :tipo ")
            query.bindValue(":tipo", str(tipo))
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as e:
            print("Error en conexion al dar de baja tipo propiedad", e)

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into propiedades (alta,direccion,provincia,municipio,tipo_propiedad,num_habitaciones,num_banos,superficie,precio_alquiler,precio_venta,codigo_postal,descripcion,tipo_operacion,estado,nombre_propietario,movil) values (:alta,:direccion,:provincia,:municipio,:tipo_propiedad,:num_habitaciones,:num_banos,:superficie,:precio_alquiler,:precio_venta,:codigo_postal,:descripcion,:tipo_operacion,:estado,:nombre_propietario,:movil) ")
            query.bindValue(":alta",str(propiedad[0]))
            query.bindValue(":direccion",str(propiedad[1]))
            query.bindValue(":provincia",str(propiedad[2]))
            query.bindValue(":municipio",str(propiedad[3]))
            query.bindValue(":tipo_propiedad",str(propiedad[4]))
            query.bindValue(":num_habitaciones",str(propiedad[5]))
            query.bindValue(":num_banos",str(propiedad[6]))
            query.bindValue(":superficie",str(propiedad[7]))
            query.bindValue(":precio_alquiler",str(propiedad[8]))
            query.bindValue(":precio_venta",str(propiedad[9]))
            query.bindValue(":codigo_postal",str(propiedad[10]))
            query.bindValue(":descripcion",str(propiedad[11]))
            query.bindValue(":tipo_operacion",str(propiedad[12]))
            query.bindValue(":estado",str(propiedad[13]))
            query.bindValue(":nombre_propietario",str(propiedad[14]))
            query.bindValue(":movil",str(propiedad[15]))

            if query.exec():
                return True
            else:
                return False


        except Exception as e:
            print("Error al dar de alta propiedad en conexion",e)

    @staticmethod
    def modifProp(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1: #verificamos que solo nos devuelve un resultado, la fila para el codigo que buscamos

                    query.prepare("UPDATE propiedades set alta = :alta, baja = :baja, direccion = :direccion, municipio = :municipio, provincia = :provincia, tipo_propiedad = :tipo_propiedad, num_habitaciones=:num_habitaciones, num_banos = :num_banos, superficie = :superficie, precio_alquiler = :precio_alquiler, precio_venta = :precio_venta, codigo_postal = :codigo_postal, descripcion = :descripcion, tipo_operacion = :tipo_operacion, estado=:estado, nombre_propietario =:nombre_propietario, movil =:movil WHERE codigo = :codigo")
                    query.bindValue(":codigo",str(propiedad[0]))
                    query.bindValue(":alta",str(propiedad[1]))
                    query.bindValue(":direccion",str(propiedad[3]))
                    query.bindValue(":provincia",str(propiedad[4]))
                    query.bindValue(":municipio",str(propiedad[5]))
                    query.bindValue(":tipo_propiedad",str(propiedad[6]))
                    query.bindValue(":num_habitaciones",str(propiedad[7]))
                    query.bindValue(":num_banos",str(propiedad[8]))
                    query.bindValue(":superficie",str(propiedad[9]))
                    query.bindValue(":precio_alquiler",str(propiedad[10]))
                    query.bindValue(":precio_venta",str(propiedad[11]))
                    query.bindValue(":codigo_postal",str(propiedad[12]))
                    query.bindValue(":descripcion",str(propiedad[13]))
                    query.bindValue(":tipo_operacion",str(propiedad[14]))
                    query.bindValue(":estado",str(propiedad[15]))
                    query.bindValue(":nombre_propietario",str(propiedad[16]))
                    query.bindValue(":movil",str(propiedad[17]))
                    if propiedad[2] == "":
                        query.bindValue(":baja",QtCore.QVariant()) #QVariant añade un null a la BD
                    else:
                        query.bindValue(":baja",str(propiedad[2]))

                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al modificar propiedad en conexión.",e)

    @staticmethod
    def bajaProp(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1: #verificamos que solo nos devuelve un resultado a consulta, por tanto la propiedad existe.
                    query.prepare("update propiedades set baja =:baja, estado =:estado where codigo = :codigo ")
                    query.bindValue(":codigo",str(propiedad[0]))
                    query.bindValue(":baja",str(propiedad[2])) #dejamos el segundo espacio del array para fecha de alta, y comprobar mas tarde que no sea posterior a fecha de baja
                    query.bindValue(":estado",str(propiedad[3]))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al dar de baja propiedad en conexión.",e)

    @staticmethod
    def listadoPropiedades():
        try:
            listado = []
            historico = var.ui.chkHistoriaprop.isChecked()
            municipio = var.ui.cmbMuniprop.currentText()
            filtrado = var.ui.btnBuscaTipoProp.isChecked()
            tipoSeleccionado = var.ui.cmbTipoprop.currentText()

            base_query = "SELECT * FROM propiedades"
            condiciones = []
            parametros_bind = {}

            if not historico:
                condiciones.append("baja is NULL")
            if filtrado:
                condiciones.append("tipo_propiedad = :tipo_propiedad")
                parametros_bind[":tipo_propiedad"] = tipoSeleccionado
                condiciones.append("municipio = :municipio")
                parametros_bind[":municipio"] = municipio
            elif not historico:
                condiciones.append("estado = 'Disponible'")

            if condiciones:
                base_query += " WHERE " + " AND ".join(condiciones)
            base_query += " ORDER BY municipio ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)
            for clave, valor in parametros_bind.items():
                query.bindValue(clave, valor)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar propiedades en listadoPropiedades", e)