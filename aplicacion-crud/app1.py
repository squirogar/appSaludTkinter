#Aplicacion tipo CRUD
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, messagebox
import bd
import re


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
        self.title("SaludMas")
        self.protocol('WM_DELETE_WINDOW', self.avisoSalida)
        #self.resizable(False, False)
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
        self.registro = RegFrame(self)
        self.lista = ListaPacFrame(self)
        self.main = MainFrame(self)
        self.modPac = modFrame(self)
        self.listaAtencion = ListaAtencionFrame(self)
        self.genAtencion = GenAtencionFrame(self)
        

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

        if isinstance(frameNuevo, ListaPacFrame):
            frameNuevo.regeneraTabla()
        elif isinstance(frameNuevo, ListaAtencionFrame):
            frameNuevo.destruyeTabla()

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


class ImgFrame(tk.Frame):
    """
    Clase que representa a un subframe con el siguiente contenido:
    1. Un título y
    2. una imagen
    Este subframe se debe mostrar sobre otro frame.
    """
    def __init__(self, frame, img, subsample, texto):
        """
        Constructor
        - frame: frame que actuará como contenedor de este subframe
        - img: imagen a proporcionar
        - subsample: escala de reducción de imagen
        - texto: título
        """
        super().__init__(frame)

        self.__imgRecortada = img.subsample(subsample)
        tk.Label(self, text=texto, fg="#205375", font=("Arial",20,"bold")).grid(row=0, column=0)
        tk.Label(self, image=self.__imgRecortada).grid(row=1, column=0)



class DatosPacienteFrame(tk.Frame):
    """
    Clase para el procesamiento de los datos de un paciente.
    Esta clase contiene todos los campos que tiene un paciente en la base de datos
    como entry, excepto la prevision que es un IntVar. 
    Además, proporciona métodos para validar estos campos antes de que sean ingresados 
    a la base de datos.
    """
    def __init__(self, root):
        super().__init__(root)
        
        # subframe de datos en donde van los widgets
        self.datosFrame = tk.Frame(self)

        # Campos de paciente
        self._labelRut = tk.Label(self.datosFrame, text="Rut")
        self._rut = tk.Entry(self.datosFrame)
        
        self._labelNombre = tk.Label(self.datosFrame, text="Nombre")
        self._nombre = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaStr), "%P") 
        )
        
        self._labelApellido = tk.Label(self.datosFrame, text="Apellido")
        self._apellido = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaStr), "%P") 
        )
        
        self._labelDireccion = tk.Label(self.datosFrame, text="Dirección")
        self._direccion = tk.Entry(self.datosFrame)
        
        self._labelFechaNac = tk.Label(
            self.datosFrame, text="Fecha de nacimiento\n(DD-MM-AAAA)"
        )
        self._fecha_nac = tk.Entry(self.datosFrame)
        
        self._labelEmail = tk.Label(self.datosFrame, text="E-mail")
        self._email = tk.Entry(self.datosFrame)
        
        self._labelTel = tk.Label(self.datosFrame, text="Teléfono")
        self._telefono = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaNum), "%P") 
        )
        
        self._labelPrev = tk.Label(self.datosFrame, text="Previsión:")
        self._prevision = tk.IntVar()
        self._prevR1 = tk.Radiobutton(
            self.datosFrame, text="FONASA", variable=self._prevision, value=1
        )
        self._prevR2 = tk.Radiobutton(
            self.datosFrame, text="ISAPRE", variable=self._prevision, value=2
        )

    def _limpiaCampos(self):
        """
        Borra cualquier valor establecido en los campos de paciente.

        No retorna nada.
        """
        listaCampos = [
        self._rut, self._nombre, self._apellido, self._direccion, self._fecha_nac, 
        self._email, self._telefono
        ]

        for l in listaCampos:
            l.delete(0, tk.END)
        self._prevision.set(0)
    
    def _camposNulos(self):
        """
        Comprueba si existen campos nulos en los campos del paciente.
        
        En el caso que hayan campos nulos, retorna True. Caso contrario
        retorna False.
        """
        listaCampos = [
        self._rut, self._nombre, self._apellido, self._direccion, self._fecha_nac, 
        self._email, self._telefono
        ]
        for l in listaCampos:
            if l.get() == "":
                return True
        if self._prevision.get() == 0:
            return True

        print("No hay campos nulos")
        return False

    def _validaFecha(self):
        """
        Comprueba que la fecha ingresada por el usuario está en el formato
        adecuado: DD-MM-AAAA.

        Retorna True, si la fecha sigue el formato. Caso contrario, retorna
        False.
        """
        if re.fullmatch(
            r"((^0?[1-9])|(^[12]\d)|(^3[01]))-((0?[1-9])|(1[0-2]))-((19\d\d$)|(2[01]\d\d$))", 
            self._fecha_nac.get()
        ):
            print("true fecha")
            return True
        return False

    def _validaStr(self, val):
        """
        Comprueba que solo se puedan poner caracteres alfabéticos en el entry.

        Retorna True si el valor a poner en el entry es alfabético. Caso contrario,
        retorna False.
        """
        # Esto es para que el Entry quede vacío cuando se aprieta el boton "limpiacampos"
        if val == "":
            return True

        nval = "".join(val.split(" "))
        print(nval.isalpha())
        return nval.isalpha()
    
    def _validaNum(self, val):
        """
        Comprueba que solo se puedan poner caracteres numéricos en el entry.

        Retorna True si el valor a poner en el entry es numérico. Caso contrario,
        retorna False.
        """
        # Esto es para que el Entry quede vacío cuando se aprieta el boton "limpiacampos"
        if val == "":
            return True

        return val.isdigit()

    def _validaRut(self):
        """
        Comprueba que el rut ingresado por el usuario está en el formato
        adecuado: {10 digitos}-{digito verificador}.

        Retorna True, si el rut sigue el formato. Caso contrario, retorna
        False.
        """
        match = re.fullmatch(r"^\d{8}-[\dk]$", self._rut.get())
        if match:
            print("true rut")
            return True
        return False

    def _validaEmail(self):
        """
        Comprueba que el email ingresado por el usuario está en el formato
        adecuado.

        Retorna True, si el email sigue el formato. Caso contrario, retorna
        False.
        """
        match = re.fullmatch(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
            self._email.get()
        )
        if match:
            print("true email")
            return True
        return False


