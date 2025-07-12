# faceRec-lunexis

Capstone Design Project - Real-time Face Recognition System with Advanced Logging & Door Lock Control

## 📋 Deskripsi

Sistem pengenalan wajah real-time yang menggunakan webcam untuk mendeteksi dan mengidentifikasi wajah yang sudah terdaftar. Dilengkapi dengan sistem logging CSV dan Firebase Realtime Database untuk monitoring, serta kontrol solenoid door lock otomatis untuk keamanan pintu.

## ✨ Fitur Utama

- 🎥 **Real-time Face Recognition** - Deteksi wajah secara langsung dari webcam
- 🚪 **Automatic Door Lock Control** - Buka pintu otomatis saat wajah terdaftar terdeteksi
- 📸 **Capture System** - Menambahkan wajah baru dengan capture dari webcam
- 📊 **CSV Logging** - Mencatat siapa yang terdeteksi dan kapan dalam format CSV
- 🔥 **Firebase Integration** - Sinkronisasi data dengan Firebase Realtime Database
- 📈 **Analytics & Reports** - Analisis pola deteksi, statistik, dan laporan
- 📁 **Folder Management** - Organize foto wajah dalam folder terstruktur
- ⚙️ **Multiple Camera Support** - Mendukung berbagai webcam (internal/eksternal)
- 🎛️ **Configurable Settings** - Tolerance dan cooldown yang dapat diatur
- � **GPIO Control** - Kontrol relay dan solenoid via Raspberry Pi GPIO
- �📱 **Monitoring Ready** - Data siap untuk aplikasi monitoring external

## 🔧 Hardware Requirements (Door Lock System)

### For Complete Door Lock System:
- 🍓 **Raspberry Pi 5** (Recommended) atau Pi 3B+/4
- 🔌 **1-Channel 5V Relay Module (ACTIVE LOW)**
- 🚪 **12V DC Solenoid Door Lock**
- ⚡ **12V DC Power Supply (2A minimum)**
- 🔗 **Jumper wires & breadboard**
- 🔋 **Pi 5: Official 5V 5A USB-C power adapter**

### For Face Recognition Only:
- 💻 **Any computer with webcam**
- 🎥 **USB Webcam (internal atau eksternal)**

### 🚀 **Raspberry Pi 5 Advantages:**
- **15-25 FPS** face recognition (vs 8-12 FPS on Pi 4)
- **Enhanced GPIO performance** (0.1ms response time)
- **Better power efficiency**
- **Multiple camera support**
- **AI acceleration ready**

## 🛠️ Instalasi

### Prerequisites

- Python 3.7+
- Webcam (internal atau eksternal)
- Koneksi internet (untuk Firebase)

### Setup Environment

```bash
# Clone repository
git clone https://github.com/yunanyuansyah/faceRec-lunexis.git
cd faceRec-lunexis

# Buat virtual environment
python -m venv facerecenv

# Aktifkan virtual environment
# Windows:
facerecenv\Scripts\activate
# Linux/Mac:
source facerecenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Setup Firebase (Opsional)

1. Ikuti panduan di `FIREBASE_SETUP.md`
2. Download service account key dari Firebase Console
3. Rename menjadi `firebase-service-account.json`
4. Letakkan di folder project

## 📂 Struktur Project

```
faceRec-lunexis/
├── 🎥 Face Recognition Core
│   ├── facePI.py                       # Program utama face recognition + door lock
│   ├── csv_logger.py                   # Module CSV logging
│   ├── firebase_config.py              # Module Firebase integration
│   └── known_faces/                    # Folder foto wajah terdaftar
│       ├── obama.jpg
│       ├── biden.jpg
│       └── yunan.jpg
├── 🚪 Door Lock System
│   ├── door_controller.py              # Module kontrol solenoid door lock (ACTIVE LOW)
│   ├── test_door_controller.py         # Test script untuk door controller
│   ├── test_active_low_relay.py        # Test script khusus active low relay
│   ├── start_system.sh                 # Startup script dengan hardware check
│   ├── start_pi5_system.sh             # Pi 5 optimized startup script
│   ├── install_pi5.sh                  # Automated Pi 5 installation
│   ├── DOOR_LOCK_SETUP.md             # Panduan setup hardware door lock
│   └── PI5_SETUP_GUIDE.md             # Raspberry Pi 5 specific guide
├── 📊 Logging & Analytics
│   ├── log_analyzer.py                 # Tool analisis log
│   ├── test_logging.py                 # Test script untuk logging
│   ├── view_log.py                     # Script lihat log CSV
│   └── face_detection_logs.csv         # File log CSV (auto-generated)
├── 🔧 Utilities
│   ├── organize_photos.py              # Script organize foto
│   ├── manage_faces.py                 # Script kelola wajah
│   ├── detect_cameras.py               # Script deteksi kamera
│   └── test_yunan_face.py              # Script test deteksi wajah
├── 🔥 Firebase Integration
│   ├── firebase-service-account.json   # Firebase credentials (setup required)
│   └── FIREBASE_SETUP.md               # Panduan setup Firebase
└── 📋 Documentation
    ├── README.md                       # Dokumentasi utama
    ├── requirements.txt                # Dependencies
    └── SECURITY_GUIDE.md               # Panduan keamanan
