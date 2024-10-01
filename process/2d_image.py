from dotenv import load_dotenv
import os
import subprocess

load_dotenv()
# OBTIENE UNA CARPETA DE FOTOS 360 Y LAS DEVUELVE EN 2D
def convert_360_to_2d(input_image, output_image, yaw=0, pitch=0):
    """
    Convierte una imagen 360 grados en una imagen plana usando ffmpeg.
    """
    command = [
        'ffmpeg', '-i', input_image,
        '-vf', f"v360=input=e:output=flat:yaw={yaw}:pitch={pitch}",
        output_image
    ]
    try:
        result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(f"Imagen guardada como {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando ffmpeg para {input_image}: {e}")
        print(e.stderr)


def process_images_in_folder(folder_path, output_folder, yaw=0, pitch=0):
    """
    Procesa todas las imágenes 360 grados en la carpeta y las convierte a imágenes planas.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Crear la carpeta de salida si no existe

    for filename in os.listdir(folder_path):
        # Filtrar solo imágenes (puedes ajustar esto según el formato de tus imágenes)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_image = os.path.join(folder_path, filename)
            output_image = os.path.join(output_folder, f"flat_{filename}")

            # Convertir la imagen 360 a plana
            convert_360_to_2d(input_image, output_image, yaw, pitch)

# Ruta de la carpeta de entrada y salida
input_folder = os.getenv('FOLDER_IMAGE_PATH')
output_folder = os.getenv('FOLDER_OUTPUT_PATH')

# Procesar todas las imágenes en la carpeta
process_images_in_folder(input_folder, output_folder, yaw=0, pitch=0)
