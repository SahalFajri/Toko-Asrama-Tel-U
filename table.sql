-- mahasiswa: nim, nama_mahasiswa, password, no_gedung, no_kamar
-- admin: id_admin, nama_admin, username, password
-- barang: id_barang, nama_barang, harga_barang
-- transaksi: id_transaksi, nim, total_harga, tanggal_transaksi
-- detail_transaksi: id_transaksi, id_barang, jumlah

CREATE TABLE mahasiswa (
  nim VARCHAR(10) PRIMARY KEY,
  nama_mahasiswa VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  no_gedung VARCHAR(2),
  no_kamar VARCHAR(3)
);

CREATE TABLE admin (
  id_admin INT PRIMARY KEY AUTO_INCREMENT,
  nama_admin VARCHAR(50) NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL
);

CREATE TABLE barang (
  id_barang VARCHAR(30) PRIMARY KEY,
  nama_barang VARCHAR(50) NOT NULL,
  harga_barang INT
);

CREATE TABLE transaksi (
  id_transaksi INT PRIMARY KEY AUTO_INCREMENT,
  nim VARCHAR(10),
  total_harga INT,
  tanggal_transaksi DATE,
  FOREIGN KEY (nim) REFERENCES mahasiswa(nim)
);

CREATE TABLE detail_transaksi (
  id_transaksi INT,
  id_barang VARCHAR(30),
  jumlah INT,
  FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
  FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
);

-- Data Dummy

-- Tabel mahasiswa
INSERT INTO mahasiswa (nim, nama_mahasiswa, password, no_gedung, no_kamar)
VALUES
  ('123', 'Sahal Fajri', '123', 'A1', '101'),
  ('456', 'Ahmad Suhail', '456', 'B2', '202'),
  ('789', 'Widia Nurainy', '789', 'C3', '303');

-- Tabel admin
INSERT INTO admin (nama_admin, username, password)
VALUES
  ('Admin 1', 'admin1', 'adminpass1'),
  ('Admin 2', 'admin2', 'adminpass2'),
  ('Admin 3', 'admin3', 'adminpass3');

-- Tabel barang
INSERT INTO barang (id_barang, nama_barang, harga_barang)
VALUES
  ('B001', 'Laptop', 8000000),
  ('B002', 'Smartphone', 5000000),
  ('B003', 'Mouse', 50000);

-- Trigger

DELIMITER //
CREATE TRIGGER `delete_related_rows` BEFORE DELETE ON `barang`
 FOR EACH ROW BEGIN
    -- Hapus baris dari tabel detail_transaksi yang terkait dengan barang yang akan dihapus
    DELETE FROM detail_transaksi WHERE id_barang = OLD.id_barang;
END//
DELIMITER ;