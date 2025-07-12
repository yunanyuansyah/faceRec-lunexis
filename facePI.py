import face_recognition
import cv2
import numpy as np
import os
import time
from datetime import datetime
import pytz

# Import logging modules
from csv_logger import csv_logger
from firebase_config import firebase_logger

# Import door controller for solenoid lock
from door_controller import initialize_door_controller, unlock_door_for_person, cleanup_door_controller

def get_person_name():
    """Function to get person name for new face"""
    try:
        # Simple method - you can enhance this with GUI later
        name = input("\n🔸 Masukkan nama untuk wajah baru (atau tekan Enter untuk nama otomatis): ").strip()
        if not name:
            timestamp = int(time.time())
            name = f"Person_{timestamp}"
        return name
    except:
        # Fallback if input fails
        timestamp = int(time.time())
        return f"Person_{timestamp}"

def load_known_faces_from_folder(folder_path="known_faces"):
    """Load all known faces from a folder structure"""
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(folder_path):
        print(f"📁 Folder {folder_path} tidak ditemukan, membuatnya...")
        os.makedirs(folder_path)
        return known_face_encodings, known_face_names
    
    print(f"📂 Memuat wajah dari folder: {folder_path}")
    
    # Get all image files in the folder (avoid duplicates)
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(folder_path, file))
    
    for image_path in image_files:
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) > 0:
                # Use filename (without extension) as the person's name
                filename = os.path.basename(image_path)
                name = os.path.splitext(filename)[0]
                
                # Add to known faces
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(name)
                
                print(f"✅ Wajah dimuat: {name} dari {filename}")
            else:
                print(f"⚠️  Tidak ada wajah ditemukan di: {os.path.basename(image_path)}")
                
        except Exception as e:
            print(f"❌ Error memuat {os.path.basename(image_path)}: {e}")
    
    print(f"📊 Total {len(known_face_encodings)} wajah berhasil dimuat dari folder")
    return known_face_encodings, known_face_names

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(1)

# Load known faces from folder
print("🔄 Memuat wajah terdaftar...")
known_face_encodings, known_face_names = load_known_faces_from_folder("known_faces")

# Initialize door controller system
print("🔄 Menginisialisasi sistem kontrol pintu...")
door_controller = initialize_door_controller(relay_pin=18, lock_duration=5)
print("🚪 Door controller initialized - GPIO pin 18, unlock duration 5 seconds")

# Display information about loaded faces
if len(known_face_encodings) == 0:
    print("❌ Tidak ada wajah yang berhasil dimuat!")
    print("💡 Letakkan foto wajah di folder 'known_faces/' dengan format:")
    print("   - Format yang didukung: .jpg, .jpeg, .png, .bmp")
    print("   - Nama file akan menjadi nama orang (contoh: John.jpg)")
    print("   - Pastikan foto berisi wajah yang jelas")
    print("🎥 Anda tetap dapat menambah wajah menggunakan webcam (tekan 'C' untuk capture)")

print(f"👥 Total wajah terdaftar: {len(known_face_names)}")
if known_face_names:
    print(f"📋 Daftar wajah: {', '.join(known_face_names)}")
print()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
debug_mode = False  # Debug mode to show distance values

# Logging variables
last_logged_faces = {}  # Track last log time for each person
log_cooldown = 30  # Seconds between logs for same person
detection_confidence_threshold = 0.6  # Confidence threshold for logging

# Display startup information
print("🎥 FACE RECOGNITION SYSTEM WITH LOGGING")
print("=" * 50)
print("📂 Sistem memuat wajah dari folder 'known_faces/'")
print("� Log deteksi akan disimpan ke CSV dan Firebase")
print("�💡 Untuk menambah wajah baru:")
print("   1. Tekan 'C' untuk capture dari webcam, lalu 'S' untuk save")
print("   2. Atau letakkan foto langsung di folder 'known_faces/'")
print()
print("Keyboard Controls:") 
print("  X      - Exit system")
print("  C      - Capture photo for new face")
print("  S      - Save captured face")
print("  D      - Toggle debug mode (show distance values)")
print("  L      - Show today's detection logs")
print("  R      - Show detection statistics")
print("  U      - Manual unlock door (5 seconds)")
print("  K      - Force lock door immediately")
print("  T      - Test door controller")
print("=" * 50)
print("📹 Webcam active... Use keyboard controls as needed")
print()

# Test Firebase connection
if firebase_logger.is_connected:
    print("🔥 Firebase: Terhubung")
