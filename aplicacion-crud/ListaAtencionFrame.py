"""
Frame que muestra todas las atenciones de un paciente

"""

import tkinter as tk
import ImgFrame as imgf
import Utilidades
from tkinter import messagebox
import bd

class ListaAtencionFrame(tk.Frame):
    """
    Clase que muestra las atenciones realizadas a un paciente dado su rut
    En su interior se encuentra un subframe de la clase TablaFrame que
    muestra las atenciones efectuadas para dicho paciente.

    """
    def __init__(self, root):
        super().__init__(root)


        self.__img = imgf.ImgFrame(
            self, tk.PhotoImage(file="./img/list.png"), 7, "Atenciones de paciente"
        )
        
        labelR = tk.Label(
            self, text="Introduzca el rut del paciente:", font=("Arial", 12)
        )
        self.__busqueda = tk.Entry(self)
        botonBusq = tk.Button(
            self, text="Buscar", command=lambda:self.muestraAtencionPac(self.__busqueda.get()), fg="white", bg="#48a8e8"
        )


        self.__frameScrolleable = Utilidades.FrameScrolleable(self)

        botonV = tk.Button(
            self, text="Volver", bg="white", fg="#205375", font=("Arial"), 
            command=self.__limpiaYCambia
        )
        
        self.__img.grid(row=0, columnspan=2)
        botonV.grid(row=1, column=0, pady=10)
        labelR.grid(row=2, columnspan=2, pady=10)
        self.__busqueda.grid(row=3, columnspan=2, pady=10)
        botonBusq.grid(row=4, columnspan=2, pady=10)
    
    def muestraAtencionPac(self, rut):
        """
        Muestra en pantalla las atenciones pertenecientes
        a un paciente determinado dado su rut.
        Recibe como parámetro:
        - rut: rut del paciente
        """
        # destruimos el subframe anterior, por si se aprieta varias veces
        # buscar
        self.__destruyeTabla()
        # creamos un nuevo subframe en el que se mostrarán
        # los datos
        root = self.nametowidget(self.winfo_parent())
        data = bd.leeDatosAtencionPaciente(root.getConexion(), rut)
        if data != []:
            nombreColumnas = (
                "Número atencion", "Fecha de atención", "Tipo de servicio", 
                "Nombre Médico Trat.", "Especialidad Médico",
                "Rut paciente", "Usuario registrador", "Monto Total"
            )
            self.__frameScrolleable = Utilidades.FrameScrolleable(self, vertical=True, ancho="990", alto="300")
            self.__frameScrolleable.grid(row=5, column=0)
            self.__frameTabla = Utilidades.TablaFrame(
                self.__frameScrolleable.getFrame(), data, nombreColumnas
            )
            self.__frameTabla.grid(row=0, column=0, pady=10)
        else:
            messagebox.showerror(
                title="Error en consulta de atenciones",
                message="El rut consultado no cuenta con atenciones."
            )

    def __destruyeTabla(self):
        """
        Destruye el subframe que muestra las atenciones del
        paciente consultado.
        """
        self.__frameScrolleable.destroy()

    def limpia(self):
        """
        Limpia los campos y destruye la tabla con las atenciones del paciente
        """
        self.__busqueda.delete(0, tk.END)
        self.__destruyeTabla()

    def __limpiaYCambia(self):
        print("llama")
        self.limpia()
        root = self.nametowidget(self.winfo_parent())
        root.cambiaFrame(self, root.main)

