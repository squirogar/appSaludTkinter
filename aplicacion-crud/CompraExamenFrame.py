"""
Frame para la compra de examenes
"""
import tkinter as tk
from tkinter import ttk



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

