"""
CSV Logger Module untuk Face Recognition System
Mencatat log deteksi wajah ke file CSV
"""

import csv
import os
from datetime import datetime
import pytz
import pandas as pd

class CSVLogger:
    def __init__(self, log_file="face_detection_logs.csv"):
        self.log_file = log_file
        self.setup_csv_file()
    
    def setup_csv_file(self):
        """Setup CSV file dengan header jika belum ada"""
        try:
            # Cek apakah file sudah ada
            if not os.path.exists(self.log_file):
                # Buat file baru dengan header
                with open(self.log_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        'Nama',
                        'Hari', 
                        'Tanggal',
                        'Jam'
                    ])
                print(f"✅ File CSV log dibuat: {self.log_file}")
            else:
                print(f"📁 File CSV log sudah ada: {self.log_file}")
                
        except Exception as e:
            print(f"❌ Error setup CSV file: {e}")
    
    def log_detection(self, name, confidence=None, location="Camera-1", status="Detected"):
        """Log deteksi wajah ke CSV file (simplified version)"""
        try:
            # Get current time in Jakarta timezone
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            now = datetime.now(jakarta_tz)
            
            # Prepare simplified data (nama, hari, tanggal, jam)
            log_data = [
                name,
                now.strftime('%A'),  # Day name (Monday, Tuesday, etc.)
                now.strftime('%Y-%m-%d'),  # Date (YYYY-MM-DD)
                now.strftime('%H:%M:%S')   # Time (HH:MM:SS)
            ]
            
            # Write to CSV
            with open(self.log_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(log_data)
            
            print(f"📊 CSV log berhasil: {name} - {now.strftime('%A, %Y-%m-%d %H:%M:%S')}")
            return True
            
        except Exception as e:
            print(f"❌ Error logging ke CSV: {e}")
            return False
    
    def get_today_logs(self):
        """Ambil log hari ini dari CSV"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            # Read CSV file
            df = pd.read_csv(self.log_file)
            
            # Get today's date
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            today = datetime.now(jakarta_tz).strftime('%Y-%m-%d')
            
            # Filter for today's logs
            today_logs = df[df['Tanggal'] == today]
            
            return today_logs.to_dict('records')
            
        except Exception as e:
            print(f"❌ Error membaca CSV: {e}")
            return []
    
    def get_logs_by_date(self, date):
        """Ambil log berdasarkan tanggal tertentu (format: YYYY-MM-DD)"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            df = pd.read_csv(self.log_file)
            date_logs = df[df['Tanggal'] == date]
            
            return date_logs.to_dict('records')
            
        except Exception as e:
            print(f"❌ Error membaca CSV untuk tanggal {date}: {e}")
            return []
    
    def get_logs_by_name(self, name):
        """Ambil semua log untuk nama tertentu"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            df = pd.read_csv(self.log_file)
            name_logs = df[df['Nama'] == name]
            
            return name_logs.to_dict('records')
            
        except Exception as e:
            print(f"❌ Error membaca CSV untuk nama {name}: {e}")
            return []
    
    def get_summary_stats(self):
        """Dapatkan statistik ringkasan dari log"""
        try:
            if not os.path.exists(self.log_file):
                return {}
            
            df = pd.read_csv(self.log_file)
            
            # Get today's date
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            today = datetime.now(jakarta_tz).strftime('%Y-%m-%d')
            
            # Calculate statistics
            stats = {
                'total_detections': len(df),
                'today_detections': len(df[df['Tanggal'] == today]),
                'unique_people': df['Nama'].nunique(),
                'most_detected_person': df['Nama'].mode().iloc[0] if len(df) > 0 else 'N/A',
                'most_active_day': df['Hari'].mode().iloc[0] if len(df) > 0 else 'N/A',
                'last_detection': df['Tanggal'].iloc[-1] if len(df) > 0 else 'N/A'
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Error menghitung statistik: {e}")
            return {}
    
    def export_to_excel(self, filename=None):
        """Export CSV log ke Excel file"""
        try:
            if not os.path.exists(self.log_file):
                print("❌ File CSV tidak ditemukan")
                return False
            
            if not filename:
                jakarta_tz = pytz.timezone('Asia/Jakarta')
                now = datetime.now(jakarta_tz)
                filename = f"face_detection_logs_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Read CSV and save as Excel
            df = pd.read_csv(self.log_file)
            df.to_excel(filename, index=False, sheet_name='Face Detection Logs')
            
            print(f"✅ Log berhasil di-export ke: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error export ke Excel: {e}")
            return False
    
    def clear_old_logs(self, days=30):
        """Hapus log yang lebih lama dari jumlah hari tertentu"""
        try:
            if not os.path.exists(self.log_file):
                return False
            
            df = pd.read_csv(self.log_file)
            
            # Calculate cutoff date
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            cutoff_date = datetime.now(jakarta_tz) - pd.Timedelta(days=days)
            cutoff_date_str = cutoff_date.strftime('%Y-%m-%d')
            
            # Filter recent logs
            recent_logs = df[df['Tanggal'] >= cutoff_date_str]
            
            # Save back to CSV
            recent_logs.to_csv(self.log_file, index=False)
            
            removed_count = len(df) - len(recent_logs)
            print(f"🗑️  {removed_count} log lama berhasil dihapus (lebih dari {days} hari)")
            return True
            
        except Exception as e:
            print(f"❌ Error menghapus log lama: {e}")
            return False

# Global CSV logger instance
csv_logger = CSVLogger()
