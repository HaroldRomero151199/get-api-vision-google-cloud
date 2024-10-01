import cv2
import os
from geopy.distance import geodesic
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

video_path = os.environ.get('VIDEO_GPS_PATH')
exiftool_path = os.environ.get('EXIFTOOL_PATH')

def get_gps_data_from_video(video_path):
    """
    Extrae datos GPS del archivo de video usando ExifTool a través de subprocess.
    """
    # Ejecutar el comando ExifTool para obtener los metadatos en formato JSON
    command = [exiftool_path, '-j', '-n', video_path]  # '-n' devuelve las coordenadas GPS en decimal
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Si hay un error en la ejecución, mostrar el error
    if result.returncode != 0:
        print(f"Error ejecutando ExifTool: {result.stderr}")
        return None
    print(result)
    # Convertir el resultado en formato JSON
    metadata = json.loads(result.stdout)

    # Verificar si hay datos GPS
    if 'GPSLatitude' in metadata[0] and 'GPSLongitude' in metadata[0]:
        try:
            gps_data = {
                'latitude': float(metadata[0]['GPSLatitude']),
                'longitude': float(metadata[0]['GPSLongitude'])
            }
            print(gps_data)
            return gps_data
        except ValueError:
            print("Error: Los datos GPS no están en formato numérico.")
            return None
    else:
        return None

def extract_frames_based_on_distance(video_path, min_distance=1):
    """
    Extrae frames del video si hay una diferencia significativa en la distancia geográfica.
    """
    # Cargar los datos GPS del video completo
    gps_coords = get_gps_data_from_video(video_path)
    if gps_coords is None:
        print("No se encontraron datos GPS en el video.")
        return []

    cap = cv2.VideoCapture(video_path)
    prev_gps_coords = gps_coords  # Coordenadas GPS iniciales
    saved_frames = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Usamos las mismas coordenadas GPS del video para todos los frames
        current_gps_coords = gps_coords  # Suponemos que las coordenadas son constantes

        # Validar las coordenadas antes de calcular la distancia
        if prev_gps_coords and current_gps_coords:
            try:
                distance = geodesic((prev_gps_coords['latitude'], prev_gps_coords['longitude']),
                                    (current_gps_coords['latitude'], current_gps_coords['longitude'])).meters
            except ValueError as e:
                print(f"Error al calcular la distancia: {e}")
                break

            # Si la distancia es mayor al mínimo, guardamos el frame
            if distance >= min_distance:
                saved_frames.append(frame)
                prev_gps_coords = current_gps_coords  # Actualizamos las coordenadas previas
                print(f"Frame {frame_count} guardado. Distancia recorrida: {distance} metros.")
        frame_count += 1

    cap.release()
    return saved_frames

# Ejecutar la extracción de frames
frames = extract_frames_based_on_distance(video_path)

# Guardar los frames o procesarlos
for idx, frame in enumerate(frames):
    cv2.imwrite(f"frame_{idx}.jpg", frame)
    print(f"Frame {idx} guardado como 'frame_{idx}.jpg'.")
