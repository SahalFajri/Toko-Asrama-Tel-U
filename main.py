import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
import mysql.connector
import matplotlib.pyplot as plt


class Barang:
    def __init__(self, id_barang, nama_barang, harga_barang):
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.harga_barang = harga_barang


class Toko:

    # Koneksi ke database
    mydb = mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="tubes_alpro"
    )
    mycursor = mydb.cursor()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Toko Asrama Tel-U")

        self.window_width = 1280
        self.window_height = 650

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_coordinate = int(
            (self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int(
            (self.screen_height / 2) - (self.window_height / 2))
        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")

        # Membuat frame utama
        self.current_frame = None

        # List kosong untuk keranjang
        self.keranjang = []

    # Untuk menjalankan program

    def run(self):
        self.show_login_frames()
        self.root.mainloop()

    def show_login_frames(self):
        # Membuat frame utama
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            self.current_frame, text="Selamat Datang Di Toko Asrama Tel-U", font=("default", 12))
        title_label.grid(row=0, columnspan=2, padx=20, pady=20)

        # Membuat frame login admin
        admin_frame = tk.Frame(self.current_frame)
        admin_frame.grid(row=1, column=0, padx=20, pady=20)

        admin_label = tk.Label(admin_frame, text="Admin Login")
        admin_label.pack()

        admin_username_label = tk.Label(admin_frame, text="Username")
        admin_username_label.pack()

        self.admin_username = tk.Entry(admin_frame)
        self.admin_username.pack()

        admin_password_label = tk.Label(admin_frame, text="Password")
        admin_password_label.pack()

        self.admin_password = tk.Entry(admin_frame, show="*")
        self.admin_password.pack()

        admin_login_button = tk.Button(
            admin_frame, text="Login", command=self.login_admin)
        admin_login_button.pack()

        # Membuat frame login mahasiswa
        mahasiswa_frame = tk.Frame(self.current_frame)
        mahasiswa_frame.grid(row=1, column=1, padx=20, pady=20)

        mahasiswa_label = tk.Label(mahasiswa_frame, text="Mahasiswa Login")
        mahasiswa_label.pack()

        mahasiswa_nim_label = tk.Label(mahasiswa_frame, text="NIM")
        mahasiswa_nim_label.pack()

        self.mahasiswa_nim = tk.Entry(mahasiswa_frame)
        self.mahasiswa_nim.pack()

        mahasiswa_password_label = tk.Label(mahasiswa_frame, text="Password")
        mahasiswa_password_label.pack()

        self.mahasiswa_password = tk.Entry(mahasiswa_frame, show="*")
        self.mahasiswa_password.pack()

        mahasiswa_login_button = tk.Button(
            mahasiswa_frame, text="Login", command=self.login_mahasiswa)
        mahasiswa_login_button.pack()

    def login_admin(self):
        username = self.admin_username.get()
        password = self.admin_password.get()

        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        val = (username, password)
        self.mycursor.execute(query, val)
        result = self.mycursor.fetchone()

        if result:
            # Jika login sukses, tampilkan halaman manage barang
            self.show_manage_barang(username)
        else:
            messagebox.showerror(
                "Login Failed", "Username or password is incorrect")

    def login_mahasiswa(self):
        nim = self.mahasiswa_nim.get()
        password = self.mahasiswa_password.get()

        query = "SELECT * FROM mahasiswa WHERE nim = %s AND password = %s"
        val = (nim, password)
        self.mycursor.execute(query, val)
        result = self.mycursor.fetchone()

        if result:
            # Jika login sukses, tampilkan halaman pembelian
            self.show_pembelian(nim)
        else:
            messagebox.showerror(
                "Login Failed", "NIM or password is incorrect")

    def logout(self):
        # Mengkosongkan isi keranjang
        self.keranjang.clear()

        # Menghapus semua frame yang ada
        for widget in self.root.winfo_children():
            widget.destroy()

        # Memunculkan kembali frame utama (login admin dan mahasiswa)
        self.show_login_frames()

    def show_pembelian(self, nim):
        # Menghapus frame utama
        if self.current_frame:
            self.current_frame.destroy()

        # Membuat frame pembelian
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Mendapatkan data mahasiswa dari database berdasarkan NIM
        query = "SELECT nama_mahasiswa FROM mahasiswa WHERE nim = %s"
        val = (nim,)
        self.mycursor.execute(query, val)
        nama_mahasiswa = self.mycursor.fetchone()[0]

        # Menampilkan label nama mahasiswa
        nama_mahasiswa_label = tk.Label(
            self.current_frame, text=f"Selamat datang, {nama_mahasiswa}")
        nama_mahasiswa_label.pack()

        # Tabel-tabelnya
        self.notebook = ttk.Notebook(self.current_frame)
        self.notebook.pack(padx=10, pady=10)

        self.barang_frame = ttk.Frame(self.notebook)
        self.keranjang_frame = ttk.Frame(self.notebook)
        self.histori_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.barang_frame, text="Barang")
        self.notebook.add(self.keranjang_frame, text="Keranjang")
        self.notebook.add(self.histori_frame, text="Histori Transaksi")

        self.barang_columns = ("ID Barang", "Nama Barang", "Harga")
        self.barang_treeview = ttk.Treeview(
            self.barang_frame, columns=self.barang_columns, show="headings")
        self.barang_treeview.pack(padx=10, pady=10)

        self.keranjang_columns = (
            "ID Barang", "Nama Barang", "Harga", "Jumlah")
        self.keranjang_treeview = ttk.Treeview(
            self.keranjang_frame, columns=self.keranjang_columns, show="headings")
        self.keranjang_treeview.pack(padx=10, pady=10)

        self.histori_columns = (
            "ID Transaksi", "Total Harga", "Tanggal Transaksi")
        self.histori_treeview = ttk.Treeview(
            self.histori_frame, columns=self.histori_columns, show="headings")
        self.histori_treeview.pack(padx=10, pady=10)

        self.generate_barang()
        self.generate_keranjang()
        self.generate_histori_transaksi(nim)

        self.tambah_button = tk.Button(
            self.barang_frame, text="Masukkan ke Keranjang", command=self.tambah_ke_keranjang)
        self.tambah_button.pack(padx=10, pady=10)

        self.hapus_button = tk.Button(
            self.keranjang_frame, text="Hapus dari Keranjang", command=self.hapus_dari_keranjang)
        self.hapus_button.pack(padx=10, pady=10)

        self.checkout_button = tk.Button(
            self.keranjang_frame, text="Checkout", command=lambda: self.checkout(nim))
        self.checkout_button.pack(padx=10, pady=10)

        self.total_harga_label = tk.Label(
            self.keranjang_frame, text="Total Harga: Rp 0")
        self.total_harga_label.pack(padx=10, pady=10)

        self.detail_button = tk.Button(
            self.histori_frame, text="Lihat Detail", command=self.detail_histori_transaksi)
        self.detail_button.pack(padx=10, pady=10)

        # Menampilkan tombol logout
        logout_button = tk.Button(
            self.current_frame, text="Logout", command=self.logout)
        logout_button.pack()

    def generate_barang(self):
        query = "SELECT id_barang, nama_barang, harga_barang FROM barang"
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()

        self.barang_list = []
        for row in result:
            barang = Barang(row[0], row[1], row[2])
            self.barang_list.append(barang)
            self.barang_treeview.insert("", tk.END, values=(
                barang.id_barang, barang.nama_barang, barang.harga_barang))

        for column in self.barang_columns:
            self.barang_treeview.heading(column, text=column)

    def generate_keranjang(self):
        for column in self.keranjang_columns:
            self.keranjang_treeview.heading(column, text=column)

        # self.keranjang_treeview.column("ID Barang", width=80, anchor="center")
        # self.keranjang_treeview.column("Nama Barang", width=150, anchor="w")
        # self.keranjang_treeview.column("Harga", width=100, anchor="e")
        # self.keranjang_treeview.column("Jumlah", width=80, anchor="center")

    def generate_histori_transaksi(self, nim):
        # Hapus semua data dalam tabel
        for row in self.histori_treeview.get_children():
            self.histori_treeview.delete(row)

        query = "SELECT id_transaksi, total_harga, tanggal_transaksi FROM transaksi WHERE nim = %s ORDER BY tanggal_transaksi DESC"
        val = (nim,)
        self.mycursor.execute(query, val)
        result = self.mycursor.fetchall()

        for row in result:
            self.histori_treeview.insert("", tk.END, values=(
                row[0], row[1], row[2]))

        for column in self.histori_columns:
            self.histori_treeview.heading(column, text=column)

    def detail_histori_transaksi(self):
        selection = self.histori_treeview.selection()
        if selection:
            selected_item = self.histori_treeview.item(selection)

            id_detail = selected_item['values'][0]
            total_harga = selected_item['values'][1]
            total_harga = "{:,.0f}".format(total_harga)
            tanggal_transaksi = selected_item['values'][2]

            window = tk.Toplevel(self.current_frame)
            window.title("Detail Histori Transaksi")
            window.resizable(False, False)

            # agar fokus ke window
            window.grab_set()

            # membuat frame untuk input data barang
            detail_frame = ttk.LabelFrame(
                window, text=f"Transaksi ID: {id_detail}")
            detail_frame.pack(padx=30, pady=20)

            # mengambil data dari database
            self.mycursor.execute(
                "SELECT barang.nama_barang, barang.harga_barang, detail_transaksi.jumlah FROM detail_transaksi JOIN barang ON detail_transaksi.id_barang = barang.id_barang WHERE id_transaksi=%s", (id_detail,))
            result = self.mycursor.fetchall()

            label_tanggal_transaksi = tk.Label(
                detail_frame, text=f'Tanggal {tanggal_transaksi}')
            label_tanggal_transaksi.grid(row=0, columnspan=4, pady=(10, 0))

            # garis pembatas
            separator = ttk.Separator(detail_frame, orient='horizontal')
            separator.grid(row=1, columnspan=4,
                           sticky="ew", padx=10, pady=10)

            # kolom-kolom
            kolom_barang = tk.Label(
                detail_frame, text='Barang')
            kolom_barang.grid(row=2, column=0)

            kolom_harga = tk.Label(
                detail_frame, text='Harga')
            kolom_harga.grid(row=2, column=1)

            kolom_jumlah = tk.Label(
                detail_frame, text='Jumlah')
            kolom_jumlah.grid(row=2, column=2)

            kolom_jumlah_harga = tk.Label(
                detail_frame, text='Jumlah Harga')
            kolom_jumlah_harga.grid(row=2, column=3)

            # Membuat label baru untuk setiap baris data
            for i, data in enumerate(result):
                jumlah_harga = data[1] * data[2]
                jumlah_harga = "{:,.0f}".format(jumlah_harga)

                harga = "{:,.0f}".format(data[1])
                jumlah = "{:,.0f}".format(data[2])

                label_barang = tk.Label(detail_frame, text=data[0])
                label_harga = tk.Label(detail_frame, text=harga)
                label_jumlah = tk.Label(detail_frame, text=jumlah)
                label_jumlah_harga = tk.Label(detail_frame, text=jumlah_harga)

                label_barang.grid(row=i+3, column=0)
                label_harga.grid(row=i+3, column=1)
                label_jumlah.grid(row=i+3, column=2)
                label_jumlah_harga.grid(row=i+3, column=3)

            # garis pembatas
            separator = ttk.Separator(detail_frame, orient='horizontal')
            separator.grid(row=i+4, columnspan=4,
                           sticky="ew", padx=10, pady=10)

            label_total_harga = tk.Label(
                detail_frame, text='Total Harga:')
            label_total_harga.grid(row=i+5, column=0, pady=(0, 20))

            label_total_harga = tk.Label(
                detail_frame, text=f'Rp {total_harga}')
            label_total_harga.grid(row=i+5, column=3, pady=(0, 20))

            # mengatur posisi jendela dialog di tengah-tengah layar
            window.update_idletasks()
            width = window.winfo_width()
            height = window.winfo_height()
            x = (window.winfo_screenwidth() // 2) - (width // 2)
            y = (window.winfo_screenheight() // 2) - (height // 2)
            window.geometry(f"{width}x{height}+{x}+{y}")

        else:
            messagebox.showwarning(
                "Peringatan", "Pilih transaksi terlebih dahulu.")

    def tambah_ke_keranjang(self):
        selection = self.barang_treeview.selection()
        if selection:
            selected_item = self.barang_treeview.item(selection)
            barang = self.parse_barang(selected_item["values"])
            dialog = JumlahBarangDialog(self.root)
            if dialog.jumlah_barang is not None:
                self.update_keranjang(barang, dialog.jumlah_barang)
                self.update_total_harga()
                messagebox.showinfo(
                    "Sukses", f"Barang '{barang.nama_barang}' telah ditambahkan ke keranjang.")
        else:
            messagebox.showwarning(
                "Peringatan", "Pilih barang terlebih dahulu.")

    def update_keranjang(self, barang, jumlah):
        for item in self.keranjang:
            if item["barang"].id_barang == barang.id_barang:
                item["jumlah"] += jumlah
                index = self.keranjang.index(item)
                self.keranjang_treeview.set(
                    self.keranjang_treeview.get_children()[index], "Jumlah", item["jumlah"])
                self.update_total_harga()
                return

        self.keranjang.append({"barang": barang, "jumlah": jumlah})
        self.keranjang_treeview.insert("", tk.END, values=(
            barang.id_barang, barang.nama_barang, barang.harga_barang, jumlah))
        self.update_total_harga()

    def hapus_dari_keranjang(self):
        selection = self.keranjang_treeview.selection()
        if selection:
            index = self.keranjang_treeview.index(selection)
            self.keranjang.pop(index)
            self.keranjang_treeview.delete(selection)
            self.update_total_harga()
        else:
            messagebox.showwarning(
                "Peringatan", "Pilih barang dalam keranjang terlebih dahulu.")

    def checkout(self, nim):
        if self.keranjang:
            total_harga = sum(
                item["barang"].harga_barang * item["jumlah"] for item in self.keranjang)
            query = "INSERT INTO transaksi (nim, total_harga, tanggal_transaksi) VALUES (%s, %s, %s)"
            val = (nim, total_harga, date.today())
            self.mycursor.execute(query, val)
            last_id = self.mycursor.lastrowid
            self.mydb.commit()

            for item in self.keranjang:
                query = "INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah) VALUES (%s, %s, %s)"
                val = (last_id, item["barang"].id_barang, item["jumlah"])
                self.mycursor.execute(query, val)
                self.mydb.commit()

            total_harga = "{:,.0f}".format(total_harga)
            messagebox.showinfo(
                "Checkout", f"Total harga: Rp {total_harga}, Terima kasih sudah berbelanja")
            self.keranjang.clear()
            self.keranjang_treeview.delete(
                *self.keranjang_treeview.get_children())
            self.update_total_harga()
            self.generate_histori_transaksi(nim)
        else:
            messagebox.showwarning(
                "Peringatan", "Keranjang kosong. Tambahkan barang terlebih dahulu.")

    def parse_barang(self, values):
        id_barang, nama_barang, harga_barang = values
        return Barang(id_barang, nama_barang, harga_barang)

    def update_total_harga(self):
        total_harga = sum(
            item["barang"].harga_barang * item["jumlah"] for item in self.keranjang)
        total_harga = "{:,.0f}".format(total_harga)
        self.total_harga_label.config(text=f"Total Harga: Rp {total_harga}")

    # Bagian Admin
    def show_manage_barang(self, username):
        # Menghapus frame saat ini
        if self.current_frame:
            self.current_frame.destroy()

        # Membuat frame manage barang
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Mendapatkan data admin dari database berdasarkan NIM
        query = "SELECT nama_admin FROM admin WHERE username = %s"
        val = (username,)
        self.mycursor.execute(query, val)
        nama_admin = self.mycursor.fetchone()[0]

        # Menampilkan label nama admin
        nama_admin_label = tk.Label(
            self.current_frame, text=f"Selamat datang, {nama_admin}")
        nama_admin_label.pack()

        # Frame untuk button
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(side=tk.LEFT, padx=20)

        # Button Tambah
        add_button = ttk.Button(
            button_frame, text="Tambah", command=lambda: self.window_baru("Tambah")
        )
        add_button.pack(fill=tk.X, padx=5, pady=5)

        # Button Update/Edit
        edit_button = ttk.Button(
            button_frame, text="Edit", command=lambda: self.window_baru("Edit")
        )
        edit_button.pack(fill=tk.X, padx=5, pady=5)

        # Button Hapus
        delete_button = ttk.Button(
            button_frame, text="Hapus", command=self.hapus_data
        )
        delete_button.pack(fill=tk.X, padx=5, pady=5)

        # Memberikan garis pembatas
        separator = ttk.Separator(button_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

        # Menampilkan tombol Data Penjualan
        penjualan_button = ttk.Button(
            button_frame, text="Data Penjualan", command=self.data_penjualan)
        penjualan_button.pack(fill=tk.X, padx=5, pady=5)

        # Memberikan garis pembatas
        separator = ttk.Separator(button_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

        # Menampilkan tombol logout
        logout_button = ttk.Button(
            button_frame, text="Logout", command=self.logout)
        logout_button.pack(fill=tk.X, padx=5, pady=5)

        # Frame Table
        table_frame = ttk.Frame(self.current_frame)
        table_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.admin_treeview = ttk.Treeview(
            table_frame,
            columns=("id_barang", "nama_barang",
                     "harga_barang"),
            show="headings",
        )
        self.admin_treeview.pack(side=tk.LEFT)

        self.admin_treeview.heading("id_barang", text="ID Barang")
        self.admin_treeview.heading("nama_barang", text="Nama Barang")
        self.admin_treeview.heading("harga_barang", text="Harga Barang")

        self.show_data()

    def data_penjualan(self):
        labels_nama_barang = []
        barang_terjual = []

        query = "SELECT barang.nama_barang, SUM(detail_transaksi.jumlah) FROM barang JOIN detail_transaksi ON barang.id_barang = detail_transaksi.id_barang GROUP BY barang.id_barang"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        for row in data:
            labels_nama_barang.append(row[0])
            barang_terjual.append(row[1])

        plt.figure(figsize=(6, 6))

        lebar_bar = 0.5  # lebar bar

        # membuat bar plot, memberi label
        plt.bar(labels_nama_barang, barang_terjual,
                width=lebar_bar, label="Barang")

        for i in range(len(labels_nama_barang)):
            plt.text(
                labels_nama_barang[i], barang_terjual[i], barang_terjual[i], ha='center', va='bottom')

        plt.ylabel("Jumlah Barang Terjual")  # memberi label pada sumbu y
        plt.xlabel('Nama Barang')
        plt.title("Jumlah Masing-masing Barang Yang Terjual")

        plt.legend()
        plt.show()

    # Menampilkan data ke table

    def show_data(self):
        # Mengkosongkan table
        records = self.admin_treeview.get_children()
        for record in records:
            self.admin_treeview.delete(record)

        # Mengambil data dari database
        query = "SELECT * FROM barang"
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        for row in data:
            self.admin_treeview.insert("", tk.END, values=row)

    # Buat window baru untuk Tambah/Edit

    def window_baru(self, tipe):
        if tipe == "Edit":
            # Jika tidak ada data yang dipilih
            if not self.admin_treeview.focus():
                messagebox.showwarning(
                    title="Warning", message="Silahkan pilih data untuk di-Edit"
                )
                return

            selected_item = self.admin_treeview.focus()
            values = self.admin_treeview.item(selected_item, "values")
            id_barang = values[0]
            nama_barang = values[1]
            harga_barang = values[2]

        global window, id_barang_entry, nama_barang_entry, harga_barang_entry
        window = tk.Toplevel(self.current_frame)
        window.title(f"{tipe} Data Barang")

        # agar fokus ke window
        window.grab_set()

        # membuat frame untuk input data barang
        input_frame = ttk.LabelFrame(
            window, text=f" {tipe} Barang ")
        input_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # input id_barang
        id_barang_label = ttk.Label(input_frame, text="ID Barang :")
        id_barang_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        if tipe == "Tambah":
            id_barang_entry = ttk.Entry(input_frame)
            id_barang_entry.grid(row=0, column=1, padx=5, pady=5)
        else:
            id_barang_label = ttk.Label(input_frame, text=id_barang)
            id_barang_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # input nama_barang
        nama_barang_label = ttk.Label(input_frame, text="Nama Barang :")
        nama_barang_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        nama_barang_entry = ttk.Entry(input_frame)
        nama_barang_entry.grid(row=1, column=1, padx=5, pady=5)

        # input harga_barang
        harga_barang_label = ttk.Label(input_frame, text="Harga Barang :")
        harga_barang_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        harga_barang_entry = ttk.Entry(input_frame)
        harga_barang_entry.grid(row=2, column=1, padx=5, pady=5)

        if tipe == "Edit":
            nama_barang_entry.focus_set()

            nama_barang_entry.insert(0, nama_barang)
            harga_barang_entry.insert(0, harga_barang)

            # Tombol Edit
            edit_button = ttk.Button(
                input_frame, text="Edit", command=lambda: self.edit_data(id_barang)
            )
            edit_button.grid(row=5, columnspan=2, padx=5, pady=5)
        else:
            id_barang_entry.focus_set()

            # Tombol Tambah
            clear_button = ttk.Button(
                input_frame, text="Reset", command=self.clear_input
            )
            clear_button.grid(row=3, column=0, padx=5, pady=5)

            # Tombol Tambah
            tambah_button = ttk.Button(
                input_frame, text="Tambah", command=self.tambah_data
            )
            tambah_button.grid(row=3, column=1, padx=5, pady=5)

        # mengatur posisi jendela dialog di tengah-tengah layar
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    # Untuk clear inputan

    def clear_input(self):
        id_barang_entry.delete(0, tk.END)
        nama_barang_entry.delete(0, tk.END)
        harga_barang_entry.delete(0, tk.END)

    def tambah_data(self):
        # Ambil data dari inputan
        id_barang = id_barang_entry.get()
        nama_barang = nama_barang_entry.get()
        harga_barang = harga_barang_entry.get()

        # Cek apakah ada input yang kosong
        if id_barang == "" or nama_barang == "" or harga_barang == "":
            messagebox.showerror("Error", "Mohon lengkapi semua input")
            return

        # Periksa duplikasi
        query = "SELECT id_barang FROM barang WHERE id_barang = %s"
        self.mycursor.execute(query, (id_barang,))
        result = self.mycursor.fetchone()

        if result:
            messagebox.showerror("Error", "ID Barang sudah terdaftar")
            return

        # Jika id_barang yang diinputkan bukan angka
        try:
            # Masukkan data ke database
            query = "INSERT INTO barang (id_barang, nama_barang, harga_barang) VALUES (%s, %s, %s)"
            params = (id_barang, nama_barang, harga_barang)
            self.mycursor.execute(query, params)
            self.mydb.commit()
        except mysql.connector.Error:
            messagebox.showerror(
                "Error", "Terjadi kesalahan saat menambahkan data ke database")
            return

        # Bersihkan inputan setelah data dimasukkan ke database
        self.clear_input()

        messagebox.showinfo("Success", "Data berhasil ditambahkan")

        self.show_data()

    def edit_data(self, id_barang):
        nama_barang = nama_barang_entry.get()
        harga_barang = harga_barang_entry.get()

        # Cek apakah ada input yang kosong
        if nama_barang == "" or harga_barang == "":
            messagebox.showerror("Error", "Mohon lengkapi semua input")
            return

        # Masukkan data ke database
        query = "UPDATE barang SET nama_barang = %s, harga_barang = %s WHERE id_barang = %s"
        params = (nama_barang, harga_barang, id_barang)
        self.mycursor.execute(query, params)
        self.mydb.commit()

        window.destroy()

        messagebox.showinfo("Success", "Data berhasil diubah")

        self.show_data()

    def hapus_data(self):
        # Ketika tidak ada data yang dipilih
        if not self.admin_treeview.focus():
            messagebox.showwarning(
                title="Warning", message="Silahkan pilih data untuk di-Hapus"
            )
            return

        # Konfirmasi untuk menghapus
        result = messagebox.askquestion(
            title="Delete Confirmation", message="Apakah anda yakin?"
        )

        if result == "yes":
            # Ambil ID data yang akan dihapus
            selected_item = self.admin_treeview.focus()
            values = self.admin_treeview.item(selected_item, "values")
            id = values[0]

            # Hapus data dari database
            query = "DELETE FROM barang WHERE id_barang=%s"
            params = (id,)
            self.mycursor.execute(query, params)
            self.mydb.commit()

            # Tampilkan data terbaru pada tabel
            self.show_data()


class JumlahBarangDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Jumlah Barang")
        self.resizable(False, False)

        self.jumlah_barang = None

        self.jumlah_label = tk.Label(self, text="Jumlah Barang:")
        self.jumlah_label.pack(padx=10, pady=10)

        self.jumlah_entry = tk.Entry(self)
        self.jumlah_entry.pack(padx=10, pady=5)

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(padx=10, pady=10)

        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(padx=10, pady=5)

        # Mengatur fokus otomatis ke entri jumlah barang
        self.jumlah_entry.focus_set()

        self.transient(parent)
        self.wait_visibility()

        # Mengatur posisi jendela pop-up di tengah layar
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        self.grab_set()
        self.wait_window()

    def on_ok(self):
        jumlah_barang = self.jumlah_entry.get()
        if jumlah_barang.isdigit():
            self.jumlah_barang = int(jumlah_barang)
            self.destroy()
        else:
            messagebox.showwarning(
                "Peringatan", "Jumlah barang harus berupa angka.")

    def on_cancel(self):
        self.destroy()


TokoTelU = Toko()
TokoTelU.run()
