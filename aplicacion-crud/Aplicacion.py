"""
Ventana de aplicación principal

"""
import tkinter as tk
import RegFrame as regf
import ListaPacFrame as lpf
import MainMenuFrame as mmf
import ModFrame as mdf
import ListaAtencionFrame as laf
import GenAtencionFrame as gaf
from tkinter import messagebox

class Aplicacion(tk.Tk):
    """
    Es la clase que crea la ventana principal root donde correrá el programa.
    Extiende de la clase Tk de tkinter.

    Esta clase contiene los siguientes frames en forma de variables de instancia:
    - registro, que es un frame para el registro de pacientes
    - lista, que es un frame para el listado de pacientes guardados
    - main, que es un frame para el menú principal
    - modPac, que es un frame para visualizar, modificar y eliminar los datos
    de un paciente
    - 

    """
    ventana = None
    
    
    def __init__(self):
        super().__init__()
        self.title("appSaludTkinter")
        self.protocol('WM_DELETE_WINDOW', self.avisoSalida)
        self.resizable(False, False)
        #self.geometry("400x600")

        # contendrá un objeto Connection que se utiliza para conectar 
        # a la base de datos
        self.__conexion = None

        # contendrá una tupla con los datos del usuario que inició
        # sesión
        self.__sesion = None

        
        #--barra de menú--#
        self.__miMenu = self.__creaMenu()
        self.config(menu=self.__miMenu)

        #---frames--#
        self.registro = regf.RegFrame(self)
        self.lista = lpf.ListaPacFrame(self)
        self.main = mmf.MainFrame(self)
        self.modPac = mdf.modFrame(self)
        self.listaAtencion = laf.ListaAtencionFrame(self)
        self.genAtencion = gaf.GenAtencionFrame(self)
        

        # mostramos el frame main
        self.main.grid(row=0, column=0)
        self.__frameActual = self.main

    def __creaMenu(self):
        """
        Retorna una barra de menú con los siguientes opciones:
        - Archivo:
            - cerrar sesion
            - salir
        
        - Ayuda:
            - licencia
            - acerca de

        """
        nuevoMenu = tk.Menu(self)
        archivo = tk.Menu(self, tearoff=0) 
        ayuda = tk.Menu(self, tearoff=0) 

        archivo.add_command(label="Cerrar Sesión", command=self.__cerrarSesion)
        archivo.add_separator()
        archivo.add_command(label="Salir de aplicación", command=self.avisoSalida)
        
        #limpiar.add_command(label="Limpiar todos los campos", command=limpiaCampos)
        ayuda.add_command(label="Licencia", command=self.avisoLicencia)
        ayuda.add_command(label="Acerca de", command=self.avisoAcercaDe)
        
        nuevoMenu.add_cascade(label="Archivo", menu=archivo)
        nuevoMenu.add_cascade(label="Ayuda", menu=ayuda)

        return nuevoMenu

    def __cerrarSesion(self):
        """
        Cierra la sesión del usuario actual.
        Antes de cerrar sesión se asegura de ocultar la ventana principal
        root y mostrar la del login.

        No retorna nada.
        """
        val = messagebox.askquestion(
            title="Cierre de sesión", message="Está seguro de cerrar su sesión?")

        if val == "yes":
            self.getConexion().close()

            if isinstance(self.__frameActual, regf.RegFrame) or isinstance(self.__frameActual, mdf.modFrame):
                self.__frameActual.limpiaCampos()
            elif isinstance(self.__frameActual, laf.ListaAtencionFrame):
                self.__frameActual.limpia()
            elif isinstance(self.__frameActual, gaf.GenAtencionFrame):
                self.genAtencion = gaf.GenAtencionFrame(self)


            self.cambiaFrame(self.__frameActual, self.main)
            self.withdraw()            
            self.ventana.limpiaCampos()
            self.ventana.deiconify()

    def conecta(self, conn):
        """
        guarda el objeto Connection recibido por parámetro para poder hacer
        consultas a la base de datos.

        No retorna nada.
        """
        self.__conexion = conn

    def cambiaFrame(self, frameAnt, frameNuevo):
        """
        Cambia el frame que actualmente se está mostrando en pantalla.
        Recibe los sigueintes parámetros:
        - frameAnt, que es el frame que actualmente se muestra
        - frameNuevo, que es el frame que se quiere mostrar

        No retorna nada
        """
        self.__frameActual = frameNuevo
        frameAnt.grid_forget()
        frameNuevo.grid(row=0, column=0)

        if isinstance(frameNuevo, lpf.ListaPacFrame):
            frameNuevo.regeneraTabla()
        elif isinstance(self.__frameActual, gaf.GenAtencionFrame):
                self.genAtencion = gaf.GenAtencionFrame(self)

    def getSesion(self):
        """
        Retorna los datos no sensibles del usuario que está acutalmente conectado al sistema
        """
        return self.__sesion

    def setSesion(self, user):
        """
        Guarda los datos de sesión del usuario que se acaba de loguear.
        Además, llama al método setName del frame del menú 
        principal pasandole los datos de sesión.

        No retorna nada
        """
        self.__sesion = user
        self.main.setName(self.__sesion)

    def getConexion(self):
        """
        Retorna el objeto conection que se utiliza para conectar con la base de datos
        """
        return self.__conexion

    def avisoSalida(self):
        """
        Ventana emergente de confirmación para salir de la aplicación.

        No retorna nada.
        """
        valor = messagebox.askquestion(
            title="Salir", message="¿Esta seguro que quiere salir de la aplicación?"
        )
        if valor == "yes":
            self.__conexion.close()
            self.destroy()

    
    def avisoLicencia(self):
        """
        Ventana emergente de información indicando el estado de licencia.
        
        No retorna nada.
        """
        messagebox.showinfo(
            title="Estado de licencia", 
            message="Este software es freeware, no requiere pago"
        ) 

    def avisoAcercaDe(self):
        """
        Ventana emergente de información sobre el autor.

        No retorna nada
        """
        messagebox.showinfo(
            title="Acerca de APP", 
            message="Aplicación hecha por Sebastián Quiroga R. en Python con tkinter"
        )
