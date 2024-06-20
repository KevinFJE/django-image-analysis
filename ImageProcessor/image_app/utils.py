# utils.py

import cv2 as cv
from django.conf import settings
import numpy as np
from rembg import remove
import os

def remove_background(image_path):
    input_path = image_path
    output_path = os.path.join(settings.MEDIA_ROOT, 'processed', os.path.basename(image_path))
    with open(input_path, 'rb') as inp, open(output_path, 'wb') as outp:
        background_output = remove(inp.read())
        outp.write(background_output)
    return output_path

def apply_color_filters(image_path):
    imga = cv.imread(image_path, 1)
    img = cv.resize(imga, (640, 480))
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Definir los rangos de color
    blancoBajo = np.array([0, 0, 200], np.uint8)
    blancoAlto = np.array([180, 50, 255], np.uint8)

    verdeBajo = np.array([40, 50, 50])
    verdeAlto = np.array([80, 255, 255])

    amarilloBajo = np.array([20, 50, 50])
    amarilloAlto = np.array([39, 255, 255])

    # Aplicar los filtros
    maskYellow = cv.inRange(img_hsv, amarilloBajo, amarilloAlto)
    filterYelow = cv.bitwise_and(img, img, mask=maskYellow)

    maskGreen = cv.inRange(img_hsv, verdeBajo, verdeAlto)
    filterGreen = cv.bitwise_and(img, img, mask=maskGreen)

    maskWhite = cv.inRange(img_hsv, blancoBajo, blancoAlto)
    filterWhite = cv.bitwise_and(img, img, mask=maskWhite)

    # Contar el número de píxeles en cada máscara
    total_pixels = img.shape[0] * img.shape[1]

    yellow_pixels = cv.countNonZero(maskYellow)
    green_pixels = cv.countNonZero(maskGreen)
    white_pixels = cv.countNonZero(maskWhite)

    # Calcular el porcentaje de cada color
    yellow_percentage = (yellow_pixels / total_pixels) * 100
    green_percentage = (green_pixels / total_pixels) * 100
    white_percentage = (white_pixels / total_pixels) * 100

    # Determinar el diagnóstico
    diagnosis = "Planta sana"
    if green_percentage < 20:
        diagnosis = "No es una planta o la limpieza falló"
    if yellow_percentage >= 10:
        diagnosis = "Posible Botritis, mildiu o falta de agua"
    if white_percentage >= 2:
        diagnosis = "Posible ataque de Oidio"

    # Guardar las imágenes filtradas
    output_dir = os.path.join(os.path.dirname(image_path), 'filtered')
    os.makedirs(output_dir, exist_ok=True)

    green_filtered_path = os.path.join(output_dir, 'green_filtered.png')
    white_filtered_path = os.path.join(output_dir, 'white_filtered.png')
    yellow_filtered_path = os.path.join(output_dir, 'yellow_filtered.png')

    cv.imwrite(green_filtered_path, filterGreen)
    cv.imwrite(white_filtered_path, filterWhite)
    cv.imwrite(yellow_filtered_path, filterYelow)

    return {
        'filtered_images': {
            'green': green_filtered_path,
            'white': white_filtered_path,
            'yellow': yellow_filtered_path,
        },
        'diagnosis': diagnosis,
        'percentages': {
            'yellow': yellow_percentage,
            'green': green_percentage,
            'white': white_percentage,
        }
    }