else:
    print("⚠️  Firebase: Tidak terhubung (hanya CSV yang akan digunakan)")
print(f"📊 CSV Logger: Aktif - File: {csv_logger.log_file}")
print()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if not ret or frame is None:
        print("Failed to grab frame from webcam. Exiting...")
        break

    # Keep a clean copy of the original frame for capture (without any overlay)
    clean_frame = frame.copy()
    
    # Create a display frame that will have all the overlays
    display_frame = frame.copy()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(display_frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        else:
            face_encodings = []

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s) with custom tolerance
            tolerance = 0.6  # Lower tolerance for better matching (default is 0.6)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
            name = "Unknown"
            confidence = None

            # Use the known face with the smallest distance to the new face
            if len(known_face_encodings) > 0:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                best_distance = face_distances[best_match_index]
                
                # Check if the best match is within our tolerance and show distance for debugging
                if best_distance <= tolerance:
                    name = known_face_names[best_match_index]
                    confidence = 1.0 - best_distance  # Convert distance to confidence
                    
                    # Log detection if cooldown period has passed
                    current_time = time.time()
                    if name not in last_logged_faces or (current_time - last_logged_faces[name]) >= log_cooldown:
                        # Log to CSV (simplified: hanya nama, hari, tanggal)
                        csv_logger.log_detection(name=name)
                        
                        # Log to Firebase (simplified: hanya nama, hari, tanggal)
                        firebase_logger.log_detection(name=name)
                        
                        # 🚪 UNLOCK DOOR FOR RECOGNIZED PERSON
                        unlock_success = unlock_door_for_person(name)
                        if unlock_success:
                            print(f"🔓 Selamat Datang !, {name}!")
                        
                        # Update last logged time
                        last_logged_faces[name] = current_time
                    
                    if debug_mode:
                        print(f"✅ Match: {name} (confidence: {confidence:.3f}, distance: {best_distance:.3f})")
                else:
                    # Unknown face detected
                    if debug_mode:
                        print(f"❌ No match - closest: {known_face_names[best_match_index]} (distance: {best_distance:.3f}, tolerance: {tolerance})")
                    
                    # Log unknown face detection (with cooldown)
                    current_time = time.time()
                    if "Unknown" not in last_logged_faces or (current_time - last_logged_faces["Unknown"]) >= log_cooldown:
                        csv_logger.log_detection(name="Unknown")
                        firebase_logger.log_detection(name="Unknown")
                        last_logged_faces["Unknown"] = current_time

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Choose color based on recognition status
        if name == "Unknown":
            color = (0, 0, 255)  # Red for unknown faces
        else:
            color = (0, 255, 0)  # Green for known faces

        # Draw a box around the face
        cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(display_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(display_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display control instructions on the video
    instructions = [
        "Controls:",
        "X - Exit",
        "C - Capture", 
        "S - Save",
        "D - Debug mode",
        "L - Show logs",
        "R - Statistics",
        "U - Unlock door",
        "K - Lock door",
        "T - Test door"
    ]
    
    y_offset = 30
    for i, instruction in enumerate(instructions):
        color = (255, 255, 255) if i == 0 else (0, 255, 255)  # White for title, yellow for others
        cv2.putText(display_frame, instruction, (10, y_offset + i * 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Show face count and detection info
    cv2.putText(display_frame, f"Faces detected: {len(face_locations)}", (10, display_frame.shape[0] - 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(display_frame, f"Known faces: {len(known_face_names)}", (10, display_frame.shape[0] - 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(display_frame, "Tips: Face camera directly, good lighting", (10, display_frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

    # Show capture mode indicator if in capture mode
    if 'captured_encodings' in locals():
        cv2.putText(display_frame, "CAPTURE MODE - Press 'S' to save", (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        # Add a border to indicate capture mode
        cv2.rectangle(display_frame, (5, 5), (display_frame.shape[1]-5, display_frame.shape[0]-5), (0, 255, 255), 3)

    # Display the resulting image
    cv2.imshow('Video', display_frame)
    
    # Keyboard controls for stopping the system
    key = cv2.waitKey(1) & 0xFF
    
    # Hit 'x' to exit
    if key == ord('x'):
        print("🛑 Sistem dihentikan dengan tombol 'x' (exit)")
        break
    elif key == ord('d'):
        # Toggle debug mode
        debug_mode = not debug_mode
        if debug_mode:
            print("🔍 Debug mode ON - akan menampilkan distance values")
        else:
            print("🔍 Debug mode OFF")
    elif key == ord('l'):
        # Show today's logs
        print("\n📊 LOG DETEKSI HARI INI:")
        print("=" * 50)
        today_logs = csv_logger.get_today_logs()
        if today_logs:
            for i, log in enumerate(today_logs, 1):
                print(f"{i:2d}. {log['Nama']} - {log['Waktu']} ({log['Status']})")
        else:
            print("Tidak ada log hari ini")
        print("=" * 50)
        print()
    elif key == ord('r'):
        # Show statistics
        print("\n📈 STATISTIK DETEKSI:")
        print("=" * 50)
        stats = csv_logger.get_summary_stats()
        if stats:
            print(f"Total deteksi: {stats.get('total_detections', 0)}")
            print(f"Deteksi hari ini: {stats.get('today_detections', 0)}")
            print(f"Jumlah orang unik: {stats.get('unique_people', 0)}")
            print(f"Paling sering terdeteksi: {stats.get('most_detected_person', 'N/A')}")
            print(f"Hari paling aktif: {stats.get('most_active_day', 'N/A')}")
            print(f"Deteksi terakhir: {stats.get('last_detection', 'N/A')}")
        else:
            print("Tidak ada data statistik")
        print("=" * 50)
        print()
    elif key == ord('c'):
        # Capture current frame for adding new face
        if len(face_locations) > 0:
            print("📸 Foto berhasil diambil! Tekan 'S' untuk menyimpan wajah, atau 'C' lagi untuk foto ulang")
            captured_frame = clean_frame.copy()  # Use clean frame without overlays
            captured_locations = face_locations.copy()
            captured_encodings = face_encodings.copy()
        else:
            print("❌ Tidak ada wajah yang terdeteksi! Posisikan wajah Anda di depan kamera dan tekan 'C' lagi")
    elif key == ord('s'):
        # Save captured face to known faces
        if 'captured_encodings' in locals() and len(captured_encodings) > 0:
            print("\n🔄 Menyimpan wajah baru...")
            
            # Get name from user input
            new_name = get_person_name()
            
            # Add the first detected face to known faces
            known_face_encodings.append(captured_encodings[0])
            known_face_names.append(new_name)
            
            # Create known_faces directory if it doesn't exist
            known_faces_dir = "known_faces"
            os.makedirs(known_faces_dir, exist_ok=True)
            
            # Save the captured image to known_faces folder
            filename = os.path.join(known_faces_dir, f"{new_name}.jpg")
            cv2.imwrite(filename, captured_frame)
            
            print(f"✅ Wajah baru berhasil ditambahkan dengan nama: {new_name}")
            print(f"📁 Foto disimpan sebagai: {filename}")
            print(f"👥 Total wajah yang dikenal sekarang: {len(known_face_names)}")
            print("📹 Kembali ke mode deteksi...\n")
            
            # Clear captured data
            del captured_frame, captured_locations, captured_encodings
        else:
            print("❌ Tidak ada foto yang diambil! Tekan 'C' terlebih dahulu untuk mengambil foto")
    elif key == ord('u'):
        # Manual unlock door
        print("🔓 Manual unlock door...")
        unlock_success = unlock_door_for_person("Manual_User")
        if unlock_success:
            print("✅ Door unlocked manually for 5 seconds")
        else:
            print("❌ Failed to unlock door")
    elif key == ord('k'):
        # Force lock door
        print("🔒 Force locking door...")
        if door_controller:
            door_controller.force_lock()
            print("✅ Door force locked")
        else:
            print("❌ Door controller not available")
    elif key == ord('t'):
        # Test door controller
        print("🧪 Testing door controller...")
        if door_controller:
            status = door_controller.get_status()
            print(f"📊 Door Status:")
            print(f"   - Unlocked: {status['is_unlocked']}")
            print(f"   - Relay Pin: {status['relay_pin']}")
            print(f"   - Lock Duration: {status['lock_duration']}s")
            print(f"   - Raspberry Pi: {status['raspberry_pi']}")
            print(f"   - Relay Available: {status['relay_available']}")
        else:
            print("❌ Door controller not available")

# Release handle to the webcam
print("\n🔄 Membersihkan resource...")

# Cleanup door controller
print("🚪 Membersihkan door controller...")
cleanup_door_controller()

video_capture.release()
cv2.destroyAllWindows()
print("✅ Webcam dilepas")
print("✅ Jendela OpenCV ditutup")
print("✅ Door controller dibersihkan")
print("🛑 Sistem face recognition telah dihentikan sepenuhnya")
print("👋 Terima kasih telah menggunakan Face Recognition & Door Lock System!")