from datetime import datetime

import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets

class ConexionServer():
    @staticmethod
    def crear_conexion():

        try:
            conexion = mysql.connector.connect(
            host='192.168.10.66', # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
            user='dam',
            password='dam2425',
            database='bbdd',
            charset="utf8mb4",
            collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
            # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                #print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()

        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    @staticmethod
    def listadoClientes():
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            cursor.execute("SELECT dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli, bajacli  FROM clientes ORDER BY apelcli, nomecli ASC")
            resultados = cursor.fetchall()
            # Procesar cada fila de los resultados
            for fila in resultados:
                # Crear una lista con los valores de la fila
                listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes

            # Cerrar el cursor y la conexión si no los necesitas más
            cursor.close()
            conexion.close()
            return listadoclientes
        except Exception as e:
            print("error listado de clientes en conexión", e)


    @staticmethod
    def altaCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    @staticmethod
    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli, bajacli FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error


    @staticmethod
    def bajaCliente(dni):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                UPDATE clientes SET bajacli = %s WHERE dnicli = %s
                """
                fecha_baja =  datetime.now().strftime("%d/%m/%Y")
                cursor.execute(query, (fecha_baja,dni))
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    @staticmethod
    def modifCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                reordenarCliente = cliente[1:] + [cliente [0]]
                query = """
                UPDATE clientes 
                SET altacli = %s, apelcli = %s, nomecli = %s,emailcli = %s, movilcli = %s, dircli = %s, provcli = %s, municli = %s, bajacli = %s 
                WHERE dnicli = %s
                """
                cursor.execute(query, reordenarCliente)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")


    '''
    CONEXION A TABLA PROPIEDADES
    '''

    @staticmethod
    def cargarTipoprop():
        try:
            conexion = ConexionServer().crear_conexion()
            registro = []
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo from tipopropiedad")
            resultados = cursor.fetchall()
            for fila in resultados:
                registro.append(fila[0])
            cursor.close()
            return registro
        except Exception as e:
            print("error cargando tipos de propiedad", e)

    @staticmethod
    def listadoPropiedades():
        try:
            conexion = ConexionServer().crear_conexion()
            listadoPropiedades = []
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo,altaprop,bajaprop,dirprop,provprop,muniprop,tipoprop,habprop,banprop,superprop,prealquiprop,prevenprop,cpprop,obserprop,tipooper,estadoprop,nomeprop,movilprop FROM propiedades ORDER BY muniprop ASC")
            resultados = cursor.fetchall()
            for fila in resultados:
                listadoPropiedades.append(list(fila))

            cursor.close()
            conexion.close()
            return listadoPropiedades
        except Exception as e:
            print("error listado de propiedades en conexión", e)

    @staticmethod
    def datosOnePropiedad(codigo):
        registro = []  # Inicializa la lista para almacenar los datos de la propiedad
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT codigo,altaprop,bajaprop,dirprop,provprop,muniprop,tipoprop,habprop,banprop,superprop,prealquiprop,prevenprop,cpprop,obserprop,tipooper,estadoprop,nomeprop,movilprop FROM propiedades WHERE codigo = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (codigo,))
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de una propiedad:", e)
            return None  # Devolver None en caso de error

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO propiedades (altaprop,dirprop,provprop,muniprop,tipoprop,habprop,banprop,superprop,prealquiprop,prevenprop,cpprop,obserprop,tipooper,estadoprop,nomeprop,movilprop)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
                """
                propiedad[12] = str(propiedad[12])
                cursor.execute(query, propiedad)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar una propiedad", e)

    @staticmethod
    def modifPropiedad(propiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                reordenarPropiedad = propiedad[1:] + [propiedad[0]]
                query = """
                
                UPDATE propiedades 
                SET altaprop = %s, bajaprop = %s, dirprop = %s, provprop = %s,muniprop = %s, tipoprop = %s, habprop = %s, banprop = %s, superprop = %s, prealquiprop = %s , prevenprop = %s,cpprop = %s,obserprop = %s,tipooper = %s,estadoprop = %s,nomeprop = %s,movilprop = %s
                WHERE codigo = %s
                """
                reordenarPropiedad[13] = str(reordenarPropiedad[13])
                cursor.execute(query, reordenarPropiedad)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")