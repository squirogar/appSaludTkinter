import sqlite3 as sq

"""
Módulo de base de datos para la aplicación SaludMás

1. Este módulo cuenta con las siguientes funciones diseñadas:
- Conexion a base de datos
- autenticación
- creación de tablas
- actualización de tablas
- inserción de registros
- lectura de registros
- eliminación de registros

2. Las entidades de la bd para esta aplicación son:
- PACIENTE
- USUARIO
- ATENCION
- EXAMEN
- COMPRA_EXAMEN
- PREVISION
"""



def connectar():
    """
    Conecta con la base de datos. Si no la encuentra, crea una nueva.

    Retorna un objeto Connection
    """
    conn = None
    try:
        conn = sq.connect("data")
        conn.execute("PRAGMA foreign_keys = 1")
    except sq.Error as e:
        print(e.args[0])
    
    return conn

def autenticacion(conn, tupla):
    """
    Si los datos de login que están en "tupla" existen dentro de la base de datos,
    entonces se retorna los datos de ese usuario específico.

    La tupla debe contener:
    1. nombre_usuario
    2. password

    Retorna una tupla
    """
    miCursor = conn.cursor()
    user = ()
    try:
        miCursor.execute(
            f"SELECT * FROM USUARIO WHERE NOMBRE_USUARIO = '{tupla[0]}' AND PASSWORD = '{tupla[1]}'"
        )
        user = miCursor.fetchone()
        print("user", user)
    except sq.Error as e:
        print(e.args[0])
    finally:    
        miCursor.close()
    return user

