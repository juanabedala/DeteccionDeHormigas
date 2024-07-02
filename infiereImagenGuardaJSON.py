import torch
import cv2
import numpy as np
import os
import json
import re


def listar_imagenes_en_directorio(subdirectorio='img'):
    extensiones_permitidas = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    imagenes = []


    try:
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        directorio_imagenes = os.path.join(directorio_actual, subdirectorio)


        for archivo in os.listdir(directorio_imagenes):
            if os.path.isfile(os.path.join(directorio_imagenes, archivo)):
                if any(archivo.lower().endswith(ext) for ext in extensiones_permitidas):
                    imagenes.append(archivo)
    except Exception as e:
        print(f"Error al listar imágenes: {e}")


    return imagenes


def extraer_lat_long(nombre_archivo):
    # Utilizar una expresión regular para extraer los números del nombre del archivo
    match = re.match(r'(-?\d+\.\d+)_(-?\d+\.\d+)\.py', nombre_archivo)
    if match:
        latitud = float(match.group(1))
        longitud = float(match.group(2))
        return latitud, longitud
    else:
        raise ValueError("El nombre del archivo no está en el formato esperado")
   


def guardar_en_json(resultados, ruta_salida):
    with open(ruta_salida, 'w') as archivo_json:
        json.dump(resultados, archivo_json, indent=4)
           
pathImgsParaInferencia = 'imgParaInferencia/'
pathModelo = 'C:/Users/MSI/Desktop/vsCodeYolov5/modelos/yolov5s100e.pt'




model = torch.hub.load('ultralytics/yolov5', 'custom',path=pathModelo,force_reload=True)


subdirectorio_a_listar = pathImgsParaInferencia  # Cambia esto si el subdirectorio tiene un nombre diferente
imagenes_en_subdirectorio = listar_imagenes_en_directorio(subdirectorio_a_listar)
contaBoxes = 0
resultados = {}




if imagenes_en_subdirectorio:
    print(f"Imágenes en el subdirectorio '{subdirectorio_a_listar}':")
    for imagen in imagenes_en_subdirectorio:
        contaBoxes = 0
        imagen2 = cv2.imread('imgParaInferencia/'+imagen)
        imagenres = cv2.resize(imagen2, (640, 640))
        latitud, longitud = extraer_lat_long(imagen)
        detect = model(imagenres)
       
        # Obtener los bounding boxes y las etiquetas predichas
        bounding_boxes = detect.pandas().xyxy[0]
        labels = detect.names[0]
       
        coordenadas = []


        for index, row in bounding_boxes.iterrows():
            contaBoxes = contaBoxes + 1
            label = labels[int(row['class'])]
            confidence = row['confidence']
            xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            coordenadas.append({
                "label": label,
                "confidence": float(confidence),
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax
            })
       
        resultados.append({
            "imagen": imagen,
            "latitud": latitud,
            "longitud": longitud,
            "coordenadas": coordenadas
        })
       
    # Guardar los resultados en un archivo JSON
    guardar_en_json(resultados, 'resultados.json')
   
else:
    print(f"No se encontraron imágenes en el subdirectorio '{subdirectorio_a_listar}'.")
