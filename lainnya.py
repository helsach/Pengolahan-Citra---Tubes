import qrcode
import os

# NIM untuk pengujian (tidak ada di data_mahasiswa.txt)
nim_uji = "4.33.23.1.99"
nama_uji = "Test Error"

# Buat folder untuk menyimpan QR code (jika belum ada)
output_folder = 'qrcodes'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Buat objek QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Tambahkan NIM sebagai data QR code
qr.add_data(nim_uji)
qr.make(fit=True)

# Buat gambar QR code
img = qr.make_image(fill_color="black", back_color="white")

# Bersihkan nama file dari karakter yang tidak valid
safe_nama = nama_uji.replace(' ', '_').replace(',', '').replace('/', '_')
filename = f"{output_folder}/{nim_uji}_{safe_nama}.png"

# Simpan QR code sebagai file PNG
img.save(filename)
print(f"QR code untuk {nama_uji} ({nim_uji}) disimpan sebagai {filename}")