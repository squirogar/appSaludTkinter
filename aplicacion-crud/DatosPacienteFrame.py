"""
Frame que proporciona métodos y widgets para mostrar y procesar
datos de un paciente médico.

"""
import tkinter as tk
import re

class DatosPacienteFrame(tk.Frame):
    """
    Clase para el procesamiento de los datos de un paciente.
    Esta clase contiene todos los campos que tiene un paciente en la base de datos
    como entry, excepto la prevision que es un IntVar. 
    Además, proporciona métodos para validar estos campos antes de que sean ingresados 
    a la base de datos.
    """
    def __init__(self, root):
        super().__init__(root)
        
        # subframe de datos en donde van los widgets
        self.datosFrame = tk.Frame(self)

        # Campos de paciente
        self._labelRut = tk.Label(self.datosFrame, text="Rut")
        self._rut = tk.Entry(self.datosFrame)
        
        self._labelNombre = tk.Label(self.datosFrame, text="Nombre")
        self._nombre = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaStr), "%P") 
        )
        
        self._labelApellido = tk.Label(self.datosFrame, text="Apellido")
        self._apellido = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaStr), "%P") 
        )
        
        self._labelDireccion = tk.Label(self.datosFrame, text="Dirección")
        self._direccion = tk.Entry(self.datosFrame)
        
        self._labelFechaNac = tk.Label(
            self.datosFrame, text="Fecha de nacimiento\n(DD-MM-AAAA)"
        )
        self._fecha_nac = tk.Entry(self.datosFrame)
        
        self._labelEmail = tk.Label(self.datosFrame, text="E-mail")
        self._email = tk.Entry(self.datosFrame)
        
        self._labelTel = tk.Label(self.datosFrame, text="Teléfono")
        self._telefono = tk.Entry(
            self.datosFrame, validate="key", 
            validatecommand=(root.register(self._validaNum), "%P") 
        )
        
        self._labelPrev = tk.Label(self.datosFrame, text="Previsión:")
        self._prevision = tk.IntVar()
        self._prevR1 = tk.Radiobutton(
            self.datosFrame, text="FONASA", variable=self._prevision, value=1
        )
        self._prevR2 = tk.Radiobutton(
            self.datosFrame, text="ISAPRE", variable=self._prevision, value=2
        )

    def limpiaCampos(self):
        """
        Borra cualquier valor establecido en los campos de paciente.

        No retorna nada.
        """
        listaCampos = [
        self._rut, self._nombre, self._apellido, self._direccion, self._fecha_nac, 
        self._email, self._telefono
        ]

        for l in listaCampos:
            l.delete(0, tk.END)
        self._prevision.set(0)
    
    def _camposNulos(self):
        """
        Comprueba si existen campos nulos en los campos del paciente.
        
        En el caso que hayan campos nulos, retorna True. Caso contrario
        retorna False.
        """
        listaCampos = [
        self._rut, self._nombre, self._apellido, self._direccion, self._fecha_nac, 
        self._email, self._telefono
        ]
        for l in listaCampos:
            if l.get() == "":
                return True
        if self._prevision.get() == 0:
            return True

        
        return False

    def _validaFecha(self):
        """
        Comprueba que la fecha ingresada por el usuario está en el formato
        adecuado: DD-MM-AAAA.

        Retorna True, si la fecha sigue el formato. Caso contrario, retorna
        False.
        """
        if re.fullmatch(
            r"((^0?[1-9])|(^[12]\d)|(^3[01]))-((0?[1-9])|(1[0-2]))-((19\d\d$)|(2[01]\d\d$))", 
            self._fecha_nac.get()
        ):
            
            return True
        return False

    def _validaStr(self, val):
        """
        Comprueba que solo se puedan poner caracteres alfabéticos en el entry.

        Retorna True si el valor a poner en el entry es alfabético. Caso contrario,
        retorna False.
        """
        # Esto es para que el Entry quede vacío cuando se aprieta el boton "limpiacampos"
        if val == "":
            return True

        nval = "".join(val.split(" "))
        
        return nval.isalpha()
    
    def _validaNum(self, val):
        """
        Comprueba que solo se puedan poner caracteres numéricos en el entry.

        Retorna True si el valor a poner en el entry es numérico. Caso contrario,
        retorna False.
        """
        # Esto es para que el Entry quede vacío cuando se aprieta el boton "limpiacampos"
        if val == "":
            return True

        return val.isdigit()

    def _validaRut(self):
        """
        Comprueba que el rut ingresado por el usuario está en el formato
        adecuado: {10 digitos}-{digito verificador}.

        Retorna True, si el rut sigue el formato. Caso contrario, retorna
        False.
        """
        match = re.fullmatch(r"^\d{8}-[\dk]$", self._rut.get())
        if match:
            
            return True
        return False

    def _validaEmail(self):
        """
        Comprueba que el email ingresado por el usuario está en el formato
        adecuado.

        Retorna True, si el email sigue el formato. Caso contrario, retorna
        False.
        """
        match = re.fullmatch(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
            self._email.get()
        )
        if match:
            return True
        
        return False

