import cv2
import os

def extract_frames(input_folder, output_folder):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Entre")
    # Iterar sobre todos los archivos en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        # Comprobar si el archivo es un archivo de video
        print("File name:" + file_name)
        if file_name.endswith(('.mp4', '.avi', '.MOV')):
            # Obtener la ruta completa del archivo de video
            video_path = os.path.join(input_folder, file_name)
            # Obtener el nombre del archivo sin la extensión
            file_name_no_extension = os.path.splitext(file_name)[0]


            # Abrir el archivo de video
            cap = cv2.VideoCapture(video_path)
            # Inicializar el contador de frames
            frame_count = 0


            # Iterar sobre los frames del video
            while True:
                # Leer el siguiente frame
                success, frame = cap.read()
                if not success:
                    break
                # Guardar el frame como una imagen
                if (frame_count%30==0):
                    # Cambiar el tamaño del frame a 640x640
                    frame_resized = cv2.resize(frame, (640, 640))
                    frame_output_path = os.path.join(output_folder, f"{file_name_no_extension}_frame{frame_count}.jpg")
                    cv2.imwrite(frame_output_path, frame_resized)


                frame_count += 1


            # Cerrar el archivo de video
            cap.release()


# Carpeta de entrada que contiene los archivos de video
input_folder = "videos"
# Carpeta de salida donde se guardarán los frames extraídos
output_folder = "imgs"


# Llamar a la función para extraer los frames
extract_frames(input_folder, output_folder)
