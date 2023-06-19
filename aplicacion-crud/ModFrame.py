"""
Frame de modificación de pacientes médicos


"""
import DatosPacienteFrame as dpf
import ImgFrame as imgf
import bd
import tkinter as tk
from tkinter import messagebox

class modFrame(dpf.DatosPacienteFrame):
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

        self.__img = imgf.ImgFrame(
            self, tk.PhotoImage(file="./img/mod.png"), 10, 
            "Modificar información de un paciente"
        )

        labelR = tk.Label(
            self, text="Introduzca el rut del paciente:", font=("Arial", 12)
        )
        self.__busqueda = tk.Entry(self)
        botonBusq = tk.Button(
            self, text="Buscar", command=lambda:self.muestraDatosPac(self.__busqueda.get()), bg="#48a8e8", fg="white"
        )
        

        # botones
        frameBotones = tk.Frame(self)
        botonC = tk.Button(
            frameBotones, text="Cancelar",  bg="white", fg="#205375", font=("Arial"),
            command=self.__limpiaYCambia
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
        self.__busqueda.grid(row=2, columnspan=2, pady=5)
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
        self.limpiaCampos()
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
    
    def __limpiaYCambia(self):
        self.limpiaCampos()
        root = self.nametowidget(self.winfo_parent())
        root.cambiaFrame(self, root.main)

    def limpiaCampos(self):
        """
        Deja vacío los entry que se muestran en el frame. 
        Este método sobreescribe al _limpiaCampos original
        
        No retorna nada
        """
        self.__busqueda.delete(0, tk.END)
        self._rut.config(state=tk.NORMAL)
        super().limpiaCampos()


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
                    self.limpiaCampos()
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
        
        if val:
            if rut != "":
                root = self.nametowidget(self.winfo_parent())
                exito = bd.borraPaciente(root.getConexion(), rut)
                if exito:
                    messagebox.showinfo(
                        title="Eliminación", message="Paciente eliminado exitosamente"
                    )
                    self.limpiaCampos()
                else:
                    messagebox.showerror(
                        title="Error", 
                        message="Ha ocurrido un error al eliminar el paciente de la base de datos"
                    )
            else:
                messagebox.showerror(
                    title="Error", message="Introduzca el rut del paciente en el cuadro de búsqueda")