class RegFrame(DatosPacienteFrame):
    """
    Clase que representa un registro de pacientes.
    Extiende de DatosPacienteFrame para validar los valores que vaya ingresando
    el usuario durante el registro antes de ponerlos en la base de datos.
    """

    #You cannot use both pack and grid on widgets that have the same master
    def __init__(self, root):
        super().__init__(root)
        self.__img = ImgFrame(self, tk.PhotoImage(file="./img/reg.png"), 5, "Registro de Paciente")        

        # botones
        botonC = tk.Button(
            self, text="Cancelar", bg="white", fg="#205375", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.main)
        )
        
        botonRe = tk.Button(
            self, text="Registrar", bg="#205375", fg="white", font=("Arial"), 
            command=self.__registrarPac
        )
        
        botonL = tk.Button(
            self, text="Limpiar campos", fg="white", bg="#48a8e8", font=("Arial"), 
            command=self._limpiaCampos
        )
        

        # desplegamos los widgets dentro del frame principal
        self.__img.grid(row=0, columnspan=2)
        self.datosFrame.grid(row=1, columnspan=2, pady=10)
        botonL.grid(row=2, columnspan=2)
        botonC.grid(row=3, column=0, pady=10)
        botonRe.grid(row=3, column=1)


        # desplegamos los widgets que están dentro del subframe datosFrame
        self._labelRut.grid(row=0, column=0)
        self._rut.grid(row=0, column=1, padx=10, pady=5)
        self._labelNombre.grid(row=1, column=0)
        self._nombre.grid(row=1, column=1, pady=5)
        self._apellido.grid(row=2, column=1, pady=5)
        self._labelApellido.grid(row=2, column=0)
        self._labelDireccion.grid(row=3, column=0)
        self._direccion.grid(row=3, column=1, pady=5)
        self._labelFechaNac.grid(row=4, column=0)
        self._fecha_nac.grid(row=4, column=1, pady=5)
        self._labelEmail.grid(row=5, column=0)
        self._email.grid(row=5, column=1, pady=5)
        self._labelTel.grid(row=6, column=0)
        self._telefono.grid(row=6, column=1, pady=5)
        self._labelPrev.grid(row=7, column=0)
        self._prevR1.grid(row=8, column=1, sticky="w")
        self._prevR2.grid(row=9, column=1, sticky="w")
        

    
    def __registrarPac(self):
        """
        Registra el paciente dentro de la base de datos. 
        Realiza el siguiente procedimiento:
        1. comprueba que no hayan campos sin completar
        2. valida los valores de dichos campos
        3. envía todos los valores de los campos concretando el registro.

        No retorna nada.
        """
        
        if not self._camposNulos() and self._validaRut() and self._validaEmail() and self._validaFecha():
            root = self.nametowidget(self.winfo_parent())
            
            # insertamos el paciente
            exito = bd.insertaPaciente(
                root.getConexion(), (
                    self._rut.get(), self._nombre.get(), self._apellido.get(), 
                    self._direccion.get(), self._fecha_nac.get(), self._email.get(), 
                    self._telefono.get(), self._prevision.get()
                )
            )
            if exito:
                self._limpiaCampos()
                messagebox.showinfo(
                    title="Registro de paciente", 
                    message="El paciente ha sido registrado con éxito"
                )
            else:
                messagebox.showerror(
                    title="Error de registro", 
                    message=(
                        "Hubo un error al registrar el paciente en la base de datos. "
                        "Verifique que los datos estén bien escritos."
                    )
                )
        else:
            messagebox.showerror(
                title="Error de registro", 
                message=(
                "No se puede registrar paciente. Por favor revise si hay campos vacíos o si " 
                "los valores ingresados siguen el formato."
                )
            )


