"""
Utilidades para la aplicación:
- una frame que genera una tabla con los datos que le pasen
- un frame scrolleable

"""

import tkinter as tk
from tkinter import ttk


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
                    e.config(justify="center")
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
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

    def getFrame(self):
        return self.__frameInterior

    def setView(self):
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)