# appSaludTkinter

CRUD en Python usando la bibliioteca de interfaz gráfica tkinter.

La aplicación está pensada para ser usada por personal administrativo de un centro médico durante la atención que se le hace a un paciente en la compra de examenes.

La aplicación cuenta con las siguientes funciones:
1. Login de usuario
2. Registro de pacientes
3. Ver pacientes registrados
4. Exportar a Excel la lista de pacientes registrados
5. Modificación de datos de pacientes registrados
6. Ver atenciones registradas de un paciente
7. Generar una atención de un paciente. Acá se registrará la compra de examenes médicos.


## Base de datos
La base de datos utilizada es una base de datos generada por el gestor sqlite. Se puede identificar dentro del directorio de archivos como `data`.

## Ejecución
1. Si es la primera vez al usar el software, se debe ejecutar el archivo `bd.py` antes de la aplicación principal `main.py` para así crear la base de datos sqlite.

```
python bd.py
```

2. Ejecutar la aplicación `main.py`

```
python main.py
```

## Screenshots