class modFrame(DatosPacienteFrame):
    """
    Clase que representa un frame que procesa la información de un paciente.
    En este frame se puede:
    - visualizar la información de un paciente
    - modificar la información de un paciente
    - eliminar un paciente de la base de datos

    Extiende de DatosPacienteFrame para validar los valores que vaya ingresando
    el usuario durante la modificación de los datos de un paciente antes de 
    ponerlos en la base de datos.
    """
    
    def __init__(self, root):
        super().__init__(root)

        self.__img = ImgFrame(
            self, tk.PhotoImage(file="./img/mod.png"), 10, 
            "Modificar información de un paciente"
        )

        labelR = tk.Label(
            self, text="Introduzca el rut del paciente:", font=("Arial", 12)
        )
        busqueda = tk.Entry(self)
        botonBusq = tk.Button(
            self, text="Buscar", command=lambda:self.muestraDatosPac(busqueda.get()), bg="#48a8e8", fg="white"
        )
        

        # botones
        frameBotones = tk.Frame(self)
        botonC = tk.Button(
            frameBotones, text="Cancelar",  bg="white", fg="#205375", font=("Arial"),
            command=lambda:root.cambiaFrame(self, root.main)
        )
        
        botonM = tk.Button(
            frameBotones, text="Modificar", bg="#205375", fg="white", font=("Arial"),
            command=self.__avisoModPac 
        )

        botonE = tk.Button(
            frameBotones, text="Eliminar", fg = "white", bg="red", font=("Arial"),
            command=self.__avisoEliminarPac
        )

        
        # desplegamos los widgets dentro del frame principal
        self.__img.grid(row=0, columnspan=2)
        labelR.grid(row=1, columnspan=2, pady=10)
        busqueda.grid(row=2, columnspan=2, pady=5)
        botonBusq.grid(row=3, columnspan=2)
        self.datosFrame.grid(row=4, columnspan=2, pady=10)

        frameBotones.grid(row=5, columnspan=2, pady=5)
        botonC.grid(row=0, column=0, padx=5)
        botonM.grid(row=0, column=1, padx=5)
        botonE.grid(row=0, column=2)
        
        
        # desplegamos los widgets que están dentro del subframe datosFrame
        self._labelRut.grid(row=0, column=0)
        self._rut.grid(row=0, column=1, padx=10, pady=5)
        self._labelNombre.grid(row=1, column=0)
        self._nombre.grid(row=1, column=1, pady=5)
        self._apellido.grid(row=2, column=1, pady=5)
        self._labelApellido.grid(row=2, column=0)
        self._labelDireccion.grid(row=3, column=0)
        self._direccion.grid(row=3, column=1, pady=5)
        self._labelFechaNac.grid(row=4, column=0)
        self._fecha_nac.grid(row=4, column=1, pady=5)
        self._labelEmail.grid(row=5, column=0)
        self._email.grid(row=5, column=1, pady=5)
        self._labelTel.grid(row=6, column=0)
        self._telefono.grid(row=6, column=1, pady=5)
        self._labelPrev.grid(row=7, column=0)
        self._prevR1.grid(row=8, column=1, sticky="w")
        self._prevR2.grid(row=9, column=1, sticky="w")

        

    def muestraDatosPac(self, rut):
        """
        Muestra por pantalla los datos del paciente recuperados de 
        la base de datos en forma de entry y radio button
        """
        self._limpiaCampos()
        root = self.nametowidget(self.winfo_parent())
        data = bd.leeDatosPacientes(root.getConexion(), rut)
        if data != []:
            self._rut.config(state=tk.NORMAL)
            self._rut.insert(0, data[0][0])
            self._rut.config(state=tk.DISABLED)
            self._nombre.insert(0, data[0][1])
            self._apellido.insert(0, data[0][2])
            self._direccion.insert(0, data[0][3])
            self._fecha_nac.insert(0, data[0][4])
            self._email.insert(0, data[0][5])
            self._telefono.insert(0, data[0][6])
            self._prevision.set(data[0][7])
        else:
            messagebox.showerror(
                title="Error", 
                message="No se ha encontrado un paciente con ese rut"
            )

    def _limpiaCampos(self):
        """
        Deja vacío los entry que se muestran en el frame. 
        Este método sobreescribe al _limpiaCampos original
        
        No retorna nada
        """
        self._rut.config(state=tk.NORMAL)
        super()._limpiaCampos()


    def __avisoModPac(self):
        if self._rut.get() == "":
            messagebox.showerror(
                title="Error", 
                message="Introduzca el rut del paciente en el cuadro de búsqueda"
            )
            return

        val = messagebox.askyesno(
            title="Modificar Paciente", 
            message=(
                "¿Está seguro de modificar los datos de este paciente? "
                "Esta acción no puede deshacerse."
            )
        )
        rut = self._rut.get()
        print(rut)


        if val:
            if not self._camposNulos() and self._validaRut() and self._validaEmail() and self._validaFecha():
                root = self.nametowidget(self.winfo_parent())
                exito = bd.actualizaDatosPaciente(
                    root.getConexion(), 
                    (
                        self._rut.get(), self._nombre.get(), self._apellido.get(), 
                        self._direccion.get(), self._fecha_nac.get(), self._email.get(), 
                        self._telefono.get(), self._prevision.get()
                    )
                )
                if exito:
                    messagebox.showinfo(
                        title="Eliminación", 
                        message="Paciente actualizado exitosamente"
                    )
                    self._limpiaCampos()
                else:
                    messagebox.showerror(
                        title="Error", 
                        message=(
                            "Ha ocurrido un error al eliminar el paciente"
                            " de la base de datos"
                        )
                    )
            else:
                messagebox.showerror(
                    title="Error de actualización", 
                    message=(
                    "No se puede actualizar la información del paciente. Por favor revise si hay campos vacíos o si " 
                    "los valores ingresados siguen el formato."
                    )
                )




    def __avisoEliminarPac(self):
        """
        Elimina un paciente de la base de datos. La elimimación la hace en base al rut.

        No retorna nada
        """
        val = messagebox.askyesno(
            title="Eliminar Paciente", 
            message="¿Está seguro de eliminar este paciente? Esta acción no puede deshacerse."
        )
        rut = self._rut.get()
        print(rut)
        if val:
            if rut != "":
                root = self.nametowidget(self.winfo_parent())
                exito = bd.borraPaciente(root.getConexion(), rut)
                if exito:
                    messagebox.showinfo(
                        title="Eliminación", message="Paciente eliminado exitosamente"
                    )
                    self._limpiaCampos()
                else:
                    messagebox.showerror(
                        title="Error", 
                        message="Ha ocurrido un error al eliminar el paciente de la base de datos"
                    )
            else:
                messagebox.showerror(
                    title="Error", message="Introduzca el rut del paciente en el cuadro de búsqueda")




