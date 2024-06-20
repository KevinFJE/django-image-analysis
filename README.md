# Django Image Analysis

Este proyecto es una aplicación web de Django que permite la eliminación de fondos y la aplicación de filtros de colores a imágenes. Las imágenes originales se leen de una carpeta específica y se procesan para mostrar los resultados de los análisis realizados.

## Características

- Elimina el fondo de las imágenes.
- Aplica filtros de colores (amarillo, blanco y verde) para detectar posibles enfermedades en las plantas.
- Muestra las imágenes originales y procesadas.
- Registra y muestra los resultados de los análisis.

## Requisitos

- Python 3.x
- Django
- numpy
- rembg
- opencv-python

## Instalación

1. Clonar el repositorio:

git clone https://github.com/KevinFJE/django-image-analysis.git

cd django-image-analysis

2. Crear y activar un entorno virtual:

python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. Instalar las dependencias:

pip install -r requirements.txt

4. Realizar las migraciones y ejecutar el servidor de desarrollo:

python manage.py migrate
python manage.py runserver

5. Acceder a la aplicación en http://127.0.0.1:8000.

Uso

Sube una imagen en la pagina de inicio.

Haz clic en "Realizar análisis" para procesar la imagen más reciente.

Los resultados se mostrarán en la página, incluyendo las imágenes originales y procesadas