```
## 🚀 Cara Penggunaan

### 1. Setup Hardware (Untuk Door Lock System)

**Raspberry Pi 5 Quick Install:**
```bash
# Automated installation untuk Pi 5
bash install_pi5.sh

# Manual setup
pip install -r requirements.txt
```

**Test Active Low Relay:**
```bash
# Test active low relay specifically
python3 test_active_low_relay.py

# Verify relay type
python3 test_active_low_relay.py 2
```

**Hardware Setup Guides:**
- `PI5_SETUP_GUIDE.md` - Panduan lengkap Raspberry Pi 5
- `DOOR_LOCK_SETUP.md` - Setup hardware solenoid lock

**Quick Setup:**
```bash
# Test door controller hardware
python3 test_door_controller.py

# Start with Pi 5 optimizations
bash start_pi5_system.sh
```

### 2. Face Recognition Only (Tanpa Door Lock)

```bash
# Jalankan tanpa door lock (comment door controller imports)
python3 facePI.py
```

### 3. Jalankan Program Utama (Full System)
```bash
python facePI.py
```

### 4. Kontrol Keyboard

Saat program berjalan, gunakan keyboard untuk kontrol:

**Basic Controls:**
- **'X'** - Keluar dari program
- **'C'** - Capture foto untuk wajah baru
- **'S'** - Simpan wajah yang sudah di-capture
- **'D'** - Toggle debug mode (tampilkan confidence values)
- **'L'** - Tampilkan log deteksi hari ini
- **'R'** - Tampilkan statistik deteksi

**Door Lock Controls:**
- **'U'** - Manual unlock door (5 detik)
- **'K'** - Force lock door immediately
- **'T'** - Test door controller status

### 5. Automatic Door Operation

**Ketika wajah terdaftar terdeteksi:**
1. 🔓 Pintu otomatis unlock selama 5 detik
2. 📝 Deteksi di-log ke CSV dan Firebase
3. 🔒 Pintu otomatis lock kembali
4. ⏱️ Cooldown 30 detik antara deteksi yang sama

### 6. Menambahkan Wajah Baru

**Metode 1: Via Capture Webcam**
1. Posisikan wajah di depan kamera
2. Tekan 'C' untuk capture
3. Tekan 'S' untuk save
4. Masukkan nama saat diminta

**Metode 2: Via File Foto**
1. Letakkan foto di folder `known_faces/`
2. Format nama: `NamaOrang.jpg`
3. Restart program untuk memuat foto baru

### 7. Testing Door Controller

**Test Hardware:**
```bash
# Test basic functionality
python3 test_door_controller.py

# Interactive test mode
python3 test_door_controller.py 5
```

**Test Active Low Relay:**
```bash
# Test active low relay specifically
python3 test_active_low_relay.py

# Verify relay type
python3 test_active_low_relay.py 2
```

**Test Commands:**
- Test Mode 1: Basic functionality
- Test Mode 2: Multiple unlocks
- Test Mode 3: Force lock
- Test Mode 4: GPIO simulation
- Test Mode 5: Interactive mode

### 8. Melihat dan Menganalisis Log

**Lihat Log Hari Ini:**
```bash
# Dalam program, tekan 'L'
# Atau jalankan analyzer
python log_analyzer.py
```

**Analisis Mendalam:**
```bash
# Menu interaktif lengkap
python log_analyzer.py