class ListaPacFrame(tk.Frame):
    """
    Clase que muestra los pacientes registrados en la base de datos.
    En su interior se encuentra un subframe del tipo TablaFrame
    en el que se muestran la lista de pacientes registrados.
    """
    def __init__(self, root):
        super().__init__(root)
        
        self.__img = ImgFrame(
            self, tk.PhotoImage(file="./img/list.png"), 7, "Pacientes registrados"
        )
        
        self.__frameTabla = tk.Frame(self)

        botonV = tk.Button(
            self, text="Volver", bg="white", fg="#205375", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.main)
        )
        
        self.__img.grid(row=0, columnspan=8)
        botonV.grid(row=1, column=0, pady=10)
        self.__frameTabla.grid(row=2, columnspan=8, pady=10)

    def __creaTabla(self, data):
        """
        retorna un subframe del tipo TablaFrame con los datos proporcionados.
        """
        nombreColumnas = (
            "Rut paciente", "Nombre", "Apellido", "Dirección", "Fecha nacimiento",
            "E-mail", "Teléfono", "Previsión"
        )
        tabla = TablaFrame(self, data, nombreColumnas)
        return tabla
    
    def regeneraTabla(self):
        """
        Destruye el subframe que contiene la tabla de datos, generando
        uno nuevo y mostrándolo en pantalla.

        No retorna nada
        """
        # se destruye el subframe
        self.__frameTabla.destroy()

        # creamos un nuevo subframe con la data correspondiente
        root = self.nametowidget(self.winfo_parent())
        rec = bd.leeDatosPacientes(root.getConexion())
        rec = [list(x) for x in rec]
        data = []
        for x in rec:
            x.pop(7) # eliminamos el id de la prevision porque no nos sirve
            data.append(x)
        self.__frameTabla = self.__creaTabla(data)

        # mostramos en pantalla el nuevo subframe
        self.__frameTabla.grid(row=2, column=0, pady=10, padx = 10)




class ListaAtencionFrame(tk.Frame):
    """
    Clase que muestra las atenciones realizadas a un paciente dado su rut
    En su interior se encuentra un subframe de la clase TablaFrame que
    muestra las atenciones efectuadas para dicho paciente.

    """
    def __init__(self, root):
        super().__init__(root)


        self.__img = ImgFrame(
            self, tk.PhotoImage(file="./img/list.png"), 7, "Atenciones de paciente"
        )
        
        labelR = tk.Label(
            self, text="Introduzca el rut del paciente:", font=("Arial", 12)
        )
        busqueda = tk.Entry(self)
        botonBusq = tk.Button(
            self, text="Buscar", command=lambda:self.muestraAtencionPac(busqueda.get()), fg="white", bg="#48a8e8"
        )

        self.__frameTabla = tk.Frame(self)

        botonV = tk.Button(
            self, text="Volver", bg="white", fg="#205375", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.main)
        )
        
        self.__img.grid(row=0, columnspan=2)
        botonV.grid(row=1, column=0, pady=10)
        labelR.grid(row=2, columnspan=2, pady=10)
        busqueda.grid(row=3, columnspan=2, pady=10)
        botonBusq.grid(row=4, columnspan=2, pady=10)
        self.__frameTabla.grid(row=5, column=0, pady=10)

    def muestraAtencionPac(self, rut):
        """
        Muestra en pantalla las atenciones pertenecientes
        a un paciente determinado dado su rut.
        Recibe como parámetro:
        - rut: rut del paciente
        """
        # destruimos el subframe anterior
        self.destruyeTabla()

        # creamos un nuevo subframe en el que se mostrarán
        # los datos
        root = self.nametowidget(self.winfo_parent())
        data = bd.leeDatosAtencion(root.getConexion(), rut)
        if data != []:
            nombreColumnas = (
                "Número atencion", "Fecha de atención", "Tipo de servicio", 
                "Nombre Médico Trat.", "Especialidad Médico",
                "Rut paciente", "Usuario registrador", "Monto Total"
            )
            self.__frameTabla = TablaFrame(self, data, nombreColumnas)
            self.__frameTabla.grid(row=5, column=0, pady=10)
        else:
            messagebox.showerror(
                title="Error en consulta de atenciones",
                message="El rut consultado no cuenta con atenciones."
            )

    def destruyeTabla(self):
        """
        Destruye el subframe que muestra las atenciones del
        paciente consultado.
        """
        self.__frameTabla.destroy()