def crearTablaUsuario(conn):
    """
    Crea la tabla de usuarios administrativos que son los que utilizarán 
    la aplicación.
    
    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS USUARIO (
                NOMBRE_USUARIO VARCHAR(10) PRIMARY KEY,
                RUT VARCHAR(10) UNIQUE NOT NULL,
                NOMBRE VARCHAR(100) NOT NULL, 
                APELLIDO VARCHAR(100) NOT NULL, 
                CARGO VARCHAR(100) NOT NULL, 
                PASSWORD VARCHAR(10) NOT NULL
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def crearTablaPaciente(conn):
    """
    Crea la tabla de pacientes que son atendidos por los usuarios 
    administrativos.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PACIENTE (
                RUT VARCHAR(10) PRIMARY KEY, 
                NOMBRE VARCHAR(100) NOT NULL,
                APELLIDO VARCHAR(100) NOT NULL, 
                DIRECCION VARCHAR(300) NOT NULL, 
                FECHA_NAC VARCHAR(10) NOT NULL, 
                EMAIL VARCHAR(50) NOT NULL, 
                TELEFONO INTEGER NOT NULL, 
                ID_PREVISION INTEGER NOT NULL,
                FOREIGN KEY(ID_PREVISION) REFERENCES PREVISION(ID)
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def crearTablaAtencion(conn):
    """
    Crea la tabla de atenciones hechas a un paciente. Los usuarios administrativos 
    son los encargados de realizarlas.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ATENCION (
                NUM_ATENCION INTEGER PRIMARY KEY AUTOINCREMENT, 
                FECHA_ATENCION VARCHAR(16) NOT NULL, 
                TIPO_SERVICIO VARCHAR(300) NOT NULL,
                NOMBRE_MEDICO_TRATANTE VARCHAR(300) NOT NULL,
                ESPECIALIDAD_MEDICO_TRATANTE VARCHAR(300) NOT NULL,
                RUT_PACIENTE VARCHAR(10) NOT NULL,
                USUARIO VARCHAR(10) NOT NULL,
                FOREIGN KEY(RUT_PACIENTE) REFERENCES PACIENTE(RUT), 
                FOREIGN KEY(USUARIO) REFERENCES USUARIO(NOMBRE_USUARIO)
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def crearTablaExamen(conn):
    """
    Crea la tabla de examenes que podrán ser comprados durante la atención.

    Retorna True si la operación fue exitosa, caso contrario False.
    """

    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS EXAMEN (
                CODIGO VARCHAR(10) PRIMARY KEY, 
                NOMBRE VARCHAR(300) NOT NULL UNIQUE,
                DESCRIPCION VARCHAR(500),
                TIEMPO_ENTREGA VARCHAR(100) NOT NULL, 
                PRECIO_UNITARIO FLOAT NOT NULL 
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def crearTablaCompraExamen(conn):
    """
    Crea la Compra_examen que registra la compra de los exámenes hecha por 
    el paciente durante su atención.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS COMPRA_EXAMEN (
                NUMERO_ATENCION INTEGER NOT NULL,
                CODIGO_EXAMEN VARCHAR(10) NOT NULL,
                CANTIDAD_EXAMEN INTEGER NOT NULL,
                TOTAL FLOAT NOT NULL,
                PRIMARY KEY(NUMERO_ATENCION, CODIGO_EXAMEN)
                FOREIGN KEY(NUMERO_ATENCION) REFERENCES ATENCION(NUM_ATENCION)
                FOREIGN KEY(CODIGO_EXAMEN) REFERENCES EXAMEN(CODIGO)
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def crearTablaPrevision(conn):
    """
    Crea la tabla de Previsiones. Sólo hay 2 previsiones: FONASA e ISAPRE, 
    por lo que hay que asegurarse en la base de datos que sólo esas dos estén.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PREVISION (
                ID INTEGER PRIMARY KEY, 
                NOMBRE VARCHAR(50) NOT NULL UNIQUE
            )
            """
        )
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def insertaUsuario(conn, tupla):
    """
    Se registra un usuario administrativo dentro de la base de datos.

    La tupla debe contener:
    1. nombre_usuario
    2. rut
    3. nombre
    4. apellido
    5. cargo
    6. password     

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            "INSERT INTO USUARIO VALUES(?,?,?,?,?,?)", tupla
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def insertaPaciente(conn, tupla):
    """
    Se registra un paciente dentro de la base de datos.

    La tupla debe contener:
    1. rut
    2. nombre
    3. apellido
    4. direccion
    5. fecha_nac
    6. email
    7. telefono
    8. id_prevision

    Retorna True si la operación fue exitosa, caso contrario False.
    """    
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            "INSERT INTO PACIENTE VALUES(?,?,?,?,?,?,?,?)", tupla
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()

def insertaPrevision(conn, prevision):
    """
    Se registra una previsión dentro de la base de datos.
    Se debe asegurar que ésta ya esté con las dos previsiones disponibles
    antes de poner la aplicación en producción.

    La tupla debe contener:
    1. id
    2. nombre    

    Retorna True si la operación fue exitosa, caso contrario False.
    """    
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            "INSERT INTO PREVISION VALUES(NULL, ?)", prevision
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def insertaExamen(conn, tupla):
    """
    Se registra un examen dentro de la base de datos.
    Se debe asegurar que ésta ya estén todos los examen disponibles
    antes de poner la aplicación en producción.

    La tupla debe contener:
    1. codigo
    2. nombre
    3. descripcion
    4. tiempo_entrega
    5. precio_unitario

    Retorna True si la operación fue exitosa, caso contrario False.
    """    
    miCursor = conn.cursor()
    try:
        miCursor.execute(
            "INSERT INTO EXAMEN VALUES(?,?,?,?,?)", tupla
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def insertaAtencion(conn, tupla):
    """
    Se registra una atención dentro de la base de datos.
    
    El campo "num_atencion" es generado de forma automática por sqlite
    El campo "fecha_atencion" es calculado.

    La tupla debe contener:
    1. tipo_servicio
    2. nombre_medico_tratante
    3. especialidad_medico_tratante
    4. rut_paciente
    5. usuario

    Retorna True si la operación fue exitosa, caso contrario False.
    """        
    miCursor = conn.cursor()

    # solo para obtener la fecha
    import datetime
    x = datetime.datetime.now()
    hora = str(x.hour)
    minuto = str(x.minute)
    if x.hour < 10:
        hora = "0" + hora
    if x.minute < 10:
        minuto = "0" + minuto

    fecha = "{}-{}-{} {}:{}".format(x.day, x.month, x.year, hora, minuto)

    try:
        miCursor.execute(
            f"""INSERT INTO ATENCION VALUES(NULL,'{fecha}','{tupla[0]}','{tupla[1]}',
            '{tupla[2]}','{tupla[3]}','{tupla[4]}')"""
        )
        conn.commit()
        
        print("atencion despues de insercion:",leeDatosAtencion(conn))
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def insertaCompraExamen(conn, tupla):
    """
    Se registra una compra de examen hecha durante la atención
    en la base de datos.

    La tupla debe contener:
    1. numero_atencion
    2. codigo_examen
    3. cantidad_examen
    4. total: precio_unitario*cantidad_examen

    Retorna True si la operación fue exitosa, caso contrario False.
    """    
    miCursor = conn.cursor()

    try:
        miCursor.execute(
            "INSERT INTO COMPRA_EXAMEN VALUES(?,?,?,?)", tupla
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def actualizaDatosPaciente(conn, tupla):
    """
    Se actualizan los datos de un paciente.
    
    La tupla debe contener los siguientes datos:
    0. rut
    1. nombre
    2. apellido
    3. direccion
    4. fecha_nac
    5. email
    6. telefono
    7. id_prevision
    
    El campo rut no se cambia en la actualizacion por ser clave primaria.

    Retorna True si la operación fue exitosa, caso contrario False.
    """    
    miCursor = conn.cursor()

    try: 
        miCursor.execute(
            f"""UPDATE PACIENTE SET NOMBRE = ?, APELLIDO = ?, DIRECCION = ?, 
            FECHA_NAC = ?, EMAIL = ?, TELEFONO = ?, ID_PREVISION = ?
            WHERE RUT = '{tupla[0]}'
            """, tupla[1:]
        )
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()



def leeDatosPacientes(conn, rut=None):
    """
    Retorna la informacion de un paciente o de todos los pacientes que estan 
    en la base de datos de acuerdo al parámetro "rut".

    Retorna una lista de tuplas con los registros
    """
    miCursor = conn.cursor()
    resultado = []

    try:
        if rut is None:
            miCursor.execute(
                """SELECT p.*, prev.nombre FROM PACIENTE p 
                INNER JOIN PREVISION prev ON p.ID_PREVISION = prev.ID"""
            )
        else:
            miCursor.execute(
                f"""SELECT p.*, prev.nombre FROM PACIENTE p 
                INNER JOIN PREVISION prev ON p.ID_PREVISION = prev.ID 
                WHERE RUT='{rut}'"""
            )
        resultado = miCursor.fetchall()

    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
        
    print("datos pacientes", resultado)
    return resultado


#retona toda la informacion correspondiente a un usuario especifico
def leeDatosUsuario(conn, usuario):
    """
    Retorna la informacion de un usuario administrativo está 
    en la base de datos de acuerdo al parámetro "usuario". Este parámetro
    representa el nombre_usuario del usuario administrativo dentro de
    la base de datos.

    Retorna una lista de tuplas.
    """
    miCursor = conn.cursor()
    resultado = []
    try:
        miCursor.execute(f"SELECT * FROM USUARIO WHERE NOMBRE_USUARIO = '{usuario}'")
        resultado = miCursor.fetchall()
    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
    print("datos usuario", resultado)
    
    return resultado


def leeDatosPrevision(conn, nombre=None):
    """
    Retorna la informacion de la prevision o de todos las previsiones 
    que estan en la base de datos de acuerdo al parámetro "nombre".

    Retorna una lista de tuplas con los registros
    """

    miCursor = conn.cursor()
    resultado = []
    try:
        if nombre is None:
            miCursor.execute("SELECT * FROM PREVISION")
        else:
            miCursor.execute(f"SELECT * FROM PREVISION WHERE NOMBRE = '{nombre}'")
        resultado = miCursor.fetchall()
    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
        
    print("datos prevision", resultado)
    return resultado


def leeDatosExamen(conn, codigo = None, nombre = None):
    """
    Retorna la informacion de un examen o de todos los examenes
    que estan en la base de datos de acuerdo al parámetro "codigo"
    y/o al "nombre".

    Retorna una lista de tuplas con los registros

    """
    miCursor = conn.cursor()
    resultado = []
    try:
        if codigo is not None and nombre is not None:
            miCursor.execute(
                f"""SELECT * FROM EXAMEN WHERE CODIGO = '{codigo}'
                AND NOMBRE = '{nombre}'"""
            )
        elif codigo is not None and nombre is None:
            miCursor.execute(f"SELECT * FROM EXAMEN WHERE CODIGO = '{codigo}'")
        elif codigo is None and nombre is not None:   
            miCursor.execute(f"SELECT * FROM EXAMEN WHERE NOMBRE = '{nombre}'")
        else:
            miCursor.execute(f"SELECT * FROM EXAMEN")
        resultado = miCursor.fetchall()

    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
    print("datos examen", resultado)
    
    return resultado


def leeDatosAtencionPaciente(conn, rut):
    """
    Retorna la informacion de las atenciones de un paciente si es que se
    especifica un rut. Caso contrario, se retornan todas las atenciones
    de la base de datos.

    Retorna una lista de tuplas con los registros
    """
    miCursor = conn.cursor()
    resultado = []
    try:
        miCursor.execute(
            f"""SELECT a.*, sum(ce.TOTAL) AS monto_total FROM ATENCION a, COMPRA_EXAMEN ce 
            WHERE a.NUM_ATENCION = ce.NUMERO_ATENCION
            AND RUT_PACIENTE = '{rut}'
            GROUP BY a.NUM_ATENCION 
            ORDER BY a.FECHA_ATENCION ASC"""
        )
        resultado = miCursor.fetchall()
    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
        
    print("datos atencion PACIENTE", resultado)
    return resultado


def leeDatosAtencion(conn):
    miCursor = conn.cursor()
    resultado = []
    try:
        miCursor.execute(
            f"""SELECT * FROM ATENCION"""
        )
        resultado = miCursor.fetchall()
    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
        
    print("datos atencion all", resultado)
    return resultado


def leeDatosCompraExamen(conn, numero_atencion):
    """
    Retorna los datos de las compras de examenes hecha en una 
    atención específica. 
    
    Retorna los registros en una lista de tuplas.

    """    
    miCursor = conn.cursor()
    resultado = []
    try:
        miCursor.execute(f"SELECT * FROM COMPRA_EXAMEN WHERE NUMERO_ATENCION = {numero_atencion}")
        resultado = miCursor.fetchall()
    except sq.Error as e:
        print(e.args[0])
    finally:
        miCursor.close()
    print("datos compra examen", resultado)
    
    return resultado




def borraPaciente(conn, rut):
    """
    Elimina un paciente. Al borrar este paciente se debe borrar 
    sus atenciones y las compras de examenes que haya hecho.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        atenciones = leeDatosAtencionPaciente(conn, rut)

        # si el paciente tiene atenciones las borramos
        if atenciones != []:
            for atencion in atenciones:
                # borramos las compras de examenes
                exito = borraCompraExamen(conn, atencion[0])
                if exito == False:
                    return False
                 
            # borramos las atenciones del paciente
            exito = borraAtencion(conn, rut)
            if exito == False:
                return False

        # borramos el paciente de la base de datos
        miCursor.execute(f"DELETE FROM PACIENTE WHERE RUT = '{rut}'")
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()

def borraAtencion(conn, rut):
    """
    Elimina todas las atenciones de un paciente dado su rut.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(f"DELETE FROM ATENCION WHERE RUT_PACIENTE = '{rut}'")
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()  


def borraExamen(conn, codigo):
    """
    Elimina un examen.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    try:
        miCursor.execute(f"DELETE FROM EXAMEN WHERE CODIGO = '{codigo}'")
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


def borraCompraExamen(conn, numero_atencion, codigo = None):
    """
    Elimina una compra de examen.
    Si se proporciona el código junto con el numero de atencion, se borrará una compra
    de examen específica.
    Si se proporciona solamente el numero de atencion, se borrará todas las compras
    de examenes hechas en dicha atención.

    Retorna True si la operación fue exitosa, caso contrario False.
    """
    miCursor = conn.cursor()
    sentencia = f"DELETE FROM COMPRA_EXAMEN WHERE NUMERO_ATENCION = '{numero_atencion}'"

    if codigo is not None:
        sentencia += f" AND CODIGO_EXAMEN = '{codigo}'"
    try:
        miCursor.execute(sentencia)
        conn.commit()
        return True
    except sq.Error as e:
        print(e.args[0])
        return False
    finally:
        miCursor.close()


if __name__ == "__main__":
    conn = connectar()
    if conn is not None:
        #Creamos las tablas primero
        crearTablaUsuario(conn)
        crearTablaPrevision(conn)
        crearTablaPaciente(conn)
        crearTablaExamen(conn)
        crearTablaAtencion(conn)
        crearTablaCompraExamen(conn)

        #inserta registros
        insertaUsuario(conn, ("squirogar", "11111111-1", "Seb", "Quiroga", "Gerente", "1234"))
        insertaUsuario(conn, ("Danqui", "22222222-2", "Dan", "Quiroga", "Administrador", "1234"))
        insertaUsuario(conn, ("Mariaqui", "33333333-3", "Maria", "Quiroga", "Supervisor", "1234"))
        
        insertaPrevision(conn, ("FONASA",))
        insertaPrevision(conn, ("ISAPRE",))
        
        insertaExamen(conn, (
            "03.03.006", "CORTISOL AM", "Cortisol en ayunas. Hormona del estrés secretada por glándula suprarrenal", 
            "en el día", 7870)
        )
        
        insertaExamen(conn, (
            "03.03.002", "ALDOSTERONA", "Hormona secretada por glándula suprarrenal. Controla la presión arterial ", 
            "3 días hábiles", 12480
            )
        )
        insertaExamen(conn, (
            "03.03.021", "RENINA", "Hormona de riñon. Controla la producción de Aldosterona.", 
            "3 a 5 días hábiles", 70560
            )
        )
    
"""
        insertaPaciente(conn, (
            "12345678-9", "paciente prueba", "test", "calleprueba123", "10-10-1990",
            "test@test.cl", 12345689, 1)
        )


        
        
        #actualiza pacientes
        actualizaDatosPaciente(conn, "12345678-9", apellido = "pac apellido")

        
        insertaAtencion(
            conn, ("unidad de examenes", "juan perez", "medicina general", "12345678-9", "danqui")
        )
        insertaAtencion(
            conn, ("unidad de examenes", "Fido dido", "medicina general", "12345678-9", "danqui")
        )
        insertaAtencion(
            conn, ("unidad de examenes", "Gary stu", "medicina general", "12345678-9", "danqui")
        )

        
        #lee datos
        leeDatosPacientes(conn)
        leeDatosPacientes(conn, "12345678-9edw")
        leeDatosUsuario(conn, "squirogar")
        leeDatosPrevision(conn)
        leeDatosPrevision(conn, "FONASA")
        leeDatosExamen(conn)
        leeDatosAtencion(conn, "12345678-9")
        leeDatosAtencion(conn)
        

        insertaCompraExamen(conn, (1, "03.03.006", 2))
        insertaCompraExamen(conn, (0, "03.03.006", 4))
        insertaCompraExamen(conn, (0, "03.03.002", 1))

        leeDatosCompraExamen(conn, 0)
        leeDatosCompraExamen(conn, 1)

        print("\n---Borra datos---")
        borraPaciente(conn, "12345678-9")
        leeDatosPacientes(conn)
        leeDatosAtencion(conn)
        leeDatosCompraExamen(conn, 1)
        
        borraExamen(conn, "03.03.002")
        leeDatosExamen(conn)
"""
