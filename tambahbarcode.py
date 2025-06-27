import barcode
from barcode.writer import ImageWriter

# 1. Data yang ingin diubah jadi barcode (bisa angka, teks, dsb.)
data = "123456789012"

# 2. Pilih format barcode (EAN13, Code128, dll). Code128 cocok untuk alfanumerik.
barcode_format = barcode.get_barcode_class('code128')

# 3. Buat barcode
barcode_image = barcode_format(data, writer=ImageWriter())

# 4. Simpan barcode ke file (otomatis jadi PNG)
filename = barcode_image.save("barcode_otomatis")

print(f"Barcode berhasil dibuat: {filename}.png")