class CompraExamenFrame(tk.Frame):
    def __init__(self, contenedor, data):
        super().__init__(contenedor)

        self.destruido = False
        
        # obtenemos la data de los examenes que nos sirve
        self.__dic = dict()
        for reg in data:
            self.__dic[reg[1]] = reg[4]

        listNombres = list(self.__dic.keys())

        # widgets
        labelExamen = tk.Label(self, text="Examen")
        self.__combo = ttk.Combobox(self, values=listNombres, state="readonly")
        self.__combo.bind("<<ComboboxSelected>>", self.__setValor)
        self.__valor = tk.Label(self, text="Valor: ")
        labelCant = tk.Label(self, text="Cantidad")
        self.__cant = tk.Entry(
            self, validate="key", 
            validatecommand=(self.register(self.__validaNum), "%P") 
        )
        botonCancel = tk.Button(self, text="Cancelar", command=self.__cancelaCompra, bg="red", fg="white")        
        separator = ttk.Separator(master=self, orient="horizontal")

        # grid
        labelExamen.grid(row=0, column=0, pady=5)
        self.__combo.grid(row=1, column=0)
        self.__valor.grid(row=2, column=0, pady=5)
        labelCant.grid(row=4, column=0, pady=5)
        self.__cant.grid(row=5, column=0)
        botonCancel.grid(row=6, column=0, pady=5)
        separator.grid(row=7, columnspan=1, sticky="we", pady=5)


    def getValues(self):
        """
        Devuelve una tupla con los valores de los widgets del frame:
        (examen, valor, cantidad) 
        """
        return (self.__combo.get(), self.__valor["text"][1:], self.__cant.get())
    
    def camposVacios(self):
        """
        Retorna True si hay campos de este subframe vacíos. Caso contrario,
        retorna False.
        """
        if self.__combo.get() == "" or self.__cant.get() == "":
            return True
        return False

    def __setValor(self, evento):
        """
        Se llama cuando se selecciona un examen de la lista de examenes.
        Muestra el valor del examen como widget en pantalla.
        """
        nombreExamen = self.__combo.get()
        valor = self.__dic[nombreExamen]
        self.__valor.config(text=f"${str(int(valor))}")
    
    def __cancelaCompra(self):
        """
        Destruye este subframe.

        No retorna nada.
        """
        self.destroy()
        self.destruido = True

    def __validaNum(self, val):
        """
        Comprueba que solo se puedan poner caracteres numéricos mayores que 0 en el entry.

        Retorna True si el valor a poner en el entry es numérico mayor a 0
        En caso contrario, retorna False.
        """
        if val == 0:
            return False
        return val.isdigit()



