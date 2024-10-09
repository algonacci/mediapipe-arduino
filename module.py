import math

def calculate_ear(eye_points):
    # Hitung jarak vertikal antara landmark mata
    v1 = euclidean_distance(eye_points[1], eye_points[5])
    v2 = euclidean_distance(eye_points[2], eye_points[4])
    
    # Hitung jarak horizontal antara landmark mata
    h = euclidean_distance(eye_points[0], eye_points[3])
    
    # Hitung EAR
    ear = (v1 + v2) / (2.0 * h)
    return ear

def check_close_eyes(left_eye_points, right_eye_points):
    # Nilai ambang batas EAR untuk mata tertutup
    # Nilai ini mungkin perlu disesuaikan berdasarkan pengujian
    EAR_THRESHOLD = 0.2

    left_ear = calculate_ear(left_eye_points)
    right_ear = calculate_ear(right_eye_points)

    print(f"Eye Aspect Ratio - Left: {left_ear:.4f}, Right: {right_ear:.4f}")

    left_eye_closed = left_ear < EAR_THRESHOLD
    right_eye_closed = right_ear < EAR_THRESHOLD

    if left_eye_closed and right_eye_closed:
        print("Both eyes detected as closed")
    elif left_eye_closed:
        print("Left eye detected as closed")
    elif right_eye_closed:
        print("Right eye detected as closed")
    else:
        print("Both eyes detected as open")

    return left_eye_closed, right_eye_closed

def euclidean_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)