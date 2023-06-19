"""
Frame que permitira registrar un atención de un paciente que incluye la 
compra de examenes
"""
import tkinter as tk
import Utilidades 
from tkinter import ttk
import ImgFrame as imgf
from tkinter import messagebox
import bd
import re
import CompraExamenFrame as cef

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

        self.__frameScrolleable = Utilidades.FrameScrolleable(self, vertical=True, ancho="250", alto="450")

        # widgets
        self.__img = imgf.ImgFrame(self.__frameScrolleable.getFrame(), tk.PhotoImage(file="./img/cross.png"), 10, "Generar atención")
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
            self.__frameBotones, text="Cancelar", command=self.__cambia, bg="white", fg="#205375"
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
        frame = cef.CompraExamenFrame(self.__frameScrolleable.getFrame(), bd.leeDatosExamen(root.getConexion()))
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
        self.__frameScrolleable.setView()

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
                    numeroAtencion = bd.leeDatosAtencion(root.getConexion())[-1][0]
                    
                    for examenComprado in self.__listaExamenesComprados:
                        codigo = bd.leeDatosExamen(root.getConexion(), nombre = examenComprado[0])[0][0]
                        
                        bd.insertaCompraExamen(
                            root.getConexion(), 
                            (numeroAtencion, codigo, int(examenComprado[2]), int(examenComprado[2]) * float(examenComprado[1]))
                        )
                    messagebox.showinfo(
                        title="Registro atencion",
                        message="Atención registrada."
                    )
                    self.__cambia()
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
            return True
        
        return False

    def __cambia(self):
        
        root = self.nametowidget(self.winfo_parent())
        root.cambiaFrame(self, root.main)


