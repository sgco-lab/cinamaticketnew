from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def main():
    # تنظیمات مرورگر برای headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # راه‌اندازی مرورگر
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # باز کردن سایت
        driver.get("https://www.samfaa.ir/")
        print("در حال بارگذاری صفحه...")
        time.sleep(10)  # صبر برای اجرای JavaScript

        # دریافت HTML نهایی بعد از اجرای JS
        page_source = driver.page_source

        # ذخیره در فایل برای بررسی دستی
        with open("samfaa_page.html", "w", encoding="utf-8") as f:
            f.write(page_source)

        print("صفحه ذخیره شد. فایل: samfaa_page.html")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
