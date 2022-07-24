"""
ImgFrame module

"""
import tkinter as tk

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

