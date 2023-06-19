"""
Ventana de login
"""
import tkinter as tk
from tkinter import messagebox
import bd
import ImgFrame as imgfr

class Login(tk.Toplevel):
    """
    Clase que representa la ventana de login.
    Extiende de Toplevel.
    """
    def __init__(self, root):
        super().__init__(root)
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.avisoSalida)
        self.__img = imgfr.ImgFrame(self, tk.PhotoImage(file="./img/login.png"), 5, "Autenticación")
        
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

