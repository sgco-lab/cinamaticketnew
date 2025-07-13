import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_and_generate():
    # تنظیمات headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ساخت درایور
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # رفتن به سایت سامفا
    url = "https://www.samfaa.ir/"
    print("⏳ در حال بارگذاری:", url)
    driver.get(url)
    time.sleep(5)  # زمان برای بارگذاری کامل

    # دریافت HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # پیدا کردن فیلم‌ها (المان‌هایی که خودت باید دقیق تنظیم کنی)
    movies_section = soup.find_all("div", class_="card")

    if not movies_section:
        print("⚠️ هیچ فیلمی پیدا نشد.")
    else:
        print(f"✅ تعداد فیلم‌ها: {len(movies
