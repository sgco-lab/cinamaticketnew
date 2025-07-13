from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

# تنظیمات مرورگر برای headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# راه‌اندازی مرورگر
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# رفتن به صفحه اصلی سامفا
driver.get("https://www.samfaa.ir/")
time.sleep(5)

# استخراج HTML صفحه
html = driver.page_source
driver.quit()

# پردازش HTML با BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
movies = soup.select("div.card")  # فرض: هر فیلم در یک div.card نمایش داده می‌شود

# ساخت HTML خروجی
output_html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body { font-family: sans-serif; background: #f5f5f5; padding: 20px; direction: rtl; }
        .movie { background: white; border-radius: 8px; padding: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        img { max-width: 100%; border-radius: 8px; }
        .title { font-size: 18px; font-weight: bold; margin-top: 10px; }
        .desc { font-size: 14px; color: #444; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>فیلم‌های در حال اکران</h2>
"""

for movie in movies:
    title = movie.select_one(".card-title").get_text(strip=True) if movie.select_one(".card-title") else "بدون عنوان"
    desc = movie.select_one(".card-text").get_text(strip=True) if movie.select_one(".card-text") else ""
    img_tag = movie.select_one("img")
    img = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

    output_html += f"""
    <div class="movie">
        <img src="{img}" alt="{title}">
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
    </div>
    """

output_html += """
</body>
</html>
"""

# ساخت پوشه public در صورت نیاز
os.makedirs("public", exist_ok=True)

# ذخیره در فایل HTML
with open("public/now_showing.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print(f"تعداد فیلم‌ها: {len(movies)}")
