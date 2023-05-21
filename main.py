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
    # Implementasi tampilan halaman pembelian disini
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
    # Implementasi logika logout disini
    pass


# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Penjualan")
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Membuat frame utama
main_frame = tk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Membuat frame login admin
admin_frame = tk.Frame(main_frame)
admin_frame.grid(row=0, column=0, padx=20, pady=20)

admin_label = tk.Label(admin_frame, text="Admin Login")
admin_label.pack()

admin_username_label = tk.Label(admin_frame, text="Username")
admin_username_label.pack()

admin_username = tk.Entry(admin_frame)
admin_username.pack()

admin_password_label = tk.Label(admin_frame, text="Password")
admin_password_label.pack()

admin_password = tk.Entry(admin_frame, show="*")
admin_password.pack()

admin_login_button = tk.Button(admin_frame, text="Login", command=login_admin)
admin_login_button.pack()

# Membuat frame login mahasiswa
mahasiswa_frame = tk.Frame(main_frame)
mahasiswa_frame.grid(row=0, column=1, padx=20, pady=20)

mahasiswa_label = tk.Label(mahasiswa_frame, text="Mahasiswa Login")
mahasiswa_label.pack()

mahasiswa_nim_label = tk.Label(mahasiswa_frame, text="NIM")
mahasiswa_nim_label.pack()

mahasiswa_nim = tk.Entry(mahasiswa_frame)
mahasiswa_nim.pack()

mahasiswa_password_label = tk.Label(mahasiswa_frame, text="Password")
mahasiswa_password_label.pack()

mahasiswa_password = tk.Entry(mahasiswa_frame, show="*")
mahasiswa_password.pack()

mahasiswa_login_button = tk.Button(
    mahasiswa_frame, text="Login", command=login_mahasiswa)
mahasiswa_login_button.pack()

root.mainloop()
