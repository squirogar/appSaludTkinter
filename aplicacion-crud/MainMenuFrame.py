"""
Frame que muestra el menu principal de opciones

"""
import tkinter as tk
import ImgFrame as imgf

class MainFrame(tk.Frame):
    """
    Clase que representa un frame para menu principal.
    Es el punto central de la aplicación, ya que desde aquí se navegan a los
    demás frames disponibles en la aplicación.
    """
    
    def __init__(self, root):
        super().__init__(root)
        
        self.__img = imgf.ImgFrame(self, tk.PhotoImage(file="./img/cross.png"), 10, "Menú Principal")
    
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
        
        