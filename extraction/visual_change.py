import cv2
import os
from dotenv import load_dotenv
load_dotenv()

# detectar movimientos o transiciones drásticas entre escenas en un video.
def extract_significant_frames(video_path, threshold=35):
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    frame_count = 0
    saved_frames = []
    while cap.isOpened():
        print("procesando...");
        ret, frame = cap.read()
        if not ret:
            break

        # Convierte el frame actual a escala de grises para facilitar la comparación
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            prev_frame = gray_frame
            saved_frames.append(frame)
            continue

        # Calcular la diferencia absoluta entre el frame anterior y el actual
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        
        # Calcular un umbral (threshold) para decidir si el cambio es significativo
        diff_score = frame_diff.mean()

        if diff_score > threshold:
            print('frame_count siuuuuuu')    
            saved_frames.append(frame)
            prev_frame = gray_frame

        frame_count += 1
        print(frame_count)

    cap.release()
    return saved_frames

frames = extract_significant_frames(os.environ.get('VIDEO_GPS_PATH'))
print(os.environ.get('VIDEO_GPS_PATH'))

for idx, frame in enumerate(frames):
    cv2.imwrite(f"frame_{idx}.jpg", frame)
