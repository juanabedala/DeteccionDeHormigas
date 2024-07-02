import json


def generar_kml(datos_json, ruta_salida):
    kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Marcadores de imágenes</name>
    <description>Marcadores de imágenes con bounding boxes</description>
'''
   
    for dato in datos_json:
        if dato['contaBoxes'] > 0:
            kml_content += f'''
    <Placemark>
        <name>{dato['imagen']}</name>
        <description>Bounding boxes: {dato['contaBoxes']}</description>
        <Point>
            <coordinates>{dato['longitud']},{dato['latitud']},0</coordinates>
        </Point>
    </Placemark>
'''


    kml_content += '''
</Document>
</kml>
'''


    with open(ruta_salida, 'w') as archivo_kml:
        archivo_kml.write(kml_content)


# Ejemplo de uso
ruta_json = 'resultados.json'
ruta_salida_kml = 'marcadores.kml'


# Leer los datos del archivo JSON
with open(ruta_json, 'r') as archivo_json:
    datos_json = json.load(archivo_json)


# Generar el archivo KML
generar_kml(datos_json, ruta_salida_kml)


print("Archivo KML generado en", ruta_salida_kml)