# Test logging system
python test_logging.py
```

## 📊 Fitur Logging

### CSV Logging
- **File**: `face_detection_logs.csv`
- **Format**: ID, Nama, Tanggal, Hari, Waktu, Timestamp, Confidence, Lokasi, Status
- **Auto-generated**: File dibuat otomatis saat program pertama kali jalan

### Firebase Realtime Database
- **Real-time sync**: Data langsung tersinkronisasi
- **Structure**: JSON format dengan timestamp
- **Monitoring ready**: Siap untuk aplikasi monitoring

### Data yang Dicatat
- 👤 **Nama orang** yang terdeteksi
- 📅 **Tanggal dan waktu** deteksi
- 🎯 **Confidence level** (tingkat kepercayaan)
- 📍 **Lokasi kamera** (configurable)
- ✅ **Status** (Recognized/Unrecognized)

## 📈 Analytics & Reports

### Statistik yang Tersedia
- Total deteksi per hari/minggu/bulan
- Orang yang paling sering terdeteksi
- Pola waktu deteksi (jam tersibuk)
- Tingkat akurasi recognisi
- Trend aktivitas

### Contoh Output Analisis

```
📊 STATISTIK DETEKSI HARI INI
================================
Total deteksi: 45
Orang terdeteksi: 8 unique
Paling sering: John Doe (12x)
Jam tersibuk: 09:00 (8 deteksi)
Tingkat akurasi: 92.3%

⏰ POLA PER JAM:
08:00 | ████████ 8
09:00 | ████████████ 12
10:00 | ██████ 6
11:00 | ████████████████ 16
...
```

## 🔧 Konfigurasi

### Door Lock Settings dalam `door_controller.py`
```python
# GPIO pin untuk relay control (default: pin 18)
relay_pin = 18

# Durasi pintu terbuka dalam detik (default: 5)
lock_duration = 5

# Inisialisasi door controller
door_controller = initialize_door_controller(
    relay_pin=18, 
    lock_duration=5
)
```

### Face Recognition Settings dalam `facePI.py`
```python
# Cooldown antara log untuk orang yang sama (detik)
log_cooldown = 30

# Threshold confidence untuk logging
detection_confidence_threshold = 0.6

# Tolerance untuk face recognition
tolerance = 0.6
```

### Settings Firebase dalam `firebase_config.py`
```python
# URL Firebase Realtime Database
database_url = "https://your-project-name-default-rtdb.firebaseio.com/"

# Path ke service account file
service_account_path = "firebase-service-account.json"
```

### 🍓 **Raspberry Pi 5 Performance Optimization:**

```python
# Pi 5 optimized settings dalam facePI.py
FACE_DETECTION_SCALE = 0.25    # Pi 5 dapat handle resolusi lebih tinggi
PROCESS_EVERY_FRAME = True     # Pi 5 dapat proses setiap frame
DETECTION_TOLERANCE = 0.5      # Deteksi lebih sensitif
MULTI_THREADING = True         # Gunakan multi-core Pi 5
```

### Pi 5 vs Other Models Performance:
| Model | FPS | GPIO Response | Recommended Use |
|-------|-----|---------------|-----------------|
| Pi 3B+ | 3-5 FPS | ~1ms | Basic |
| Pi 4 | 8-12 FPS | ~0.5ms | Standard |
| Pi 5 | 15-25 FPS | ~0.1ms | Professional |

## 📱 Integrasi dengan Aplikasi Monitoring

### Struktur Data Firebase
```json
{
  "face_detection_logs": {
    "auto-key-1": {
      "name": "John Doe",
      "timestamp": "2025-01-11T10:30:45+07:00",
      "date": "2025-01-11",
      "time": "10:30:45",
      "day_of_week": "Saturday",
      "confidence": 0.85,
      "location": "Camera-1",
      "created_at": 1641873045.123
    }
  }
}
```

### Query Data untuk Aplikasi

**JavaScript (Web App):**
```javascript
// Get today's logs
const today = new Date().toISOString().split('T')[0];
const logsRef = ref(database, 'face_detection_logs');
const todayQuery = query(logsRef, orderByChild('date'), equalTo(today));

onValue(todayQuery, (snapshot) => {
  const data = snapshot.val();
  // Process data for your app
});
```

**Python (Backend):**
```python
from firebase_admin import db

