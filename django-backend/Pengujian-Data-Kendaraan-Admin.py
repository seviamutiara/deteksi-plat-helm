from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

driver = webdriver.Chrome()

def log_to_file(fitur, status):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('Pengujian-Login-Data-Kendaraan.txt', 'a') as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status}\n")

try:
    # === LOGIN ===
    driver.get('http://127.0.0.1:9000/dashboard')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    ).send_keys('vikraselpian')

    driver.find_element(By.NAME, 'password').send_keys('selpian123')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)
    if '/dashboard' in driver.current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", f"Gagal, redirect ke {driver.current_url}")

    # === AKSES HALAMAN DATA KENDARAAN ===
    driver.get('http://127.0.0.1:9000/kendaraan/')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[td]"))
    )

    rows = driver.find_elements(By.XPATH, "//table/tbody/tr[td]")
    if rows:
        log_to_file("Data Kendaraan", f"Berhasil menampilkan {len(rows)} data")
    else:
        log_to_file("Data Kendaraan", "Tampil tapi belum ada data kendaraan")

    # === TAMBAH DATA KENDARAAN ===
    tambah_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "+ Tambah Kendaraan"))
    )
    tambah_button.click()

    # Tunggu form tambah kendaraan muncul
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "plat_nomor"))
    )

    # Isi form
    driver.find_element(By.NAME, "plat_nomor").send_keys("BP 2871 JG")
    driver.find_element(By.NAME, "jenis_kendaraan").send_keys("Verza Putih")
    driver.find_element(By.NAME, "user").send_keys("batam")

    # Upload file gambar kendaraan
    foto_input = driver.find_element(By.NAME, "foto_kendaraan")
    foto_path = os.path.abspath("../detection-app/2.jpg")  
    foto_input.send_keys(foto_path)

    # Submit form
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    # Cek kembali ke halaman kendaraan
    if '/kendaraan' in driver.current_url:
        log_to_file("Tambah Kendaraan", "Berhasil menambahkan kendaraan baru")
    else:
        log_to_file("Tambah Kendaraan", f"Gagal, tetap di {driver.current_url}")

except Exception as e:
    log_to_file("Error", str(e))

finally:
    driver.quit()
