
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.samfaa.ir/")
        print("در حال بارگذاری صفحه...")
        time.sleep(12)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        movies_section = soup.find_all("div", class_="v-card")

        output_html = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: Tahoma, sans-serif; background: #f7f7f7; padding: 20px; }
    h1 { text-align: center; color: #333; }
    .grid { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
    .card {
      width: 22%;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow: hidden;
      direction: rtl;
      text-align: center;
      padding-bottom: 10px;
    }
    .card img {
      width: 100%;
      height: 300px;
      object-fit: cover;
      border-bottom: 1px solid #eee;
    }
    .card h3 {
      margin: 10px 0 5px;
      font-size: 18px;
      color: #014874;
    }
    .card p {
      font-size: 14px;
      padding: 0 10px;
      color: #444;
    }
    @media (max-width: 768px) {
      .card { width: 45%; }
    }
    @media (max-width: 500px) {
      .card { width: 100%; }
    }
  </style>
</head>
<body>
  <h1>فیلم‌های در حال اکران</h1>
  <div class="grid">'''

        count = 0
        for div in movies_section:
            img_tag = div.find("img")
            title_tag = div.find("h3") or div.find("span")
            if not img_tag or not title_tag:
                continue
            img_src = img_tag.get("src")
            title = title_tag.get_text(strip=True)
            output_html += f'''
    <div class="card">
      <img src="{img_src}" alt="{title}">
      <h3>{title}</h3>
      <p>در حال اکران در سینماهای کشور</p>
    </div>'''
            count += 1
            if count >= 12:
                break

        output_html += '''
  </div>
</body>
</html>'''

        os.makedirs("public", exist_ok=True)
        with open("public/now_showing.html", "w", encoding="utf-8") as f:
            f.write(output_html)

        print("فایل now_showing.html با موفقیت ساخته شد.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
