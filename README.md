# 🎭 Face Recognition App

Aplikasi Face Recognition berbasis Streamlit untuk registrasi dan deteksi wajah secara real-time.

## 📋 Fitur

- ✅ Registrasi wajah melalui upload foto
- ✅ Deteksi wajah real-time dengan webcam
- ✅ Deteksi wajah dari video upload
- ✅ Interface yang user-friendly
- ✅ Support multiple faces
- ✅ Threshold kepercayaan yang dapat disesuaikan

## 🏗️ Struktur Folder

```
face_recognition_app/
├── app.py                  # File utama aplikasi Streamlit
├── requirements.txt        # Dependencies Python
├── README.md              # Dokumentasi ini
├── data/                  # Folder untuk data
│   ├── known_faces/       # Foto wajah yang terdaftar
│   └── encodings/         # Encoding wajah (pickle file)
├── uploads/               # Temporary uploads
└── utils/                 # Utility functions
    └── face_utils.py      # Helper functions
```

## 🛠️ Instalasi

### 1. Persyaratan Sistem
- Python 3.8 atau lebih tinggi (direkomendasikan Python 3.8-3.9)
- Webcam (untuk real-time detection)
- OS: Windows, Linux, atau macOS

### 2. Install Dependencies

```bash
# Clone atau download folder face_recognition_app
cd face_recognition_app

# Install dependencies
pip install -r requirements.txt
```

### 3. Install dlib (Windows)

Jika Anda menggunakan Windows, mungkin perlu install dlib secara manual:

```bash
# Untuk Windows (download .whl dari https://pypi.org/project/dlib/#files)
pip install dlib-19.22.99-cp38-cp38-win_amd64.whl  # untuk Python 3.8
# atau
pip install dlib-19.22.99-cp39-cp39-win_amd64.whl  # untuk Python 3.9
```

### 4. Install CMake (jika diperlukan)

```bash
pip install cmake
```

## 🚀 Cara Menjalankan

### Local Development

#### 1. Jalankan Aplikasi

```bash
streamlit run app.py
```

#### 2. Buka Browser

Aplikasi akan otomatis terbuka di browser Anda pada:
```
http://localhost:8501
```

### 🌐 Deploy ke Streamlit Community Cloud

#### 1. Upload ke GitHub
```bash
git init
git add .
git commit -m "Initial commit: Face Recognition App"
git branch -M main
git remote add origin https://github.com/username/face-recognition-app.git
git push -u origin main
```

#### 2. Deploy ke Streamlit
1. Buka [Streamlit Community Cloud](https://share.streamlit.io/)
2. Login dengan GitHub
3. Klik "New app"
4. Pilih repository Anda
5. **Main file path**: `app.py`
6. Klik "Deploy!"

#### 3. File Path Configuration
- **Main file path**: `app.py` ⭐
- **Python version**: Python 3.8+
- **Requirements file**: `requirements.txt` (otomatis terdeteksi)

## 📖 Cara Penggunaan

### 1. Registrasi Wajah

1. Buka aplikasi di browser
2. Pilih menu "Registrasi Wajah" di sidebar
3. Upload foto wajah (format: JPG, JPEG, PNG)
4. Masukkan nama lengkap
5. Klik tombol "Register Wajah"
6. Tunggu proses registrasi selesai

**Tips untuk foto registrasi:**
- Gunakan foto jernih dan terang
- Pastikan hanya ada satu wajah di foto
- Wajah menghadap ke depan
- Tidak menggunakan kacamata atau masker

### 2. Real-time Detection

1. Pilih menu "Real-time Detection" di sidebar
2. Pilih sumber kamera (Webcam Default atau Upload Video)
3. Atur threshold kepercayaan (default: 0.6)
4. Klik "Start Detection"
5. Arahkan kamera ke wajah
6. Sistem akan menampilkan nama jika wajah terdaftar

## ⚙️ Konfigurasi

### Threshold Kepercayaan
- **0.1-0.3**: Sangat sensitif (mungkin false positive)
- **0.4-0.6**: Seimbang (direkomendasikan)
- **0.7-1.0**: Sangat ketat (mungkin false negative)

### Supported Image Formats
- **Input**: JPG, JPEG, PNG
- **Video**: MP4, AVI, MOV

## 🔧 Troubleshooting

### 1. Error: "No face detected"
- Pastikan foto cukup terang
- Pastikan wajah terlihat jelas
- Coba dengan foto yang berbeda

### 2. Error: "Cannot access camera"
- Pastikan webcam terhubung
- Coba restart aplikasi
- Check permission camera di browser

### 3. Install Error (Windows)
Jika mengalami error saat install `face-recognition`:

```bash
# Install dependencies manual
pip install --upgrade pip
pip install numpy
pip install opencv-python
pip install dlib
pip install face-recognition
```

### 4. Performance Issues
- Gunakan Python 3.8 untuk performa terbaik
- Pastikan RAM minimal 4GB
- Gunakan foto dengan resolusi wajar (tidak terlalu besar)

## 📁 File Management

### Data Location
- **Foto wajah**: `data/known_faces/`
- **Encoding data**: `data/encodings/encodings.pkl`
- **Temporary uploads**: `uploads/`

### Backup Data
Untuk backup data wajah:
```bash
# Copy folder data
cp -r data/ backup_data/
```

### Reset Data
Untuk menghapus semua data wajah:
```bash
# Hapus folder data
rm -rf data/
# Aplikasi akan membuat folder baru saat dijalankan
```

## 🔄 Update

Untuk update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## 🐛 Known Issues

1. **MacOS M1/M2**: Mungkin perlu install dependencies manual
2. **Low light**: Face recognition kurang akurat
3. **Multiple faces**: Registrasi hanya support satu wajah per foto
4. **Large images**: Proses lebih lambat untuk foto resolusi tinggi

## 📄 License

Aplikasi ini dibuat untuk tujuan edukasi dan penelitian.

## 🤝 Kontribusi

Silakan kirim pull request untuk improvement atau bug fix.

## 📞 Support

Jika mengalami masalah:
1. Check troubleshooting section
2. Pastikan semua dependencies terinstall dengan benar
3. Gunakan Python 3.8-3.9 untuk compatibility terbaik

---

**Happy Coding! 🎉**