class GenAtencionFrame(tk.Frame):
    """
    Clase que representa un frame para generar una atención médica a un paciente.
    En una atención médica se registran datos relacionados a la compra
    de examenes que quiere hacer un paciente. Para ello se debe indicar:

    - rut paciente
    - tipo de servicio
    - nombre del médico que ordenó la compra de examenes
    - especialidad del médico

    Cada compra de un examen que se realice se debe especificar:
    - nombre de examen
    - valor unitario de examen
    - cantidad
    
    El paciente debe estar registrado en el sistema previamente.
    """

    def __init__(self, root):
        super().__init__(root)

        self.__frameScrolleable = FrameScrolleable(self, vertical=True, ancho="250", alto="450")

        # widgets
        self.__img = ImgFrame(self.__frameScrolleable.getFrame(), tk.PhotoImage(file="./img/cross.png"), 10, "Generar atención")
        labelRut = tk.Label(self.__frameScrolleable.getFrame(), text="Rut paciente")
        self.__rut = tk.Entry(self.__frameScrolleable.getFrame())
        labelTipo = tk.Label(self.__frameScrolleable.getFrame(), text="Tipo de servicio")
        self.__tipoServ = tk.Entry(self.__frameScrolleable.getFrame())
        labelMed = tk.Label(self.__frameScrolleable.getFrame(), text="Nombre médico tratante")
        self.__med = tk.Entry(self.__frameScrolleable.getFrame())
        labelEspMed = tk.Label(self.__frameScrolleable.getFrame(), text="Especialidad médico tratante")
        self.__espMed = tk.Entry(self.__frameScrolleable.getFrame())
        separator1 = ttk.Separator(self.__frameScrolleable.getFrame(), orient="horizontal")
        
        self.__fila = 10 # desde esta fila empieza a comprarse los examenes
        self.__frameBotones = tk.Frame(self.__frameScrolleable.getFrame())
        self.__botonMas = tk.Button(
            self.__frameBotones, text="+", command=self.__agregaCompraFrame, bg="blue", fg="white", padx=5
        )
        self.__botonTerminar = tk.Button(
            self.__frameBotones, text="Terminar compra", command=self.__terminaCompra, bg="#48a8e8", fg="white"
        )
        botonCancelar = tk.Button(
            self.__frameBotones, text="Cancelar", command=self.__limpiaYCambia, bg="white", fg="#205375"
        )
        botonRA = tk.Button(
            self.__frameBotones, text="Registrar atención", command=self.__registrarAtencion,  fg="white", bg="#205375"
        )
        
        # lista de subframes de compra examen
        # se mostrarán desde fila = 10
        self.__listaSubFrames = []

        # mostrará la compra realizada durande la atención
        self.__compra = tk.Label(self.__frameScrolleable.getFrame())
        
        # contendrá la lista de examenes comprados
        self.__listaExamenesComprados = []

        # total de la compra de examenes
        self.__total = 0

        # compra terminada
        self.__compraTerminada = False

        # grid
        self.__frameScrolleable.grid(row=0, column=0)

        self.__img.grid(row=0, column=0)
        labelRut.grid(row=1, column=0)
        self.__rut.grid(row=2, column=0, pady=5)
        labelTipo.grid(row=3, column=0)
        self.__tipoServ.grid(row=4, column=0, pady=5)
        labelMed.grid(row=5, column=0)
        self.__med.grid(row=6, column=0, pady=5)
        labelEspMed.grid(row=7, column=0)
        self.__espMed.grid(row=8, column=0, pady=5)
        #separator1.grid(row=9, columnspan=1, sticky="we")

        # ...aqui deberian ir los subframes de compra de examenes...

        self.__frameBotones.grid(row=100, column=0, pady=5)
        self.__botonMas.grid(row=0, columnspan=2, pady=5)
        self.__botonTerminar.grid(row=1, columnspan=2, pady=5)
        botonCancelar.grid(row=2, column=0)
        botonRA.grid(row=2, column=1)


    def __agregaCompraFrame(self):
        """
        Agrega un nuevo subframe al frame principal.
        Este nuevo subframe sirve para comprar un nuevo examen.

        No retorna nada.
        """
        root = self.nametowidget(self.winfo_parent())
        frame = CompraExamenFrame(self.__frameScrolleable.getFrame(), bd.leeDatosExamen(root.getConexion()))
        frame.grid(row=self.__fila, column=0)
        self.__listaSubFrames.append(frame)
        self.__fila += 1

    def __terminaCompra(self):
        """
        Finaliza la compra de examenes que conforman una atención médica.
        Para ello, se realizan los siguientes procedimientos:
        - Se verifican que no hayan compras incompletas
        - Se guardan los valores de la compra
        - Se muestra la compra por pantalla

        No retorna nada.
        """
        # recorrer la lista de subframes
        # para comprobar que no hayan campos vacios
        val = self.__compraIncompleta()
        if val:
            messagebox.showerror(
                title="Error",
                message=(
                    "Una o más compras están vacías. " 
                    "Complételas primero y luego termine la compra."
                )
            )
            return
        
        self.__procesaExamenesComprados()

        # desactivar el boton para comprar mas examenes
        # y el boton para terminar la compra
        self.__botonMas.destroy()
        self.__botonTerminar.destroy()

        # eliminar los subframes
        self.__eliminarSubframesCompraExamen()
        
        # compra terminada
        self.__compraTerminada = True

    def __compraIncompleta(self):
        """
        Retorna True si hay compras incompletas. Caso contrario, retorna False.
        """
        self.__cleanSubframesCompra()
        if self.__listaSubFrames == []:
            return True
        for frame in self.__listaSubFrames:
            if not frame.destruido:
                if frame.camposVacios():
                    return True

        return False
    
    def __cleanSubframesCompra(self):
        for i, j in enumerate(self.__listaSubFrames):
            if self.__listaSubFrames[i].destruido:
                del self.__listaSubFrames[i]

    def __procesaExamenesComprados(self):
        """
        Guarda los valores de la compra de cada examen, calcula el total
        y muestra por pantalla la compra resultante.

        No retorna nada
        """
        compra = ""
        total = 0
        for frame in self.__listaSubFrames:
            tupla = frame.getValues()
            self.__listaExamenesComprados.append((tupla[0], float(tupla[1]), int(tupla[2])))
            compra += f"{tupla[0]} ${tupla[1]} cant: {tupla[2]}\n"
            total += float(tupla[1]) * int(tupla[2])
        
        self.__total = total
        compra += f"Total: ${self.__total}"
        self.__compra.config(text=compra)
        self.__compra.grid(row=self.__fila, column=0)


    def __eliminarSubframesCompraExamen(self):
        """
        Destruye todos los subframes mostrados por pantalla que sirvieron
        para comprar examenes. Estos subframes ya no tienen utilidad porque
        el usuario ya terminó la compra.

        No retorna nada.
        """
        for frame in self.__listaSubFrames:
            frame.destroy()
        del self.__listaSubFrames

    def __camposVacios(self):
        """
        Retorna True si hay algún campo del formulario vacío.
        Caso contrario, retorna False.
        """
        if self.__rut.get() == "" or self.__tipoServ.get() == "" or self.__med.get() == "" or self.__espMed.get() == "":
            return True
        return False


    def __registrarAtencion(self):
        """
        Registra la atención en la base de datos. Para hacer lo anterior, comprueba
        que la compra de examenes esté terminada, que los valores de los campos del
        formulario no estén vacíos y que el paciente exista en la base de datos.

        No retorna nada. 
        """
        if not self.__compraTerminada:
            messagebox.showerror(
                title="Registrar atencion",
                message="Debe terminar la compra de examenes."
            )
        elif not self.__validaRut(self.__rut.get()):
            messagebox.showerror(
                title="Registrar atencion",
                message="El rut no sigue el formato, vuelva a escribirlo."
            )
        elif self.__camposVacios():
            messagebox.showerror(
                title="Registrar atencion",
                message="Hay campos vacios, complételos primero para realizar la operación."
            )
        else:
            value = messagebox.askyesno(
                title="Registrar atencion",
                message="Va a registrar la atención del paciente, está seguro de continuar?"
            )
            if value:
                # reunir los datos de la atencion
                root = self.nametowidget(self.winfo_parent())
                
                print(f"""tupla a enviar ({self.__tipoServ.get()},
                        {self.__med.get()},
                        {self.__espMed.get()},
                        {self.__rut.get()},
                        {root.getSesion()[0]})""")

                exito = bd.insertaAtencion(
                    root.getConexion(), 
                    (
                        self.__tipoServ.get(),
                        self.__med.get(),
                        self.__espMed.get(),
                        self.__rut.get(),
                        root.getSesion()[0]
                    )
                )

                if exito:
                    numeroAtencion = bd.leeDatosAtencion(root.getConexion(), self.__rut.get())[-1][0]
                    print("Nro atencion", numeroAtencion)
                    for examenComprado in self.__listaExamenesComprados:
                        codigo = bd.leeDatosExamen(root.getConexion(), nombre = examenComprado[0])[0][0]
                        print("codigo", codigo)
                        bd.insertaCompraExamen(
                            root.getConexion(), 
                            (numeroAtencion, codigo, int(examenComprado[2]), int(examenComprado[2]) * float(examenComprado[1]))
                        )
                    messagebox.showinfo(
                        title="Registro atencion",
                        message="Atención registrada."
                    )
                else:
                    messagebox.showerror(
                        title="Error",
                        message="Ocurrió un error al registrar la atención. Asegúrese de que el paciente está registrado."
                    )
    
    def __validaRut(self, val):
        """
        Comprueba que el rut ingresado por el usuario está en el formato
        adecuado: {10 digitos}-{digito verificador}.

        Retorna True, si el rut sigue el formato. Caso contrario, retorna
        False.
        """
        match = re.fullmatch(r"^\d{8}-[\dk]$", val)
        if match:
            print("true rut")
            return True
        return False

    def __limpiaYCambia(self):
        
        root = self.nametowidget(self.winfo_parent())
        root.cambiaFrame(self, root.main)

    def __limpiaCampos(self):
        listaCampos = [
        self.__rut, self.__tipoServ, self.__med, self.__espMed, self._fecha_nac, 
        self._email, self._telefono
        ]

        for l in listaCampos:
            l.delete(0, tk.END)


