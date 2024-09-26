
from google.cloud import vision
from google.oauth2 import service_account
import json
import os
from dotenv import load_dotenv
load_dotenv()
credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)

image_path = os.environ.get('IMAGE_PATH')

def getImage(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    return content

client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_objects(image_content):
    getImage(image_path)
    image = vision.Image(content=image_content)
    # Realizar múltiples solicitudes a la API
    response = client.annotate_image({
        'image': image,
        'features': [
            vision.Feature(type=vision.Feature.Type.LABEL_DETECTION),
            vision.Feature(type=vision.Feature.Type.TEXT_DETECTION),
            vision.Feature(type=vision.Feature.Type.LOGO_DETECTION),
        ]
    })

    # print(json.dumps(response, indent=4))
    # print("json.dumps(response)")
    # print(json.dumps(response))
    labels = response.label_annotations
    logos = response.logo_annotations
    text_annotations = response.text_annotations

    # Etiquetas
    print("Etiquetas detectadas:")
    for label in labels:
        print(f'{label.description} (Confianza: {label.score})')

    # Texto
    print("\nTexto detectado:")
    if text_annotations:
        print(text_annotations[0].description)

    # Logotipos
    print("\nLogotipos detectados:")
    for logo in logos:
        print(f'{logo.description} (Confianza: {logo.score})')

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


# detect_objects(image_path)