# Instalación

1- Si se está en un ambiente virtual, activar el ambiente virtual; windows: `ruta-ambiente-virtual/Scripts/activate`; linux: `source ruta-ambiente-virtual/bin/activate`.

2- Clonar el repositorio desde GitHub de la siguiente forma: `git clone https://github.com/AnaPolar/EasyOCR-en-Python.git`

3- Tener instalado pip con: `python -m ensurepip --upgrade`

4- Dirigirse al directorio del repositorio instalado con: `cd EasyOCR-en-Python`

5- Instalar las librerías y frameworks necesarios con: `pip install -r dependencies.txt`

6- Ejecutar el script de python con: `python easyOCR_equipo4.py flask`

7- Usando POSTMAN (API CLIENT), ingresar la url en método POST: http://localhost:5000/archs
![image](https://github.com/AnaPolar/EasyOCR-en-Python/assets/129553512/dd0bea4d-135b-4a79-9d1f-e4216abba38b)

Y subir el pdf que se quiere usar para exxtraer el mensaje.

__Tomar en cuenta la siguiente configuración en POSTMAN__
  - Headers
	  - Content-Type : multipart/form-data

  - Body 
	 - Key : file
	 - Type : File
	 - Value: pdf

