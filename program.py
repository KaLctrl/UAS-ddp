import pwinput
import os
from datetime import datetime, time

# Data awal
data_barang = {
    "pagi": [
        {"id": 1, "nama": "assasin's creed unity", "harga": 10},
        {"id": 2, "nama": "assasin's creed odyssey", "harga": 5}
    ],
    "siang": [
        {"id": 3, "nama": "watch dogs 2", "harga": 15},
        {"id": 4, "nama": "watch dogs legion", "harga": 20}
    ],
    "malam": [
        {"id": 5, "nama": "far cry 6", "harga": 25},
        {"id": 6, "nama": "far cry new dawn", "harga": 18}
    ]
}

data_voucher = [
    {"kode": "DISKON10", "diskon": 10, "masa_berlaku": "2024-12-31", "digunakan": False}
]

data_user = {}

# Fungsi untuk registrasi
def registrasi():
    username = input("Masukkan username: ")
    if username in data_user:
        print("Username sudah terdaftar. Silakan coba username lain.")
        return
    
    password = pwinput.pwinput("Masukkan password: ")
    uang = {
        "gold": 100,  # Saldo awal
        "gems": 50,
        "diamond": 20
    }
    
    data_user[username] = {"password": password, "uang": uang}
    print("Registrasi berhasil!")

# Fungsi untuk login
def login():                                                                               
    attempts = 0
    while attempts < 3:
        username = input("Masukkan username: ")
        password = pwinput.pwinput("Masukkan password: ")
        
        if username in data_user and data_user[username]['password'] == password:
            print(f"Selamat datang, {username}!")
            return username
        else:
            attempts += 1
            print("Username atau password salah. Coba lagi.")
    
    print("Akun terkunci setelah 3 kali percobaan salah.")
    return None

# Fungsi untuk menampilkan barang berdasarkan waktu
def tampil_barang():
    now = datetime.now()
    if time(6, 0) <= now.time() < time(12, 0):
        return data_barang['pagi']
    elif time(12, 0) <= now.time() < time(18, 0):
        return data_barang['siang']
    else:
        return data_barang['malam']

# Fungsi untuk membeli barang
def beli_barang(username):
    barang = tampil_barang()
    print("Barang yang tersedia:")
    for item in barang:
        print(f"ID: {item['id']}, Nama: {item['nama']}, Harga: {item['harga']}")

    id_barang = int(input("Masukkan ID barang yang ingin dibeli: "))
    voucher = input("Masukkan kode voucher (jika ada): ")
    
    item_dipilih = next((item for item in barang if item['id'] == id_barang), None)
    
    if item_dipilih:
        harga = item_dipilih['harga']
        
        # Cek voucher
        if voucher:
            voucher_valid = next((v for v in data_voucher if v['kode'] == voucher and not v['digunakan']), None)
            if voucher_valid:
                # Cek masa berlaku voucher
                if datetime.now().date() <= datetime.strptime(voucher_valid['masa_berlaku'], "%Y-%m-%d").date():
                    harga -= voucher_valid['diskon']
                    voucher_valid['digunakan'] = True
                    print(f"Voucher digunakan. Diskon {voucher_valid['diskon']}.")
                else:
                    print("Voucher kadaluarsa.")
            else:
                print("Voucher tidak valid atau sudah digunakan.")

        # Cek saldo
        total_uang = sum(data_user[username]['uang'].values())
        if total_uang >= harga:
            print(f"Pembelian berhasil! Anda membeli {item_dipilih['nama']} seharga {harga}.")
            # Kurangi saldo
            for k in data_user[username]['uang']:
                if data_user[username]['uang'][k] >= harga:
                    data_user[username]['uang'][k] -= harga
                    break
        else:
            print("Saldo tidak cukup untuk melakukan pembelian.")
    else:
        print("Barang tidak ditemukan.")

# Fungsi untuk melakukan top-up
def topup(username):
    jumlah = int(input("Masukkan jumlah top-up: "))
    if jumlah > 0:
        data_user[username]['uang']['gold'] += jumlah
        print(f"Top-up berhasil! Saldo gold Anda sekarang: {data_user[username]['uang']['gold']}")
    else:
        print("Jumlah top-up harus lebih dari 0.")

# Fungsi untuk upgrade role ke VIP
def upgrade_role(username):
    biaya_vip = 50  # Biaya untuk upgrade ke VIP
    if data_user[username]['uang']['gold'] >= biaya_vip:
        data_user[username]['uang']['gold'] -= biaya_vip
        data_user[username]['role'] = 'vip'
        print(f"Selamat! Anda telah berhasil upgrade ke role VIP. Saldo gold Anda sekarang: {data_user[username]['uang']['gold']}")
    else:
        print("Saldo tidak cukup untuk upgrade ke VIP.")

# Menu utama
def main():
    while True:
        print("\n=== Toko Aplikasi Game ===")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih opsi (1/2/3): ")

        if pilihan == '1':
            registrasi()
        elif pilihan == '2':
            username = login()
            if username:
                while True:
                    print("\n=== Menu Pembelian ===")
                    print("1. Tampilkan Barang")
                    print("2. Beli Barang")
                    print("3. Top-Up Saldo")
                    print("4. Upgrade ke VIP")
                    print("5. Logout")
                    menu = input("Pilih opsi (1/2/3/4/5): ")

                    if menu == '1':
                        barang = tampil_barang()
                        print("Barang yang tersedia:")
                        for item in barang:
                            print(f"ID: {item['id']}, Nama: {item['nama']}, Harga: {item['harga']}")
                    elif menu == '2':
                        beli_barang(username)
                    elif menu == '3':
                        topup(username)
                    elif menu == '4':
                        upgrade_role(username)
                    elif menu == '5':
                        print("Anda telah logout.")
                        break
                    else:
                        print("Opsi tidak valid. Silakan coba lagi.")
        elif pilihan == '3':
            print("Terima kasih telah menggunakan aplikasi ini.")
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

# Menjalankan aplikasi
if __name__ == "__main__":
    main()
        
