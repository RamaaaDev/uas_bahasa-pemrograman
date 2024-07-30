# Flask Web Project

Proyek ini adalah aplikasi web yang dibangun menggunakan Flask, framework web mikro berbasis Python.

## requirements

Pastikan Anda memiliki perangkat lunak berikut yang terinstal di komputer:

- Python 3.x
- pip (Python package installer)
- Xampp
- install beberapa modul tambahan seperti mysql-connector-python 

## installation

Ikuti langkah-langkah di bawah ini untuk menginstal dan menjalankan proyek di lingkungan lokal Anda.
- clone repository ini kedalam file local
- jalankan XAMPP
- buat file database dengan perintah ini
import mysql.connector
from mysql.connector import errorcode

# Konfigurasi koneksi database
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
}

try:
    # Menghubungkan ke MySQL
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Membuat database jika belum ada
    cursor.execute("CREATE DATABASE IF NOT EXISTS db_gui")
    cursor.execute("USE db_gui")

    # Membuat tabel jika belum ada
    create_table_query = """
    CREATE TABLE IF NOT EXISTS history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        date DATETIME NOT NULL,
        time TIME NOT NULL
    )
    """

    cursor.execute(create_table_query)
    print("Database and table created successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cursor.close()
    cnx.close()
- lalu samakan file db nya
- untuk menjalankan dan melihat output berupa web, ketikkan perintah ini pada CMD atau semacamnya : py app.py (pada windows. device lain silahkan cari tau sendiri)
