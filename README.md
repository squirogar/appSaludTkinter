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

El modelo entidad relación (MER) de la base de datos es el siguiente:

![MER](https://github.com/squirogar/appSaludTkinter/assets/50588970/1196d1df-4458-40fc-ae62-8bde64998553)

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
### 1. Login
![login](https://github.com/squirogar/appSaludTkinter/assets/50588970/4f2591b4-b995-4870-bd89-a5633504110f)

### 2. Menú principal
![menu_principal](https://github.com/squirogar/appSaludTkinter/assets/50588970/b97f9823-fa9a-4568-8cde-7a9ad14734c6)

### 3. Registro de pacientes
![registro](https://github.com/squirogar/appSaludTkinter/assets/50588970/00852179-7f3f-4432-98b6-35b68062eebc)

### 4. Pacientes registrados
![pacientes_registrados](https://github.com/squirogar/appSaludTkinter/assets/50588970/ad331f98-385b-485f-89c6-5663d5ad45dc)

### 5. Modificar información de paciente y eliminarlo
![modificar_info_pacientes](https://github.com/squirogar/appSaludTkinter/assets/50588970/58ca9d9c-8c1b-438b-a208-9159bcd189e8)

### 6. Generar atención
![generar_atencion](https://github.com/squirogar/appSaludTkinter/assets/50588970/da7df847-10c3-4fa4-be02-2f9f1f6c3460)

### 7. Atenciones de un paciente
![atenciones_paciente](https://github.com/squirogar/appSaludTkinter/assets/50588970/d9216310-9136-4823-b361-e0dd5be93f2b)

## Dependencias
Es necesario tener las siguientes librerías para ejecutar el código de `main.py`. Esto se debe a la funcionalidad de exportar a Excel.
- Pandas
- openpyxl

## Licencia
GPL-3.0



