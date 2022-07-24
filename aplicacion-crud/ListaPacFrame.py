"""
Frame que muestra la lista de pacientes registrados

"""
import tkinter as tk
import ImgFrame as imgf
import bd
import Utilidades

class ListaPacFrame(tk.Frame):
    """
    Clase que muestra los pacientes registrados en la base de datos.
    En su interior se encuentra un subframe del tipo TablaFrame
    en el que se muestran la lista de pacientes registrados.
    """
    def __init__(self, root):
        super().__init__(root)
        
        self.__img = imgf.ImgFrame(
            self, tk.PhotoImage(file="./img/list.png"), 7, "Pacientes registrados"
        )
        
        self.__frameScrolleable = Utilidades.FrameScrolleable(self)

        botonV = tk.Button(
            self, text="Volver", bg="white", fg="#205375", font=("Arial"), 
            command=lambda:root.cambiaFrame(self, root.main)
        )
        
        
        self.__img.grid(row=0, columnspan=8)
        botonV.grid(row=1, column=0, pady=10)

    def __creaTabla(self, contenedor, data):
        """
        retorna un subframe del tipo TablaFrame con los datos proporcionados.
        """
        nombreColumnas = (
            "Rut paciente", "Nombre", "Apellido", "Dirección", "Fecha nacimiento",
            "E-mail", "Teléfono", "Previsión"
        )
        tabla = Utilidades.TablaFrame(contenedor, data, nombreColumnas)
        return tabla
    
    def regeneraTabla(self):
        """
        Destruye el subframe que contiene la tabla de datos, generando
        uno nuevo y mostrándolo en pantalla.

        No retorna nada
        """
        # se destruye el subframe
        self.__frameScrolleable.destroy()
        self.__frameScrolleable = Utilidades.FrameScrolleable(self, vertical=True, ancho="990", alto="300")
        # creamos un nuevo subframe con la data correspondiente
        root = self.nametowidget(self.winfo_parent())
        rec = bd.leeDatosPacientes(root.getConexion())
        rec = [list(x) for x in rec]
        data = []
        for x in rec:
            x.pop(7) # eliminamos el id de la prevision porque no nos sirve
            data.append(x)
        self.__frameTabla = self.__creaTabla(self.__frameScrolleable.getFrame(), data)

        # mostramos en pantalla el nuevo subframe
        self.__frameTabla.grid(row=0, column=0, pady=10, padx = 10)
        self.__frameScrolleable.grid(row=2, columnspan=8)

