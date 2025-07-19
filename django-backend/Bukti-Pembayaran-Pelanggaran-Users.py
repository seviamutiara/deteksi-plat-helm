from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import time
from datetime import datetime

def log_to_file(fitur, status, keterangan=""):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Bukti-Pembayaran.txt", "a", encoding="utf-8") as file:
        file.write(f"{fitur} - {waktu} - Status: {status} - {keterangan}\n")

bukti_path = os.path.abspath("bukti.jpg")

driver = webdriver.Chrome()

try:
    # Login ke sistem
    driver.get("http://127.0.0.1:9000/login/")
    driver.find_element(By.NAME, "username").send_keys("batam")
    driver.find_element(By.NAME, "password").send_keys("qwerty123")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    if "/home" in driver.current_url:
        log_to_file("Login user", "Berhasil")
    else:
        log_to_file("Login user", "Gagal", "Tidak diarahkan ke home")
        driver.quit()
        exit()

    # Akses halaman notifikasi
    driver.get("http://127.0.0.1:9000/notifikasi/saya/")
    time.sleep(2)

    # Ambil semua baris notifikasi
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

    for i, row in enumerate(rows, 1):
        try:
            status = row.find_element(By.XPATH, './td[6]').text.strip()

            if status == "Ditindak":
                try:
                    # Upload file bukti
                    file_input = row.find_element(By.XPATH, './/input[@type="file"]')
                    upload_button = row.find_element(By.XPATH, './/button[contains(text(), "Upload")]')

                    file_input.send_keys(bukti_path)
                    time.sleep(1)
                    upload_button.click()
                    time.sleep(2)

                    log_to_file("Upload Bukti", "Berhasil", f"Notifikasi ke-{i} diupload")

                    # Refresh halaman agar form upload hilang (karena status bisa berubah)
                    driver.get("http://127.0.0.1:9000/notifikasi/saya/")
                    time.sleep(2)
                    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')  # refresh rows

                except Exception as e:
                    log_to_file("Upload Bukti", "Gagal", f"Notifikasi ke-{i} error: {str(e)}")
            else:
                log_to_file("Upload Bukti", "Lewat", f"Notifikasi ke-{i} status: {status}")
        except NoSuchElementException:
            log_to_file("Upload Bukti", "Gagal", f"Notifikasi ke-{i} elemen tidak ditemukan")

except Exception as e:
    log_to_file("Error Umum", "Gagal", str(e))

driver.quit()
