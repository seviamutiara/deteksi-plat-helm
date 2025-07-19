from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

def log_to_file(fitur, status, keterangan=""):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Kirim-Notifikasi.txt", "a", encoding="utf-8") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

# Inisialisasi WebDriver
driver = webdriver.Chrome()

try:
    # 1. Login ke sistem
    driver.get("http://127.0.0.1:9000/login/")
    driver.find_element(By.NAME, "username").send_keys("vikraselpian")
    driver.find_element(By.NAME, "password").send_keys("selpian123")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    if "/dashboard" in driver.current_url:
        log_to_file("Login Admin", "Berhasil")
    else:
        log_to_file("Login Admin", "Gagal", f"Tetap di {driver.current_url}")
        driver.quit()
        exit()

    # 2. Akses halaman dashboard
    driver.get("http://127.0.0.1:9000/dashboard/")
    time.sleep(2)

    # Ambil semua baris tabel pelanggaran
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    jumlah_notif_terkirim = 0

    for index, row in enumerate(rows):
        print(f"🔍 Memeriksa baris ke-{index + 1}: {row.text}")
        try:
            tombol = row.find_element(By.XPATH, './/a[contains(text(), "Kirim Notifikasi")]')
            lokasi = row.find_elements(By.TAG_NAME, "td")[3].text  
            plat = row.find_elements(By.TAG_NAME, "td")[4].text    

            tombol.click()
            time.sleep(2)

            log_to_file("Kirim Notifikasi", "Berhasil", f"Tombol diklik di baris {index + 1}, Lokasi: {lokasi}, Plat: {plat}")
            jumlah_notif_terkirim += 1

            # Kembali ke halaman dashboard agar bisa klik notifikasi berikutnya
            driver.get("http://127.0.0.1:9000/dashboard/")
            time.sleep(2)
            rows = driver.find_elements(By.XPATH, '//table/tbody/tr') 

        except NoSuchElementException:
            log_to_file("Cek Tombol", "Tidak Ada", f"Baris {index + 1} tidak memiliki tombol Kirim Notifikasi")

    if jumlah_notif_terkirim == 0:
        log_to_file("Kirim Notifikasi", "Gagal", "Tidak ditemukan tombol di baris mana pun")
    else:
        log_to_file("Kirim Notifikasi", "Selesai", f"Total notifikasi terkirim: {jumlah_notif_terkirim}")

except Exception as e:
    log_to_file("Error Umum", "Gagal", str(e))

driver.quit()