class MainFrame(tk.Frame):
    """
    Clase que representa un frame para menu principal.
    Es el punto central de la aplicación, ya que desde aquí se navegan a los
    demás frames disponibles en la aplicación.
    """
    
    def __init__(self, root):
        super().__init__(root)
        
        self.__img = ImgFrame(self, tk.PhotoImage(file="./img/cross.png"), 10, "Menú Principal")
    
        self.name = tk.Label(self, text="" , font=("Arial", 15))
        labelA = tk.Label(self, text="Acciones disponibles:", font=("Arial", 12))
        
        # botones
        botonReg = tk.Button(
            self, text="Registrar paciente", bg="#205375", fg="white", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.registro)
            )
        botonVerPac = tk.Button(
            self, text="Ver pacientes registrados", bg="#205375", fg="white", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.lista)
            )
        botonMod = tk.Button(
            self, text="Modificar información paciente", bg="#205375", fg="white", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.modPac)
            )
        botonVerAt = tk.Button(
            self, text="Ver atenciones de un paciente", bg="#205375", fg="white", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.listaAtencion)
            )
        botonGen = tk.Button(
            self, text="Generar atención", bg="#205375", fg="white", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.genAtencion)
            )
        
        
        self.__img.grid(row=0, columnspan=2)
        self.name.grid(row=1, column=0, pady=10)
        labelA.grid(row=2, column=0, pady=10)
        botonReg.grid(row=3, columnspan=2, pady=10)
        botonVerPac.grid(row=4, columnspan=2, pady=10)
        botonMod.grid(row=5, columnspan=2, pady=10, padx=20)
        botonVerAt.grid(row=6, columnspan=2, pady=10)
        botonGen.grid(row=7, columnspan=2, pady=10)
        

    def setName(self, user):
        """
        Pone en el label "name" el nombre y el apellido del usuario que 
        entró al sistema.
        """
        self.name.config(text=f"Hola, {user[1]} {user[2]}")
        
        




