import os
import datetime

# Fungsi untuk membuka data akun dari file
def load_accounts():
    if not os.path.exists('accounts.txt'):
        return {}
    with open('accounts.txt', 'r') as file:
        lines = file.readlines()
        accounts = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 4: 
                acc_number = parts[0]
                balance = float(parts[1])
                pin = parts[2]
                transactions = parts[3:]
                accounts[acc_number] = {'tabungan': balance, 'pin': pin, 'transaksi': transactions}
        return accounts

# Fungsi untuk menghapus akun
def remove_account(accounts):
    account_number = input("Masukkan nama akun yang ingin dihapus: ")
    account_pin = input("Masukkan PIN akun: ")
    if account_number not in accounts:
        return "Akun tidak ditemukan"
    elif accounts[account_number]['pin'] != account_pin:
        return "PIN invalid"
    else:
        del accounts[account_number]
        save_accounts(accounts)
        return f"Akun {account_number} telah dihapus dari catatan"

# Fungsi untuk menyimpan akun ke file data
def save_accounts(accounts):
    with open('accounts.txt', 'w') as file:
        for acc, data in accounts.items():
            file.write(f"{acc} {data['tabungan']} {data['pin']} {' '.join(data['transaksi'])}\n")


# Fungsi untuk membuat akun baru
def create_account(accounts):
    account_name = (input("Masukkan nama akun: "))
    account_pin = (input("Masukkan PIN akun (4 angka): "))
    if len(account_pin) > 4:
        return "Pin maksimal 4 angka"
    if account_name in accounts:
        return "Akun sudah ada"
    accounts[account_name] = {'tabungan': 0, 'transaksi': [], 'pin': account_pin}
    save_accounts(accounts)
    return f"Akun {account_name} telah berhasil dibuat"

# Fungsi untuk mendeposit uang kedalam akun
def deposit(accounts):
    account_name = input("Masukkan nama akun yang mau dideposit: ")
    account_pin = input("Masukkan pin akun: ")
    if account_name not in accounts:
        return "Akun tidak ditemukan"
    elif accounts[account_name]['pin'] != account_pin:
        return "PIN invalid"
    else:
        amount = float(input("Masukkan jumlah yang mau dideposit: "))
        if amount <= 0:
            return "Jumlah invalid"
        accounts[account_name]['tabungan'] += amount
        accounts[account_name]['transaksi'].append(f"Terdeposit {amount} pada {datetime.datetime.now()}")
        save_accounts(accounts)
        return f"Deposit sebesar {amount} kedalam akun {account_name} telah sukses"

# Fungsi untuk menarik uang dari akun
def withdraw(accounts):
    account_name = input("Masukkan nama akun yang ingin ditarik: ")
    account_pin = input("Masukkan PIN akun: ")
    if account_name not in accounts:
        return "Akun tidak ditemukan"
    elif accounts[account_name]['pin'] != account_pin:
        return "PIN invalid"
    else:
        amount = float(input("Masukkan jumlah yang mau ditarik: "))
        if amount <= 0 or amount > accounts[account_name]['tabungan']:
            return "Jumlah tidak valid or tabungan tidak mencukupi"
        accounts[account_name]['tabungan'] -= amount
        accounts[account_name]['transaksi'].append(f"Transaksi senilai {amount} pada {datetime.datetime.now()}")
        save_accounts(accounts)
        return f"Penarikan tunai senilai {amount} dari akun {account_name} telah sukses"

# Fungsi untuk memeriksa history transaksi
def check_history(accounts):
    account_name = input("Masukkan nama akun yang mau dicek historinya: ")
    account_pin = input("Masukkan PIN akun: ")
    if account_name not in accounts:
        return "Akun tidak ditemukan"
    elif accounts[account_name]['pin'] != account_pin:
        return "PIN invalid"
    else:
        if account_name in accounts and accounts[account_name]['pin'] == account_pin:
            return accounts[account_name]['transaksi']
        else:
            return "Nama akun atau PIN tidak valid"

# Fungsi untuk mentransfer uang ke akun lain
def transfer(accounts):
    account_name = input("Masukkan nama akun pengirim: ")
    account_pin = input("Masukkan PIN akun pengirim: ")
    
    if account_name not in accounts:
        return "Akun pengirim tidak ditemukan"
    
    if accounts[account_name]['pin'] != account_pin:
        return "PIN pengirim invalid"
    
    receiver = input("Masukkan nama akun penerima: ")
    amount = float(input("Masukkan jumlah yang mau ditransfer: "))
    
    if receiver not in accounts:
        return "Akun penerima tidak ditemukan"
    
    if amount <= 0:
        return "Jumlah transfer tidak valid"
    
    if amount > accounts[account_name]['tabungan']:
        return "Saldo tidak mencukupi"
    
    accounts[account_name]['tabungan'] -= amount
    accounts[account_name]['transaksi'].append(f"Transfer ke {receiver} senilai {amount} pada {datetime.datetime.now()}")
    accounts[receiver]['tabungan'] += amount
    accounts[receiver]['transaksi'].append(f"Terima dari {account_name} senilai {amount} pada {datetime.datetime.now()}")
    
    save_accounts(accounts)
    
    return f"Transfer senilai {amount} dari {account_name} kepada {receiver} telah berhasil"



# Fungsi untuk memeriksa tabungan akun
def check_balance(accounts):
    account_name = input("Masukkan nama akun: ")
    account_pin = (input("Masukkan pin akun: "))
    if account_name in accounts or accounts[account_name]['pin'] != account_pin:
        return f"Tabungan dari akun {account_name}: {accounts[account_name]['tabungan']}"
    else:
        return "Account does not exist or pin invalid"

# Memuat data aku dari file data
accounts = load_accounts()

# Menu user untuk pengoperasian aplikasi bank
print("Selamat datang! Nasabah Bank Lodaya")
while True:
    print("\nMenu Bank:")
    print("1. Buat Akun")
    print("2. Deposit")
    print("3. Tarik Tunai")
    print("4. Cek History Transaksi")
    print("5. Transfer")
    print("6. Cek Saldo")
    print("7. Hapus Akun")
    print("8. Keluar")

    choice = input("Masukkan piihan Anda (1-8): ")

    if choice == '1':
        print(create_account(accounts))
    elif choice == '2':
        print(deposit(accounts))
    elif choice == '3':
        print(withdraw(accounts))
    elif choice == '4':
        print(check_history(accounts))
    elif choice == '5':
        print(transfer(accounts))
    elif choice == '6':
        print(check_balance(accounts))
    elif choice == '7':
        print(remove_account(accounts))
    elif choice == '8':
        break
    else:
        print("Pilihan invalid. Mohon pilih angka yang benar.")