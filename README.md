# EasyOCR in Python

## Acerca de OCR

OCR (Optical Character Recognition) es un proceso de análisis el cual obtiene una imagen como parámetro de entrada, convirtiéndolo en un formato de texto con su contenido.
Un ejemplo claro, es  el análisis de formularios, facturas e incluso documentos legales escaneados, información que debe ser plasmada de manera digital para su divulgación, por lo que mediante el OCR, esta actividad puede llevarse a cabo.

## Funcionamiento de un software de OCR

### Adquisición de imagen
Un escaner deberá leer los documentos y convertirlos en datos binarios, es decir, se deberá analizar la imagen escaneada para definir la diferencia entre las zonas más claras (catalogadas como "fondo" y las áreas más oscurdad (las cuales se definen como texto).

### Procesamiento previo

El software OCR se encarga de limpiar la imagen y eliminar los errores para que sea apta para su lectura, eliminando manchas de imágenes difitales, limpiando cuadros y líneas e incluso reconociendo renglones de texto mediante tecnología OCR multilingüe.

### Reconocmiento de texto

El algoritmo de OCR se encargará de extraer la información de las imágenes mediante la coincidencia de patrones y extracción de características.

### Procesamiento

Después del análisis del sistema, OCR convertirá los datos de texto extraídos en un archivo computarizado, teniendo incluso la capacidad de retornarlos como archivos PDF.

## OCR en Python

"EasyOCR" es un ha sido programado para ser un servicio web con la capacidad de obtener archivos .pdf, leer las imágenes que contiene y extraer la información textual que contienen, generando así un documento .txt con el texto extraído.

### Librerías empleadas

A continuación, se muestra una lista de las librerías empleadas en el código presentado:

- OpenCV 
> Link de instalación https://pypi.org/project/opencv-python/
> $pip3 install opencv-python

- EasyOCR versión 1.7.1
> Métodos de instalación:
> https://www.jaided.ai/easyocr/documentation/
> $pip3 install easyocr
- PyMuPDF 1.24.2
> Métodos de instalación:
> https://pypi.org/project/PyMuPDF/
> $pip3 install pymupdf
- Pillow 10.3.0
> Métodos de instalación:
> https://pypi.org/project/pillow/
> $pip3 install pillow

## Pseudocódigo
![OCR_Pseudocódigo](https://github.com/AnaPolar/EasyOCR-en-Python/assets/112904164/10a224e0-d33b-4c6e-b494-46ae24ef9e7f)

## Participantes

- Alejandro Harael Garcia Sanchez
- Ana Paula Guillen Maldonado
- Cesar Briones Martínez
- Sacnicté Cruz Arellano
