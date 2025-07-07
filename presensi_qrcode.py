import cv2
import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime
import os
import time

# ========== 1. Pastikan file data mahasiswa tersedia ==========
if not os.path.exists('data_mahasiswa.txt'):
    print("Error: File data_mahasiswa.txt tidak ditemukan.")
    exit()

# ========== 2. Baca data mahasiswa (format: NIM,Nama) ==========
with open('data_mahasiswa.txt') as f:
    try:
        daftar_mahasiswa = dict(line.strip().split(',') for line in f if ',' in line)
    except ValueError:
        print("Error: Format data_mahasiswa.txt harus: NIM,Nama")
        exit()

# ========== 3. Persiapan Kamera ==========
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Kamera tidak terbuka.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

presensi_tercatat = set()            # Mencegah duplikat presensi
scan_times = {}                      # Menyimpan waktu pemindaian terakhir
DELAY_WAKTU = 3                      # Detik menahan warna hijau sebelum kuning

# ========== 4. Loop Presensi ==========
while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca dari kamera.")
        break

    for barcode in decode(img): 
        data = barcode.data.decode('utf-8').strip()  # isi QR = NIM

        if data in daftar_mahasiswa:
            nama = daftar_mahasiswa[data]
            waktu_sekarang = time.time()

            # ========== Pertama kali hadir ==========
            if data not in presensi_tercatat:
                print(f"QR Dikenali: {data} (Valid)")
                waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{nama} ({data}) hadir pada {waktu}")

                presensi_tercatat.add(data)
                scan_times[data] = waktu_sekarang

                with open('log_presensi.csv', 'a') as f:
                    f.write(f"{data},{nama},{waktu}\n")

                color = (0, 255, 0)  # Hijau
                output = f"Hadir: {nama}"

            # ========== Sudah hadir, dalam delay ==========
            elif waktu_sekarang - scan_times.get(data, 0) < DELAY_WAKTU:
                color = (0, 255, 0)  # Tetap hijau
                output = f"Hadir: {nama}"

            # ========== Sudah hadir, lewat delay ==========
            else:
                color = (0, 255, 255)  # Kuning
                output = f"Sudah hadir: {nama}"

        else:
            print(f"QR Dikenali: {data} (Tidak valid, tidak ada di daftar_mahasiswa)")
            color = (0, 0, 255)  # Merah
            output = f"Tidak dikenali: {data}"

        # Gambar bounding box dan teks
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, color, 5)

        x, y, w, h = barcode.rect
        cv2.putText(img, output, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # ========== 5. Tampilkan hasil kamera ==========
    cv2.imshow('Presensi Kelas', img)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ========== 6. Tutup Kamera ==========
cap.release()
cv2.destroyAllWindows()
