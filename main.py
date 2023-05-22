import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Koneksi ke database
mydb = mysql.connector.connect(
    host="localhost",
    port=3308,  # Ganti dengan port MySQL yang digunakan
    user="root",
    password="",
    database="tubes_alpro"
)
mycursor = mydb.cursor()


# Fungsi untuk melakukan login admin
def login_admin():
    username = admin_username.get()
    password = admin_password.get()

    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(query, val)
    result = mycursor.fetchone()

    if result:
        # Jika login sukses, tampilkan halaman manage barang
        show_manage_barang()
    else:
        messagebox.showerror(
            "Login Failed", "Username or password is incorrect")


# Fungsi untuk melakukan login mahasiswa
def login_mahasiswa():
    nim = mahasiswa_nim.get()
    password = mahasiswa_password.get()

    query = "SELECT * FROM mahasiswa WHERE nim = %s AND password = %s"
    val = (nim, password)
    mycursor.execute(query, val)
    result = mycursor.fetchone()

    if result:
        # Jika login sukses, tampilkan halaman pembelian
        show_pembelian(nim)
    else:
        messagebox.showerror("Login Failed", "NIM or password is incorrect")


# Fungsi untuk menampilkan halaman pembelian
def show_pembelian(nim):
    # Menghapus frame utama
    main_frame.destroy()

    # Membuat frame pembelian
    global pembelian_frame
    pembelian_frame = tk.Frame(root)
    pembelian_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Mendapatkan data mahasiswa dari database berdasarkan NIM
    query = "SELECT nama_mahasiswa FROM mahasiswa WHERE nim = %s"
    val = (nim,)
    mycursor.execute(query, val)
    result = mycursor.fetchone()

    if result:
        nama_mahasiswa = result[0]

        # Menampilkan label nama mahasiswa
        nama_mahasiswa_label = tk.Label(
            pembelian_frame, text=f"Selamat datang, {nama_mahasiswa}")
        nama_mahasiswa_label.pack()

        # Menampilkan tombol pembelian
        pembelian_button = tk.Button(
            pembelian_frame, text="Pembelian", command=lambda: show_pilihan_barang(nim))
        pembelian_button.pack()

        # Menampilkan tombol histori pembelian
        histori_button = tk.Button(
            pembelian_frame, text="Histori Pembelian", command=lambda: show_histori_pembelian(nim))
        histori_button.pack()

        # Menampilkan tombol logout
        logout_button = tk.Button(
            pembelian_frame, text="Logout", command=logout)
        logout_button.pack()
    else:
        # Jika data mahasiswa tidak ditemukan, menampilkan pesan error
        messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")


# Fungsi untuk menampilkan halaman pilihan barang
def show_pilihan_barang(nim):
    # Menghapus frame pembelian
    pembelian_frame.destroy()

    # Membuat frame pilihan barang
    pilihan_barang_frame = tk.Frame(root)
    pilihan_barang_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Menampilkan label pilihan barang
    pilihan_barang_label = tk.Label(
        pilihan_barang_frame, text="Pilihan Barang")
    pilihan_barang_label.pack()

    # Menampilkan daftar barang dari database
    query = "SELECT id_barang, nama_barang, harga_barang FROM barang"
    mycursor.execute(query)
    result = mycursor.fetchall()

    for row in result:
        id_barang, nama_barang, harga_barang = row

        # Menampilkan informasi barang
        barang_label = tk.Label(
            pilihan_barang_frame, text=f"ID Barang: {id_barang} | Nama Barang: {nama_barang} | Harga: {harga_barang}")
        barang_label.pack()

        # Menampilkan tombol beli
        beli_button = tk.Button(pilihan_barang_frame, text="Beli",
                                command=lambda id_barang=id_barang, nim=nim: proses_pembelian(id_barang, nim))
        beli_button.pack()

    # Menampilkan tombol kembali
    kembali_button = tk.Button(
        pilihan_barang_frame, text="Kembali", command=lambda: show_pembelian(nim))
    kembali_button.pack()


# Fungsi untuk memproses pembelian barang
def proses_pembelian(id_barang, nim):
    # Implementasi logika pembelian barang disini
    pass


# Fungsi untuk menampilkan halaman manage barang
def show_manage_barang():
    # Implementasi tampilan halaman manage barang disini
    pass


# Fungsi untuk menampilkan halaman histori pembelian
def show_histori_pembelian(nim):
    # Implementasi tampilan halaman histori pembelian disini
    pass


# Fungsi untuk logout
def logout():
    # Menghapus semua frame yang ada
    for widget in root.winfo_children():
        widget.destroy()

    # Memunculkan kembali frame utama (login admin dan mahasiswa)
    show_login_frames()

# Fungsi untuk menampilkan frame login admin dan mahasiswa


def show_login_frames():
    # Membuat frame utama
    global main_frame
    main_frame = tk.Frame(root)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Membuat frame login admin
    admin_frame = tk.Frame(main_frame)
    admin_frame.grid(row=0, column=0, padx=20, pady=20)

    admin_label = tk.Label(admin_frame, text="Admin Login")
    admin_label.pack()

    admin_username_label = tk.Label(admin_frame, text="Username")
    admin_username_label.pack()

    global admin_username
    admin_username = tk.Entry(admin_frame)
    admin_username.pack()

    admin_password_label = tk.Label(admin_frame, text="Password")
    admin_password_label.pack()

    global admin_password
    admin_password = tk.Entry(admin_frame, show="*")
    admin_password.pack()

    admin_login_button = tk.Button(
        admin_frame, text="Login", command=login_admin)
    admin_login_button.pack()

    # Membuat frame login mahasiswa
    mahasiswa_frame = tk.Frame(main_frame)
    mahasiswa_frame.grid(row=0, column=1, padx=20, pady=20)

    mahasiswa_label = tk.Label(mahasiswa_frame, text="Mahasiswa Login")
    mahasiswa_label.pack()

    mahasiswa_nim_label = tk.Label(mahasiswa_frame, text="NIM")
    mahasiswa_nim_label.pack()

    global mahasiswa_nim
    mahasiswa_nim = tk.Entry(mahasiswa_frame)
    mahasiswa_nim.pack()

    mahasiswa_password_label = tk.Label(mahasiswa_frame, text="Password")
    mahasiswa_password_label.pack()

    global mahasiswa_password
    mahasiswa_password = tk.Entry(mahasiswa_frame, show="*")
    mahasiswa_password.pack()

    mahasiswa_login_button = tk.Button(
        mahasiswa_frame, text="Login", command=login_mahasiswa)
    mahasiswa_login_button.pack()


# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Penjualan")
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Memunculkan frame login saat aplikasi dimulai
show_login_frames()


root.mainloop()