# Get logs for specific person
ref = db.reference('face_detection_logs')
logs = ref.order_by_child('name').equal_to('John Doe').get()
```

## 🔍 Troubleshooting

### Common Issues

**1. "No faces found in known_faces folder"**
- Pastikan ada foto di folder `known_faces/`
- Format yang didukung: .jpg, .jpeg, .png, .bmp
- Pastikan foto berisi wajah yang jelas

**2. "Firebase tidak terhubung"**
- Cek file `firebase-service-account.json` exists
- Pastikan URL database benar di `firebase_config.py`
- Cek koneksi internet

**3. "Webcam tidak terdeteksi"**
- Ubah parameter camera index di `cv2.VideoCapture(0)` ke 1, 2, dst
- Jalankan `detect_cameras.py` untuk cek kamera available

**4. "Module not found"**
- Jalankan `pip install -r requirements.txt`
- Pastikan virtual environment aktif

### Test dan Debug

```bash
# Test logging system
python test_logging.py

# Test camera detection
python detect_cameras.py

# Debug face recognition
python facePI.py  # lalu tekan 'D' untuk debug mode
```

1. Jalankan program
2. Posisikan wajah di depan kamera
3. Tekan 'c' untuk capture
4. Tekan 's' untuk save
5. Masukkan nama orang

**Metode 2: Manual**

1. Letakkan foto di folder `known_faces/`
2. Rename file sesuai nama (contoh: `John.jpg`)
3. Restart program

## 🔧 Tools Tambahan

### Organize Photos

```bash
python organize_photos.py
```

Memindahkan semua foto wajah ke folder `known_faces/`

### Manage Faces

```bash
python manage_faces.py
```

Melihat status semua wajah terdaftar dan validasinya

### View Log

```bash
python view_log.py
```

Melihat log deteksi dalam format yang mudah dibaca

### Detect Cameras

```bash
python detect_cameras.py
```

Mendeteksi kamera yang tersedia di sistem

## 📊 Format CSV Log

File `face_detections.csv` berisi:

- **Nama** - Nama orang yang terdeteksi
- **Tanggal** - Tanggal deteksi (YYYY-MM-DD)
- **Waktu** - Waktu deteksi (HH:MM:SS)
- **Timestamp_Lengkap** - Timestamp lengkap

## ⚙️ Konfigurasi

### Mengubah Kamera

Edit `faceRec.py`, ubah line:

```python
video_capture = cv2.VideoCapture(1)  # Ganti angka sesuai kamera
```

### Mengubah Tolerance

Edit tolerance di `faceRec.py`:

```python
tolerance = 0.65  # Nilai 0.4-0.7 (lebih rendah = lebih ketat)
```

### Mengubah Cooldown

Gunakan keyboard '+' dan '-' saat program berjalan, atau edit:

```python
logging_cooldown = 10  # Detik
```

## 🎯 Spesifikasi Teknis

- **Face Recognition Library**: face_recognition (dlib-based)
- **Computer Vision**: OpenCV
- **Platform**: Windows, Linux, macOS
- **Format Gambar**: JPG, JPEG, PNG, BMP
- **Resolusi**: Otomatis menyesuaikan webcam

## 🐛 Troubleshooting

### Error: "No module named 'face_recognition'"

```bash
pip install face-recognition
```

### Error: "Failed to grab frame from webcam"

1. Pastikan webcam tidak digunakan aplikasi lain
2. Coba ganti index kamera di kode
3. Jalankan `python detect_cameras.py` untuk cek kamera

### Error: "No such file or directory: 'yunan.jpg'"

File tidak masalah, program akan skip dan lanjut dengan wajah lain

### Wajah tidak terdeteksi

1. Pastikan pencahayaan cukup
2. Wajah menghadap kamera
3. Jarak optimal 0.5-2 meter dari kamera

## 📝 TODO / Future Features

- [ ] GUI interface
- [ ] Database integration
- [ ] Multiple face per person
- [ ] Face recognition from video files
- [ ] Real-time attendance system
- [ ] Web interface

## 👥 Kontributor

- **Yunan Yuansyah** - Developer

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- Repository: https://github.com/yunanyuansyah/faceRec-lunexis
- Issues: https://github.com/yunanyuansyah/faceRec-lunexis/issues
