import cv2
import mediapipe as mp
import module
import serial  # Untuk komunikasi serial dengan Arduino
import time

print("Program started")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Camera opened successfully")

state = 1  # Default state
light_state = False  # Menyimpan status lampu (False = mati, True = nyala)

arduino = serial.Serial('COM3', 115200, timeout=1)  # Sesuaikan dengan port Arduino kamu
time.sleep(3)  # Tunggu 2 detik agar Arduino siap
arduino.flush() 

def toggle_light(left_eye_closed, right_eye_closed):
    global light_state
    if right_eye_closed and not light_state:
        # Jika mata kanan tertutup dan lampu mati, nyalakan lampu
        light_state = True
        print("Lampu dinyalakan")
        arduino.write('ON\n'.encode())  # Kirim perintah "ON" ke Arduino
    elif left_eye_closed and light_state:
        # Jika mata kiri tertutup dan lampu menyala, matikan lampu
        light_state = False
        print("Lampu dimatikan")
        arduino.write('OFF\n'.encode())  # Kirim perintah "OFF" ke Arduino




def adjust_light_intensity(left_ear, right_ear):
    # Hitung EAR rata-rata dari kedua mata
    average_ear = (left_ear + right_ear) / 2

    # Map EAR ke intensitas LED (EAR 0.2 - 0.3 -> Intensitas 0 - 255)
    intensity = int(max(0, min(255, (average_ear - 0.2) / (0.3 - 0.2) * 255)))

    # Kirim intensitas ke Arduino melalui serial
    arduino.write(f'{intensity}\n'.encode())  # Mengirim nilai intensitas

    # Debugging untuk memantau intensitas
    print(f"Adjusting light intensity to {intensity} (EAR: {average_ear:.4f})")



# Landmark indices for eyes
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  
    print("Entering main loop")
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Error: Could not read frame")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            print("Face detected")
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
            
                left_eye_points = [face_landmarks.landmark[i] for i in LEFT_EYE]
                right_eye_points = [face_landmarks.landmark[i] for i in RIGHT_EYE]

                left_eye_closed, right_eye_closed = module.check_close_eyes(left_eye_points, right_eye_points)

                print(f"Left eye: {'Closed' if left_eye_closed else 'Open'}, Right eye: {'Closed' if right_eye_closed else 'Open'}")

                if state == 1:
                    toggle_light(left_eye_closed, right_eye_closed)
                elif state == 2:
                    left_ear = module.calculate_ear(left_eye_points)
                    right_ear = module.calculate_ear(right_eye_points)
                    adjust_light_intensity(left_ear, right_ear)
        else:
            print("No face detected")

        # Menampilkan status lampu dan state pada layar
        # Menampilkan status lampu dan state pada layar
        status_text = f"Lampu: {'Nyala' if light_state else 'Mati'} | State: {state}"
        
        # Set posisi dan ukuran kotak latar belakang hitam
        (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)  # Ukuran teks
        x, y = 10, 30  # Posisi teks
        cv2.rectangle(image, (x, y - h - 10), (x + w, y + 10), (0, 0, 0), -1)  # Buat kotak hitam
        
        # Tampilkan teks di atas kotak hitam
        cv2.putText(image, status_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        cv2.imshow('LED Arduino', image)

        key = cv2.waitKey(5) & 0xFF
        if key == ord('1'):
            state = 1
            print("Switched to State 1: Toggle light with eye blinks")
        elif key == ord('2'):
            state = 2
            print("Switched to State 2: Adjust light intensity")
        elif key == 27:  # ESC key
            print("ESC pressed, exiting...")
            break

cap.release()
cv2.destroyAllWindows()
print("Program ended")