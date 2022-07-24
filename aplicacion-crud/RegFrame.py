"""
Frame de registro de pacientes

"""
import DatosPacienteFrame as dpf
import ImgFrame as imgf
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import bd

class RegFrame(dpf.DatosPacienteFrame):
    """
    Clase que representa un registro de pacientes.
    Extiende de DatosPacienteFrame para validar los valores que vaya ingresando
    el usuario durante el registro antes de ponerlos en la base de datos.
    """

    #You cannot use both pack and grid on widgets that have the same master
    def __init__(self, root):
        super().__init__(root)
        self.__img = imgf.ImgFrame(self, tk.PhotoImage(file="./img/reg.png"), 5, "Registro de Paciente")        

        # botones
        botonC = tk.Button(
            self, text="Cancelar", bg="white", fg="#205375", font=("Arial"), 
            command=self.__limpiaYCambia
        )
        
        botonRe = tk.Button(
            self, text="Registrar", bg="#205375", fg="white", font=("Arial"), 
            command=self.__registrarPac
        )
        
        botonL = tk.Button(
            self, text="Limpiar campos", fg="white", bg="#48a8e8", font=("Arial"), 
            command=self.limpiaCampos
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
        
    def __limpiaYCambia(self):
        self.limpiaCampos()
        root = self.nametowidget(self.winfo_parent())
        root.cambiaFrame(self, root.main)
        
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
                self.limpiaCampos()
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
