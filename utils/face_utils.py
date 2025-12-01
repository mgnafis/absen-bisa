import cv2
import face_recognition
import numpy as np
import os
import pickle

def preprocess_image(image):
    """Preprocess image untuk face recognition"""
    try:
        # Convert ke grayscale jika perlu
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Histogram equalization
        equalized = cv2.equalizeHist(gray)

        # Convert kembali ke 3 channel jika perlu
        if len(image.shape) == 3:
            equalized = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

        return equalized
    except:
        return image

def validate_face_image(image):
    """Validasi apakah image cocok untuk face recognition"""
    try:
        # Basic validation
        if image is None:
            return False, "Image is None"

        # Check image size
        if image.shape[0] < 100 or image.shape[1] < 100:
            return False, "Image terlalu kecil (minimal 100x100 pixel)"

        # Check brightness
        if np.mean(image) < 30:
            return False, "Image terlalu gelap"

        if np.mean(image) > 240:
            return False, "Image terlalu terang"

        return True, "Valid"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def get_face_quality_score(face_encoding, known_encodings):
    """Menghitung kualitas kecocokan wajah"""
    if not known_encodings:
        return 0.0

    # Hitung distance dengan semua known encodings
    distances = face_recognition.face_distance(known_encodings, face_encoding)

    # Quality score berdasarkan distance terkecil
    min_distance = min(distances)
    quality_score = 1.0 - min_distance

    return quality_score