class Login(Toplevel):
    """
    Clase que representa la ventana de login.
    Extiende de Toplevel.
    """
    def __init__(self, root):
        super().__init__(root)
        self.protocol('WM_DELETE_WINDOW', self.avisoSalida)
        self.__img = ImgFrame(self, tk.PhotoImage(file="./img/login.png"), 5, "Autenticación")
        
        labelU = tk.Label(self, text="Usuario", font=("Arial", 12))
        self.__txtUser = tk.Entry(self)
        labelP = tk.Label(self, text="Contraseña", font=("Arial", 12))
        self.__txtPass = tk.Entry(self)
        self.__txtPass.config(show="*")
        self.__ingresar = tk.Button(
            self, text="Ingresar", 
            command=lambda:self.__validaIngreso(
                self.__txtUser.get(), self.__txtPass.get()
            )
        )
        self.__ingresar.config(bg="#205375", fg="white", font=("Arial"), padx=10)
        

        self.__img.grid(row=0, columnspan=2)
        labelU.grid(row=1, column=0, padx=10, pady=5)
        self.__txtUser.grid(row=1, column=1, padx=10)
        labelP.grid(row=2, column=0, padx=10, pady=5)
        self.__txtPass.grid(row=2, column=1)
        self.__ingresar.grid(row=3, columnspan=2, pady=20)
        

    def __validaIngreso(self, user, passwd):
        """
        Comprueba que las credenciales utilizadas por el usuario
        son correctas.
        Recibe como parámetros:
        - nombre de usuario
        - contraseña

        Este método hace lo siguiente:
        1. comprueba que se puede conectar a la base de datos
        2. valida que no hayan campos nulos
        3. cambia a la ventana de aplicación principal root
        """
        conn = bd.connectar()
        if conn is not None:
            user = bd.autenticacion(conn, (user, passwd))
            print(user)
            if user is not None:
                root = self.nametowidget(self.winfo_parent())
                root.conecta(conn)
                user = (user[0], user[2], user[3])

                root.setSesion(user)
                messagebox.showinfo(title="Autenticación", message="Bienvenido!")
                self.withdraw()
                root.deiconify()
            else:
                messagebox.showerror(
                    title="Error de autenticación", 
                    message="Rut y/o contraseña invalidos"
                )
    
    def limpiaCampos(self):
        """
        Limpia los dos entry de usuario y password

        No retorna nada
        """
        self.__txtUser.delete(0, tk.END)
        self.__txtPass.delete(0, tk.END)

    def avisoSalida(self):
        """
        Ventana emergente de confirmación de salida de la aplicación
        """
        valor = messagebox.askquestion(
            title="Salir", 
            message="¿Esta seguro que quiere salir de la aplicación?"
        )

        if valor == "yes":
            root = self.nametowidget(self.winfo_parent())
            root.destroy()


class TablaFrame(tk.Frame):
    """
    Clase que representa un subframe que contiene una tabla con datos
    que se mostrarán en pantalla.
    Este subframe debería ser contenido por otro frame.

    """
    def __init__(self, contenedor, data, nombreColumnas):
        """
        Constructor
        - contenedor: frame que actuará como contenedor de este subframe
        - data: datos en forma de lista. Si la variable data no contiene
        datos, entonces despliega un label indicando que no hay datos
        para mostrar.
        - nombreColumnas: tupla con el nombre de las columnas en donde 
        van los datos
        """
        super().__init__(contenedor)

        fila = 0
        col = 0
        if data != []:
            for columna in nombreColumnas:
                l = tk.Label(self, text=columna)
                l.grid(row=fila, column=col)
                col += 1
            col = 0
            fila += 1

            for registro in data:
                for elemento in registro:
                    e = tk.Entry(self)
                    e.insert(0, f"{elemento}")
                    e.config(state="readonly")
                    e.grid(row=fila, column=col)
                    col += 1
                col = 0
                fila += 1            
        else:
            tk.Label(self, text="No data").grid(row=0, column=0)


class FrameScrolleable(tk.Frame):
    def __init__(self, contenedor, vertical=False, horizontal=False, ancho="", alto=""):
        super().__init__(contenedor)

        self.__canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        if ancho != "":
            self.__canvas.config(width=ancho)
        if alto != "":
            self.__canvas.config(height=alto)
        self.__vscrollbar = None
        if vertical:
            self.__creaScrollVertical()
            
        self.__frameInterior = tk.Frame(self.__canvas)
        self.__canvas.create_window(0, 0, window=self.__frameInterior, anchor=tk.NW)
        self.__frameInterior.bind("<Configure>", self.__haceScroll)
        self.__canvas.grid(row=0, column=0)

    def __creaScrollVertical(self):
        self.__vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar.config(command=self.__canvas.yview)
        self.__canvas["yscrollcommand"] = self.__vscrollbar.set
        self.__vscrollbar.grid(row=0, column=1, sticky="NSW")


    def __haceScroll(self, evento):
        print(evento.width, evento.height)
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

    def getFrame(self):
        return self.__frameInterior



if __name__ == "__main__":
    app = Aplicacion() #tk
    login = Login(app) #toplevel
    app.withdraw()
    app.ventana = login

    app.mainloop()
    