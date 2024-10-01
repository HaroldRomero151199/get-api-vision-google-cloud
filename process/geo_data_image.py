from PIL import Image
import piexif
from dotenv import load_dotenv
import os
load_dotenv()

def convert_to_degrees(value):
    """
    Convierte el valor en formato GPS (grados, minutos, segundos) a grados decimales.
    """
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])

    return d + (m / 60.0) + (s / 3600.0)

def get_gps_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data_raw = img.info.get('exif')
        if not exif_data_raw:
            print(f"No se encontraron datos EXIF en la imagen {image_path}")
            return None, None

        # Cargar los datos EXIF con piexif
        exif_data = piexif.load(exif_data_raw)
        
        # Verificar si existen datos GPS
        if 'GPS' in exif_data:
            gps_info = exif_data['GPS']
            gps_latitude = gps_info.get(2)  # Coordenadas de latitud
            gps_latitude_ref = gps_info.get(1)  # Referencia N/S
            gps_longitude = gps_info.get(4)  # Coordenadas de longitud
            gps_longitude_ref = gps_info.get(3)  # Referencia E/W

            if gps_latitude and gps_longitude:
                # Convertir latitud y longitud a grados decimales
                lat = convert_to_degrees(gps_latitude)
                lon = convert_to_degrees(gps_longitude)

                # Ajustar las coordenadas según la referencia N/S y E/W
                if gps_latitude_ref != b'N':
                    lat = -lat
                if gps_longitude_ref != b'E':
                    lon = -lon

                return lat, lon
        else:
            print(f"No se encontraron datos GPS en la imagen {image_path}")

    except Exception as e:
        print(f"Error procesando {image_path}: {e}")
    
    return None, None

def process_images_in_folder(folder_path):
    """
    Procesa todas las imágenes en la carpeta especificada y extrae los datos de GPS.
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            image_path = os.path.join(folder_path, filename)
            lat, lon = get_gps_data(image_path)

            if lat is not None and lon is not None:
                print(f"Imagen: {filename},  lat/long : {lat}, {lon}")
            else:
                print(f"No se encontraron datos GPS en la imagen {filename}")

folder_path = os.getenv('FOLDER_IMAGE_PATH')

# Procesar todas las imágenes en la carpeta
process_images_in_folder(folder_path)
