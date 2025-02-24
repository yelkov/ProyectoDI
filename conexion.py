import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtGui, QtCore

import var



class Conexion:

    @staticmethod
    def db_conexion():
        """

        :return: conexion con la base de datos.
        :rtype: bool

        Método para establecer conexión con la base de datos
        Si éxito devuelve True, en caso contrario devuelve False.

        """
        import eventos
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
        """

        :return: lista de provincias
        :rtype: list

        Método que devuelve la lista de provincias

        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMunicipio(provincia):
        """

        :param provincia: nombre de la provincia
        :type provincia: str
        :return: lista de municipios de una provincia
        :rtype: list

        Método que devuelve todos los municipios de una provincia

        """
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
        """

        :param nuevocli: lista de datos del cliente
        :type nuevocli: list
        :return: éxito en la creación de un cliente
        :rtype: bool

        Método que inserta datos cliente en la base de datos

        """
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
        """

        :return: devuelve la lista de clientes
        :rtype: list

        Método que devuelve el listado total de clientes de la base de datos

        """
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
        """

        :param dni: dni de un cliente
        :type dni: str
        :return: datos de un cliente
        :rtype: list

        Método que devuelve los datos de un cliente al introducir su dni

        """
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
    def modifCliente(registro):
        """

        :param registro: datos de un cliente
        :type registro: list
        :return: éxito en la modificación de detos de un cliente
        :rtype: bool

        Método que modifica los datos de un cliente en la base de datos

        """
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
        """

        :param dni: dni de un cliente
        :type dni: str
        :return: éxito al dar de baja a un cliente
        :rtype: bool

        Método que añade fecha de baja a un cliente

        """
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
    def cargarMunicipios():
        try:
            listaMuni = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM MUNICIPIOS")
            if query.exec():
                while query.next():
                    listaMuni.append(query.value(1))
                return listaMuni
        except Exception as e:
            print('Error cargando municipios')



    @staticmethod
    def cargarTipoprop():
        """

        :return: todos los tipos de propiedad
        :rtype: list

        Método que devuelve todos los tipos de propiedad almacenados en la bd

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo from tipopropiedad ")
            if query.exec():
                registro = []
                while query.next():
                    registro.append(str(query.value(0)))
                return registro
        except Exception as e:
            print("error cargando tipos de propiedad", e)

    @staticmethod
    def altaTipoprop(tipo):
        """

        :param tipo: nuevo tipo de propiedad
        :type tipo: str
        :return: tipos de propiedad
        :rtype: list

        Método que introduce un nuevo tipo de propiedad y devuelve la lista de tipos de propiedad

        """
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
        """

        :param tipo: tipo de propiedad
        :type tipo: str
        :return: éxito o no en la eliminación de un tipo de propiedad
        :rtype: bool

        Método que elimina un tipo de propiedad

        """
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
        """

        :param propiedad: datos de una propiedad
        :type propiedad: list
        :return: éxito al introducir propiedad en la base de datos
        :rtype: bool

        Método que introduce una nueva propiedad en la base de datos

        """
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
        """

        :param propiedad: datos de propiedad
        :type propiedad: list
        :return: éxito en la modificación de los datos de una propiedad
        :rtype: bool

        Método que modifica los datos de propiedad en la base de datos

        """
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
        """

        :param propiedad: datos de una propiedad
        :type propiedad: list
        :return: éxito al dar de baja a una propiedad
        :rtype: bool

        Método que añade una fecha de baja a una propiedad y modifica su estado

        """
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
        """

        :return: datos filtrados de todas las propiedades
        :rtype: list

        Método que devuelve los datos de todas las propiedades que cumplan con los filtros seleccionados

        """
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

    @staticmethod
    def datosOnePropiedad(codigo):
        """

        :param codigo: codigo de propiedad
        :type codigo: int
        :return: datos de una propiedad
        :rtype: list

        Método que devuelve los datos de la propiedad seleccionada

        """
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
    def cargarAllPropiedadesBD():
        """

        :return: datos de todas las propiedades
        :rtype: list

        Método que devuelve los datos de todas las propiedades almacenadasen la BD

        """
        try:
            listado = []

            base_query = "SELECT * FROM propiedades ORDER BY municipio ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar propiedades en cargarAllpropiedades", e)

    '''
    GESTION DE VENDEDORES
    '''

    @staticmethod
    def altaVendedor(nuevoVendedor):
        """

        :param nuevoVendedor: datos de un vendedor
        :type nuevoVendedor: list
        :return: éxito en añadir a un vendedor a la base de datos
        :rtype: bool

        Método que añade un nuevo vendedor a la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into vendedores (dniVendedor,nombreVendedor,altaVendedor,movilVendedor,mailVendedor,delegacionVendedor) values (:dniVendedor, :nombreVendedor, :altaVendedor, :movilVendedor, :mailVendedor, :delegacionVendedor)")
            query.bindValue(":dniVendedor", str(nuevoVendedor[0]))
            query.bindValue(":nombreVendedor", str(nuevoVendedor[1]))
            query.bindValue(":altaVendedor", str(nuevoVendedor[2]))
            query.bindValue(":movilVendedor", str(nuevoVendedor[3]))
            query.bindValue(":mailVendedor", str(nuevoVendedor[4]))
            query.bindValue(":delegacionVendedor", str(nuevoVendedor[5]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta vendedor en conexion", e)

    @staticmethod
    def datosOneVendedor(valor, tipo_busqueda = "idVendedor"):
        """

        :param valor: valor del tipo de búsqueda que se introduzca introducida
        :type valor: object
        :param tipo_busqueda: nombre de la columna de bd por la que se va a realizar la búsqueda
        :type tipo_busqueda: str
        :return: datos de un vendedor
        :rtype: list

        Método que devuelve los datos de un vendedor en función de un parámetro de búsqueda, siendo su id el predeterminado

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE "+tipo_busqueda+" = :valor")
            query.bindValue(":valor", str(valor))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UN cliente en la tabla.", e)

    @staticmethod
    def listadoVendedores():
        """

        :return: datos de vendedores
        :rtype: list

        Método que devuelve la lista de vendedores

        """
        try:
            listado = []
            historico = var.ui.chkHistoriaVen.isChecked()
            if historico:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores ORDER BY idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores WHERE bajaVendedor is null ORDER BY idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar vendedores")

    @staticmethod
    def bajaVendedor(dni):
        """

        :param dni: dni de un vendedor
        :type dni: str
        :return: éxito al dar de baja a un vendedor en la base de datos
        :rtype: bool

        Método que añade una fecha de baja al vendedor

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT COUNT(*) from vendedores where dniVendedor = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:
                    query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE dniVendedor = :dni")
                    query.bindValue(":bajaVendedor", datetime.now().strftime("%d/%m/%Y"))
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
            print("Error en la conexión al dar de baja vendedor", e)

    @staticmethod
    def modifVendedor(registro):
        """

        :param registro: datos de vendedor
        :type registro: list
        :return: éxito al modificar datos de vendedor en la base de datos
        :rtype: bool

        Método que modifica los datos de un vendedor en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from vendedores where idVendedor = :id")
            query.bindValue(":id", str(registro[0]))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1: #verificamos que solo nos devuelve un resultado, la fila para el dni que buscamos

                    query.prepare("UPDATE vendedores set nombreVendedor= :nombreVendedor, altaVendedor = :altaVendedor, bajaVendedor= :bajaVendedor, movilVendedor = :movilVendedor, mailVendedor = :mailVendedor, delegacionVendedor = :delegacionVendedor WHERE idVendedor = :id")
                    query.bindValue(":id", str(registro[0]))
                    query.bindValue(":nombreVendedor", str(registro[1]))
                    query.bindValue(":altaVendedor", str(registro[2]))
                    query.bindValue(":movilVendedor", str(registro[3]))
                    query.bindValue(":mailVendedor", str(registro[4]))
                    query.bindValue(":delegacionVendedor", str(registro[5]))
                    if registro[6] == "":
                        query.bindValue(":bajaVendedor",QtCore.QVariant()) #QVariant añade un null a la BD
                    else:
                        query.bindValue(":bajaVendedor", str(registro[6]))

                    if query.exec():
                        return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error al modificar un vendedor en conexion.", e)

    @staticmethod
    def cargarAllVendedoresBD():
        """

        :return: datos de todos los vendedores
        :rtype: list

        Método que devuelve todos los datos de los vendedores en la base de datos

        """
        try:
            listado = []

            base_query = "SELECT * FROM vendedores ORDER BY idVendedor ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar vendedores en cargarAllpropiedades", e)


    '''
    GESTION DE FACTURAS
    '''

    @staticmethod
    def altaFactura(registro):
        """

        :param registro: contiene la fecha de creacion de la factura y el dni del cliente
        :type registro: list
        :return: éxito al dar de alta una factura en la base de datos
        :rtype: bool

        Método que da de alta una nueva factura en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO FACTURAS (fechafac, dnicli) values (:fechafac,:dnicli)")
            query.bindValue(":fechafac", str(registro[0]))
            query.bindValue(":dnicli", str(registro[1]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error al dar de alta factura en conexion.", e)

    @staticmethod
    def listadoFacturas():
        """

        :return: datos de las facturas
        :rtype: list

        Método que devuelve todas las facturas de la base de datos

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id, dnicli, fechafac FROM facturas")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando facturas en listadoFacturas - conexión",e)

    '''
    @staticmethod
    def deleteFactura(idFactura):
        """

        :param idFactura: id de una factura
        :type idFactura: int
        :return: éxito en la eliminación de una factura, eliminación de las ventas y actualización de estado disponible para las propiedades
        :rtype: bool

        Método que modifica el estado de una propiedad, elimina las ventas relacionadas con una factura y la propia factura en cascada, haciendo rollback si algo falla

        """
        try:
            db = QtSql.QSqlDatabase.database()
            if not db.transaction():
                print("No se pudo iniciar la transacción.")
                return False

            query_propiedades = QtSql.QSqlQuery()
            query_propiedades.prepare("SELECT codprop FROM ventas WHERE facventa = :idFactura")
            query_propiedades.bindValue(":idFactura", str(idFactura))
            if query_propiedades.exec():
                while query_propiedades.next():
                    idPropiedad = query_propiedades.value(0)
                    query_update_prop = QtSql.QSqlQuery()
                    query_update_prop.prepare("UPDATE propiedades SET estado = 'Disponible', baja = null WHERE codigo = :idPropiedad")
                    query_update_prop.bindValue(":idPropiedad", str(idPropiedad))
                    if not query_update_prop.exec():
                        db.rollback()
                        return False

            query_venta = QtSql.QSqlQuery()
            query_venta.prepare("DELETE FROM ventas WHERE facventa = :idFactura")
            query_venta.bindValue(":idFactura", str(idFactura))
            if not query_venta.exec():
                db.rollback()
                print("Error al eliminar las ventas asociadas:", query_venta.lastError().text())
                return False


            query_factura = QtSql.QSqlQuery()
            query_factura.prepare("DELETE FROM facturas WHERE id = :id")
            query_factura.bindValue(":id", str(idFactura))
            if not query_factura.exec():
                db.rollback()
                print("Error al eliminar la factura:", query_factura.lastError().text())
                return False


            if not db.commit():
                print("Error al confirmar la transacción.")
                return False

            return True

        except Exception as e:
            print("Error al eliminar factura en conexion",str(e))
            if db.isOpen():
                db.rollback()  # Asegúrate de revertir en caso de excepción
            return False
    '''

    @staticmethod
    def deleteFactura(idFactura):
        """

        :param idFactura: identificador de facturas
        :type idFactura: int
        :return: éxito en la eliminación de una factura
        :rtype: bool

        Método para eliminar una factura de la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM facturas WHERE id = :idFactura")
            query.bindValue(":idFactura", str(idFactura))
            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error al borrar factura en conexion",e)

    @staticmethod
    def facturaHasVentas(idFactura):
        """

        :param idFactura: identificador de factura
        :type idFactura: int
        :return: si existen ventas asociadas a la factura o no
        :rtype: bool

        Método que comprueba si una factura tiene ventas asociadas en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) FROM ventas WHERE facventa = :idFactura")
            query.bindValue(":idFactura", str(idFactura))
            if query.exec() and query.first():
                count = query.value(0)
                return count > 0
            else:
                return False
        except Exception as e:
            print("Error al comprobar si factura tiene ventas en conexion",str(e))

    @staticmethod
    def deleteVenta(idVenta,codProp):
        """

        :param idVenta: identificador de venta
        :type idVenta: int
        :param codProp: código de identificador de propiedad
        :type codProp: str
        :return: éxito en la eliminación de la venta o no
        :rtype: bool

        Método para eliminar una venta y cambiar el estado de la propiedad a disponible

        """
        try:
            db = QtSql.QSqlDatabase.database()
            if not db.transaction():
                print("No se pudo iniciar la transacción.")
                return False

            query_prop = QtSql.QSqlQuery()
            query_prop.prepare("""
                                UPDATE propiedades 
                                SET estado = 'Disponible', baja = NULL
                                WHERE codigo = :codProp
                                """)
            query_prop.bindValue(":codProp", str(codProp))
            if not query_prop.exec():
                db.rollback()
                print("Error al cambiar estado de propiedad")
                print(query_prop.lastError().text())
                return False

            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM ventas WHERE idventa = :idVenta")
            query.bindValue(":idVenta", str(idVenta))
            if not query.exec():
                db.rollback()
                print("Error al eliminar venta")
                return False

            if not db.commit():
                print("Error al confirmar la transacción.")
                return False

            return True
        except Exception as e:
            print("Error al eliminar venta en conexion", str(e))


    @staticmethod
    def datosOneFactura(idFactura):
        """

        :param idFactura: id de la factura
        :type idFactura: int
        :return: datos de la factura buscada
        :rtype: list

        Método que devuelve los datos de la factura seleccionada

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas WHERE id = :id")
            query.bindValue(":id", str(idFactura))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as e:
            print("Error al cargar one factura en conexion.", e)

    @staticmethod
    def altaVenta(registro):
        """

        :param registro: datos de la venta: id de la factura, codigo de propiedad e id del vendedor
        :type registro: list
        :return: éxito al dar de alta una venta
        :rtype: bool

        Método que da de alta una nueva venta en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO VENTAS (facventa,codprop,agente) values (:facventa,:codprop,:agente)")
            query.bindValue(":facventa", str(registro[0]))
            query.bindValue(":codprop", str(registro[1]))
            query.bindValue(":agente", str(registro[2]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error al dar de alta factura en conexion.", e)

    @staticmethod
    def venderPropiedad(codigoPropiedad):
        """

        :param codigoPropiedad: id de la propiedad
        :type codigoPropiedad: int
        :return: éxito al cambiar el estado de la propiedad a vendida
        :rtype: bool

        Método que actualiza el estado de una propiedad a vendido y actualiza la fecha de baja

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET estado = 'Vendido', baja = :fechaBaja WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", datetime.now().strftime("%d/%m/%Y"))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error al vender una Propiedad en conexion.", e)

    @staticmethod
    def listadoVentas(idFactura):
        """

        :param idFactura: id de la factura que contiene las ventas
        :type idFactura: int
        :return: datos de todas las ventas relacionadas con la factura
        :rtype: list

        Método que devuelve todos los datos de las ventas relacionadas con una factura

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT v.idventa, v.codprop, p.direccion, p.municipio, p.tipo_propiedad, p.precio_venta FROM ventas AS v INNER JOIN propiedades as p on v.codprop = p.codigo WHERE v.facventa = :facventa")
            query.bindValue(":facventa", str(idFactura))
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando facturas en listadoFacturas - conexión",e)

    @staticmethod
    def datosOneVenta(idVenta):
        """

        :param idVenta: id de la venta seleccioanda
        :type idVenta: int
        :return: datos de la venta buscada
        :rtype: list

        Método que devuelve los datos de una venta seleccionada

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT v.agente, v.codprop, p.tipo_propiedad, p.precio_venta, p.municipio, p.direccion  FROM ventas as v INNER JOIN propiedades as p ON v.codprop = p.codigo WHERE v.idventa = :idventa")
            query.bindValue(":idventa", str(idVenta))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as e:
            print("Error en datosOneVenta en conexion", e)

    @staticmethod
    def propiedadIsVendida(codigo):
        """

        :param codigo: codigo identificador de propiedad
        :type codigo: str
        :return: si la propiedad se encuentra vendida o no
        :rtype: bool

        Método de conexión a la base de datos para comprobar si una propiedad se encuentra vendida o no

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT estado FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec() and query.next():
                estado = query.value(0)
                return estado == "Vendido"
            else:
                return False
        except Exception as e:
            print("Error en propiedadIsVendida en conexion", str(e))

    '''
    GESTIÓN DE ALQUILERES
    '''

    @staticmethod
    def altaAlquiler(registro):
        """

        :param registro: datos de un nuevo contrato de alquiler
        :type registro: list
        :return: éxito al insertar un nuevo contrato de alquiler
        :rtype:bool

        Método para insertar un nuevo contrato de alquiler en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO alquileres(propiedad_id,cliente_dni,fecha_inicio,fecha_fin,vendedor) values (:codigoprop,:dnicli,:fecha_inicio,:fecha_fin,:vendedor)")
            query.bindValue(":codigoprop", str(registro[0]))
            query.bindValue(":dnicli", str(registro[1]))
            query.bindValue(":fecha_inicio", str(registro[2]))
            query.bindValue(":fecha_fin", str(registro[3]))
            query.bindValue(":vendedor", str(registro[4]))
            if query.exec():
                query_propiedad = QtSql.QSqlQuery()
                query_propiedad.prepare("UPDATE propiedades SET estado = 'Alquilado', baja = :fecha_baja WHERE  codigo = :codigo")
                query_propiedad.bindValue(":codigo", str(registro[0]))
                query_propiedad.bindValue(":fecha_baja", str(registro[2]))
                if query_propiedad.exec():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error en altaAlquiler en conexion", e)

    @staticmethod
    def propiedadIsAlquilada(codigo):
        """

        :param codigo: codigo identificador de propiedad
        :type codigo: str
        :return: si la propiedad se encuentra alquilada o no
        :rtype: bool

        Método de conexión a la base de datos para comprobar si una propiedad se encuentra alquilada o no

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT estado FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec() and query.next():
                estado = query.value(0)
                return estado == "Alquilado"
            else:
                return False
        except Exception as e:
            print("Error en propiedadIsVendida en conexion", str(e))

    @staticmethod
    def listadoAlquileres():
        """

        :return: identificador y cliente de todos los contratos de alquiler
        :rtype: list

        Método que devuelve el identificador y el cliente de todos los contratos de alquiler que tengamos registrados

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id, cliente_dni FROM alquileres")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando alquileres en listadoAlquileres - conexión",str(e))

    @staticmethod
    def datosOneAlquiler(idAlquiler):
        """

        :param idAlquiler: identificador del contrato de alquiler
        :type idAlquiler: int
        :return: todos los datos de un contrato de alquiler (sin mensualidades)
        :rtype: list

        Método para obtener los datos de un contrato de alquiler a partir de su identificador

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT a.id, a.fecha_inicio, a.fecha_fin, a.vendedor, c.dnicli, c.nomecli, c.apelcli, p.codigo, p.tipo_propiedad, p.precio_alquiler, p.municipio, p.direccion FROM alquileres as a INNER JOIN propiedades as p ON a.propiedad_id = p.codigo INNER JOIN clientes as c ON a.cliente_dni = c.dnicli WHERE a.id = :idAlquiler")
            query.bindValue(":idAlquiler", str(idAlquiler))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as e:
            print("Error en datosOneAlquiler en conexion", str(e))

    @staticmethod
    def idOneAlquiler(codPropiedad,dniCliente):
        """

        :param codPropiedad: identificador de propiedad
        :type codPropiedad: int
        :param dniCliente: el identificador de un cliente, su DNI
        :type dniCliente: str
        :return: el identificador de un contrato de alquiler
        :rtype: id

        Método para obtener el id de un contrato de alquiler en función del id de la propiedad y el id del cliente
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id FROM alquileres WHERE cliente_dni = :dniCliente AND propiedad_id = :codPropiedad")
            query.bindValue(":dniCliente", str(dniCliente))
            query.bindValue(":codPropiedad", str(codPropiedad))
            if query.exec():
                while query.next():
                    return query.value(0)
        except Exception as e:
            print("Error en datosOneAlquiler dnicli codprop en conexion", str(e))

    @staticmethod
    def altaMensualidad(registro):
        """

        :param registro: datos de una mensualidad
        :type registro: list
        :return: éxito al insertar una nueva mensualidad
        :rtype: bool

        Método para registrar una nueva mensualidad respecto de un contrato de alquiler

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO mensualidades(idalquiler, mes, pagado) VALUES (:idalquiler,:mes,:pagado)")
            query.bindValue(":idalquiler", str(registro[0]))
            query.bindValue(":mes", str(registro[1]))
            query.bindValue(":pagado", str(registro[2]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al grabar nueva mensualidad en conexion", str(e))

    @staticmethod
    def listadoMensualidades(idAlquiler):
        """

        :param idAlquiler: identificador de un contrato de alquiler
        :type idAlquiler: int
        :return: todos los datos las mensualidades de un contrato de alquiler
        :rtype: list

        Método para obtener todos los datos de las mensualidades relacionadas con un contrato de alquiler

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idmensualidad, mes, pagado FROM mensualidades WHERE idalquiler = :idalquiler")
            query.bindValue(":idalquiler", str(idAlquiler))
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error en listadoMensualidades - conexion", str(e))

    @staticmethod
    def pagarMensualidad(idMensualidad):
        """

        :param idMensualidad: identificador de mensualidad
        :type idMensualidad: int
        :return: éxito al marcar como pagada una mensualidad
        :rtype: bool

        Método para registrar en la base de datos el pago de una mensualidad

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE mensualidades SET pagado = 1 WHERE idmensualidad = :idMensualidad")
            query.bindValue(":idMensualidad", idMensualidad)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error en pagar mensualidad",str(e))

    @staticmethod
    def datosOneMensualidad(idMensualidad):
        """

        :param idMensualidad: identificador de la mensualidad
        :type idMensualidad: int
        :return: todos los datos de la mensualidad
        :rtype: list

        Método para obtener todos los datos de una mensualidad dado su identificador

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idalquiler, mes, pagado FROM mensualidades WHERE idmensualidad = :idMensualidad")
            query.bindValue(":idMensualidad", idMensualidad)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro

        except Exception as e:
            print("Error al cargar datos de una mensualidad en conexcion",str(e))

    @staticmethod
    def modificarFechaFinContrato(idAlquiler, nuevaFechaFin):
        """

        :param idAlquiler: identificador de un contrato de alquiler
        :type idAlquiler: int
        :param nuevaFechaFin: fecha de finalización de contrato nueva
        :type nuevaFechaFin: datetime
        :return: éxito al modificar la fecha de finalización de un contrato de alquiler
        :rtype: bool

        Método para modificar la fecha de finalización de un contrato en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE alquileres set fecha_fin = :nuevaFechaFin WHERE id = :idAlquiler")
            query.bindValue(":nuevaFechaFin", str(nuevaFechaFin))
            query.bindValue(":idAlquiler", idAlquiler)
            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error modifcando fecha de alquiler en conexion", str(e))

    @staticmethod
    def eliminarMensualidad(idMensualidad):
        """

        :param idMensualidad: identificador de la mensualidad
        :type idMensualidad: int
        :return: éxito al eliminar una mensualidad
        :rtype: bool

        Método para eliminar una mensualidad de la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM mensualidades WHERE idmensualidad = :idMensualidad")
            query.bindValue(":idMensualidad", idMensualidad)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error eliminando mensualidad",str(e))


    @staticmethod
    def eliminarContratoAlquiler(idAlquiler):
        """

        :param idAlquiler: identificador del contrato de alquiler
        :type idAlquiler: int
        :return: éxito al eliminar el contrato, eliminar sus mensualidades y restablecer la propiedad a disponible
        :rtype: bool

        Método que elimina un contrato de alquiler de la base de datos, eliminando sus mensualidades relacionadas y restableciendo a disponible la propiedad del contrato

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM mensualidades WHERE idalquiler = :idAlquiler")
            query.bindValue(":idAlquiler", idAlquiler)
            if not query.exec():
                return False

            query_prop = QtSql.QSqlQuery()
            query_prop.prepare("UPDATE propiedades SET estado = 'Disponible', baja = NULL WHERE codigo = ( SELECT propiedad_id FROM alquileres WHERE id = :idAlquiler) ")
            query_prop.bindValue(":idAlquiler", idAlquiler)
            if not query_prop.exec():
                return False

            query_alq = QtSql.QSqlQuery()
            query_alq.prepare("DELETE FROM alquileres WHERE id = :idAlquiler")
            query_alq.bindValue(":idAlquiler", idAlquiler)
            if query_alq.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al eliminar un contrato de alquiler en conexion", str(e))