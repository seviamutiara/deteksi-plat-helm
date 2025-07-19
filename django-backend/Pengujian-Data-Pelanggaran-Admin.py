import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def log_to_file(fitur, status, keterangan=""):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Data-Pelaggaran.txt", "a", encoding="utf-8") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

# Inisialisasi WebDriver
driver = webdriver.Chrome()

try:
    # 1. Akses dan login
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

    # 2. Jalankan skrip simulasi kamera yang akan mengirim pelanggaran via API
    log_to_file("Kamera Simulasi", "Mulai", "Menjalankan test_post.py")
    subprocess.run(["python", "../detection-app/test_post.py"]) 
    log_to_file("Kamera Simulasi", "Selesai", "Pengiriman pelanggaran selesai")

    time.sleep(3)

    # 4. Akses halaman pelanggaran dan verifikasi apakah data dari kamera muncul
    driver.get("http://127.0.0.1:9000/dashboard/")
    time.sleep(2)

    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    ditemukan = False

    for row in rows:
        if "kamera" in row.text.lower() or "simulasi" in row.text.lower():
            ditemukan = True
            break

    if ditemukan:
        log_to_file("Verifikasi Pelanggaran", "Berhasil", "Data dari kamera muncul di tabel")
    else:
        log_to_file("Verifikasi Pelanggaran", "Gagal", "Data dari kamera tidak ditemukan di tabel")

except Exception as e:
    log_to_file("Error Umum", "Gagal", str(e))

driver.quit()
