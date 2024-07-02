import cv2
import threading
import time
import serial
import datetime


datoGPS = 'sinDato'
# Configura el objeto Serial
#puerto_serial = serial.Serial('/dev/ttyUSB0', 9600)
puerto_serial = serial.Serial('/dev/ttyS0', 9600)


def leer_datos_gps():
    global datoGPS
   
    tiempo_inicio = time.time()
    datoGPS = "sinDato"  # Inicializa la variable datoGPS
    print(datoGPS)
   
    try:
        while True:


            linea = puerto_serial.readline().decode('utf-8')
           
           
            linea = linea.strip()
            if linea.startswith('$GPGGA'):
                print(linea)
                # Procesa la línea NMEA según tus necesidades
                # Aquí puedes extraer la latitud, longitud, etc.
               
                campos = linea.split(',')
                # Verifica que la línea NMEA tenga la cantidad esperada de campos
                if len(campos) >= 6:
                    # Extrae la latitud y la longitud en formato DDDMM.MMMMM
                    latitud = float(campos[2][:2]) + float(campos[2][2:]) / 60.0
                    longitud = float(campos[4][:3]) + float(campos[4][3:]) / 60.0


                    # Ajusta la latitud y longitud según la dirección (Norte/Sur, Este/Oeste)
                    if campos[3] == 'S':
                        latitud *= -1
                    if campos[5] == 'W':
                        longitud *= -1


                    slatitud = "{:.6f}".format(latitud)
                    slongitud = "{:.6f}".format(longitud)
                    datoGPS = slatitud + '_' + slongitud
                    print(datoGPS + "GPSOKOKOKOKOKOKOKOK")
                   
                   
                else:
                    datoGPS = 'sinDato'
                    print("La línea NMEA no tiene la cantidad esperada de campos.")
            #time.sleep(1)        
    except serial.SerialException as e:
        datoGPS = 'sinDato'
        print("Error al leer datos GPS:", e)
    except Exception as e:
        datoGPS = 'sinDato'
        print("Error desconocido:", e)
   


       
def capturar_y_guardar(camara, ruta_archivo):
    try:
        cap = cv2.VideoCapture(camara)
        # Establecer la resolución deseada (640x640)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)


        # Pequeño retraso para dar tiempo a que la cámara se inicialice
        time.sleep(10)
        countFoto = 0
        while True:
            ret, frame = cap.read()
            sfechaActual = '_' + obtenerFechaHora()
            nombre_archivo = ruta_archivo + datoGPS + sfechaActual + '.jpg'
            if ret:
                # Redimensionar la imagen a 640x640 si no tiene esa resolución
                if frame.shape[0] != 640 or frame.shape[1] != 640:
                    frame = cv2.resize(frame, (640, 640))


                # Guardar la imagen en el archivo
               
                cv2.imwrite(nombre_archivo, frame)


                print(f'Foto de la cámara {camara} guardada en {nombre_archivo}')
                countFoto += 1
            else:
                print(f'Error al capturar imagen de la cámara {camara}')
                print(nombre_archivo)
                # Intentar reiniciar la cámara si no se inicializó correctamente
                cap.release()  # Liberar recursos de la cámara antes de intentar reiniciarla
                cap = cv2.VideoCapture(camara)  # Intentar reiniciar la cámara
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Restablecer la resolución
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
                time.sleep(2)  # Esperar un breve periodo antes de intentar nuevamente
                continue  # Volver al inicio del bucle para intentar capturar una imagen nuevamente


            # Esperar 2 segundos antes de capturar la próxima imagen
            time.sleep(0.5)


            # Salir del bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f'Error al acceder a la cámara {camara}: {e}')
    finally:
        cap.release()


def obtenerFechaHora():
    d = datetime.datetime.now()
    sfecha = str(d.year)+str(d.month)+str(d.day)+str(d.hour)+str(d.minute)+str(d.second)
    return sfecha


if __name__ == "__main__":
   
    camara_0_thread = threading.Thread(target=capturar_y_guardar, args=(0, 'imgsCam1/'))
    camara_1_thread = threading.Thread(target=capturar_y_guardar, args=(2, 'imgsCam2/'))


    hilo_gps = threading.Thread(target=leer_datos_gps)
    hilo_gps.start()
    time.sleep(0.5)
   


   
    camara_0_thread.start()
    # Agregamos un retraso adicional antes de iniciar la segunda cámara
    time.sleep(0.5)
    camara_1_thread.start()
    time.sleep(5)


    hilo_gps.join()
    camara_0_thread.join()
    camara_1_thread.join()
