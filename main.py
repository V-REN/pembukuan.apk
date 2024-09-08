import json
from tabulate import tabulate  # Mengimpor pustaka tabulate untuk tampilan tabel

class PersonalFinanceApp:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def load_data(self):
        try:
            with open('transactions.json', 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = []

    def save_data(self):
        with open('transactions.json', 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def format_currency(self, amount):
        """
        Fungsi untuk memformat jumlah dalam format mata uang.
        Contoh: 1000000 -> 1,000,000.00
        """
        return "{:,.2f}".format(amount)

    def add_income(self, amount, description):
        self.transactions.append({'type': 'Income', 'amount': amount, 'description': description})
        self.save_data()

    def add_expense(self, amount, description):
        self.transactions.append({'type': 'Expense', 'amount': -amount, 'description': description})
        self.save_data()

    def delete_transaction(self, index):
        """
        Fungsi untuk menghapus transaksi berdasarkan indeks yang diberikan.
        """
        try:
            removed_transaction = self.transactions.pop(index)
            print(f"Transaksi {removed_transaction['type']} sebesar {self.format_currency(removed_transaction['amount'])} telah dihapus.")
            self.save_data()
        except IndexError:
            print("Indeks tidak valid. Silakan coba lagi.")

    def delete_all_transactions(self):
        """
        Fungsi untuk menghapus semua transaksi.
        """
        confirmation = input("Apakah Anda yakin ingin menghapus semua transaksi? (y/n): ")
        if confirmation.lower() == 'y':
            self.transactions = []  # Menghapus semua transaksi
            self.save_data()  # Menyimpan perubahan
            print("Semua transaksi telah dihapus.")
        else:
            print("Penghapusan dibatalkan.")

    def view_transactions(self):
        # Menampilkan transaksi dalam bentuk tabel
        if not self.transactions:
            print("Tidak ada transaksi.")
            return
        
        # Mengatur data untuk tabel dengan format desimal
        table = [
            [index + 1, t['type'], self.format_currency(t['amount']), t['description']]
            for index, t in enumerate(self.transactions)
        ]
        headers = ["No", "Type", "Amount", "Description"]

        print("\nTransaction History:")
        print(tabulate(table, headers, tablefmt="grid"))  # Menggunakan tabulate untuk menampilkan tabel

    def calculate_balance(self):
        balance = sum(transaction['amount'] for transaction in self.transactions)
        return balance

    def run(self):
        print("Welcome to Personal Finance App!")
        while True:
            print("\nMenu:")
            print("1. Masukan data pemasukan")
            print("2. Masukan data pengeluaran")
            print("3. List transaksi")
            print("4. Lihat sisa uang")
            print("5. Hapus transaksi")
            print("6. Hapus semua transaksi")
            print("7. Exit")
            
            choice = input("Masukan pilihan: ")

            if choice == '1':
                amount = float(input("Masukan pendapatan bulanan: "))
                description = input("Deskripsikan data perbulan: ")
                self.add_income(amount, description)
                print("Berhasil memasukan data.")
            elif choice == '2':
                amount = float(input("Masukan jumlah pengeluaran: "))
                description = input("Deskripsikan pengeluaran: ")
                self.add_expense(amount, description)
                print("Berhasil menambahkan pengeluaran.")
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                balance = self.calculate_balance()
                print(f"Sisa uang mu menurut data: {self.format_currency(balance)}")
            elif choice == '5':
                self.view_transactions()
                if self.transactions:
                    try:
                        index = int(input("Masukan nomor transaksi yang ingin dihapus: ")) - 1
                        self.delete_transaction(index)
                    except ValueError:
                        print("Masukan tidak valid. Harap masukkan angka.")
            elif choice == '6':
                self.delete_all_transactions()
            elif choice == '7':
                print("Terima kasih sudah memakai layanan keuangan ini :3")
                break
            else:
                print("Gak ada pilihan nya, coba lagi.")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()