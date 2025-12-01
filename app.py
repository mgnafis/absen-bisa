import streamlit as st
import cv2
import face_recognition
import numpy as np
import os
import pickle
from PIL import Image
import time

st.set_page_config(
    page_title="Face Recognition App",
    page_icon="👤",
    layout="wide"
)

def create_directories():
    """Membuat direktori yang diperlukan jika belum ada"""
    directories = [
        "data/known_faces",
        "data/encodings",
        "uploads"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def load_known_encodings():
    """Memuat encoding wajah yang sudah diketahui"""
    encodings_path = "data/encodings/encodings.pkl"
    if os.path.exists(encodings_path):
        with open(encodings_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('encodings', []), data.get('names', [])
    return [], []

def save_encodings(encodings, names):
    """Menyimpan encoding wajah"""
    encodings_path = "data/encodings/encodings.pkl"
    data = {'encodings': encodings, 'names': names}
    with open(encodings_path, 'wb') as f:
        pickle.dump(data, f)

def register_face(image, name):
    """Mendaftarkan wajah baru"""
    try:
        # Convert PIL Image ke OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Deteksi wajah
        face_locations = face_recognition.face_locations(opencv_image, model="hog")

        if len(face_locations) == 0:
            return False, "Tidak ada wajah yang terdeteksi di foto"

        if len(face_locations) > 1:
            return False, "Deteksi lebih dari satu wajah. Harap upload foto dengan satu wajah saja"

        # Encoding wajah
        face_encoding = face_recognition.face_encodings(opencv_image, face_locations)[0]

        # Load encodings yang sudah ada
        known_encodings, known_names = load_known_encodings()

        # Tambahkan encoding baru
        known_encodings.append(face_encoding)
        known_names.append(name)

        # Simpan
        save_encodings(known_encodings, known_names)

        # Simpan foto
        photo_path = f"data/known_faces/{name}.jpg"
        cv2.imwrite(photo_path, opencv_image)

        return True, f"Wajah untuk {name} berhasil didaftarkan"

    except Exception as e:
        return False, f"Error: {str(e)}"

def recognize_faces(frame, known_encodings, known_names):
    """Mengenali wajah dalam frame"""
    try:
        # Deteksi wajah
        face_locations = face_recognition.face_locations(frame, model="hog")
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Bandingkan dengan wajah yang diketahui
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            # Cari wajah yang paling cocok
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            results.append({
                'location': (top, right, bottom, left),
                'name': name
            })

        return results

    except Exception as e:
        st.error(f"Error dalam face recognition: {str(e)}")
        return []

def draw_results(frame, results):
    """Menggambar kotak dan nama pada wajah yang terdeteksi"""
    for result in results:
        top, right, bottom, left = result['location']
        name = result['name']

        # Gambar kotak
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Gambar label
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frame

def main():
    create_directories()

    st.title("👤 Face Recognition System")
    st.markdown("---")

    # Sidebar untuk navigasi
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Pilih Halaman", ["Registrasi Wajah", "Real-time Detection"])

    if page == "Registrasi Wajah":
        st.header("📝 Registrasi Wajah Baru")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Upload Foto")
            uploaded_file = st.file_uploader(
                "Pilih foto wajah",
                type=['jpg', 'jpeg', 'png'],
                help="Upload foto jernih dengan satu wajah saja"
            )

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Foto yang diupload", use_column_width=True)

                name = st.text_input(
                    "Nama Lengkap",
                    placeholder="Masukkan nama orang di foto",
                    help="Nama akan digunakan untuk identifikasi"
                )

                if st.button("🔄 Register Wajah", type="primary"):
                    if name.strip():
                        with st.spinner("Mendaftarkan wajah..."):
                            success, message = register_face(image, name.strip())
                            if success:
                                st.success(message)
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("Silakan masukkan nama terlebih dahulu")

        with col2:
            st.subheader("Daftar Wajah Terdaftar")
            known_encodings, known_names = load_known_encodings()

            if known_names:
                st.write(f"Total wajah terdaftar: {len(known_names)}")

                for i, name in enumerate(known_names):
                    photo_path = f"data/known_faces/{name}.jpg"
                    if os.path.exists(photo_path):
                        st.image(photo_path, caption=name, width=150)
                    else:
                        st.write(f"👤 {name}")
            else:
                st.info("Belum ada wajah yang terdaftar")

    elif page == "Real-time Detection":
        st.header("📹 Real-time Face Detection")

        known_encodings, known_names = load_known_encodings()

        if not known_names:
            st.warning("❌ Belum ada wajah yang terdaftar. Silakan registrasi wajah terlebih dahulu!")
            return

        st.info(f"✅ {len(known_names)} wajah siap untuk deteksi")

        # Camera settings
        st.subheader("Pengaturan Kamera")

        col1, col2 = st.columns([1, 1])
        with col1:
            camera_source = st.selectbox(
                "Sumber Kamera",
                ["Webcam Default", "Upload Video"],
                index=0
            )

        with col2:
            confidence_threshold = st.slider(
                "Threshold Kepercayaan",
                min_value=0.1,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Semakin tinggi, semakin ketat deteksinya"
            )

        if camera_source == "Webcam Default":
            st.subheader("📷 Live Detection")

            # Placeholders
            video_placeholder = st.empty()
            status_placeholder = st.empty()

            if st.button("▶️ Start Detection", type="primary"):
                cap = cv2.VideoCapture(0)

                if not cap.isOpened():
                    st.error("❌ Tidak dapat mengakses kamera. Pastikan kamera terhubung.")
                    return

                st.session_state.detection_active = True

                while st.session_state.detection_active:
                    ret, frame = cap.read()

                    if not ret:
                        st.error("❌ Tidak dapat membaca frame dari kamera")
                        break

                    # Flip frame horizontally (mirror effect)
                    frame = cv2.flip(frame, 1)

                    # Recognize faces
                    results = recognize_faces(frame, known_encodings, known_names)

                    # Draw results
                    frame = draw_results(frame, results)

                    # Convert to RGB for display
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Display
                    video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

                    # Status
                    detected_names = [r['name'] for r in results if r['name'] != 'Unknown']
                    if detected_names:
                        status_placeholder.success(f"✅ Terdeteksi: {', '.join(set(detected_names))}")
                    else:
                        status_placeholder.info("🔍 Tidak ada wajah yang dikenali")

                    # Stop button
                    if st.button("⏹️ Stop Detection"):
                        st.session_state.detection_active = False
                        break

                    time.sleep(0.1)

                cap.release()
                video_placeholder.empty()
                status_placeholder.empty()

        else:
            st.subheader("📁 Video Upload Detection")
            uploaded_video = st.file_uploader(
                "Upload video file",
                type=['mp4', 'avi', 'mov'],
                help="Upload video untuk diproses"
            )

            if uploaded_video is not None:
                temp_video_path = "temp_video.mp4"
                with open(temp_video_path, "wb") as f:
                    f.write(uploaded_video.getbuffer())

                if st.button("▶️ Process Video", type="primary"):
                    cap = cv2.VideoCapture(temp_video_path)
                    video_placeholder = st.empty()

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        results = recognize_faces(frame, known_encodings, known_names)
                        frame = draw_results(frame, results)

                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    cap.release()
                    if os.path.exists(temp_video_path):
                        os.remove(temp_video_path)

if __name__ == "__main__":
    main()