from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

def clean_text(text):
    return text.strip().replace('\n', '').replace('\r', '')

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=fa-IR")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.samfaa.ir/")
        time.sleep(10)  # برای بارگذاری جاوااسکریپت

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # پیدا کردن بخش فیلم‌ها
        films_section = soup.find_all("div", class_="movie-card")
        print(f"تعداد فیلم پیدا شده: {len(films_section)}")

        cards_html = ""

        for film in films_section:
            title_tag = film.find("h5")
            title = clean_text(title_tag.get_text()) if title_tag else "بدون عنوان"

            desc_tag = film.find("p")
            description = clean_text(desc_tag.get_text()) if desc_tag else ""

            img_tag = film.find("img")
            image_url = img_tag["src"] if img_tag else ""

            card = f"""
            <div class="movie-card">
              <img src="{image_url}" alt="{title}">
              <div class="movie-info">
                <h3>{title}</h3>
                <p>{description}</p>
              </div>
            </div>
            """
            cards_html += card

        # تولید فایل نهایی
        output_html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <style>
    body {{ font-family: sans-serif; background: #f9f9f9; padding: 20px; }}
    h1 {{ text-align: center; color: #333; }}
    .movies-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }}
    .movie-card {{
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      overflow: hidden;
      text-align: center;
      transition: transform 0.2s;
    }}
    .movie-card:hover {{
      transform: scale(1.02);
    }}
    .movie-card img {{
      width: 100%;
      height: 340px;
      object-fit: cover;
    }}
    .movie-info {{
      padding: 10px 15px;
    }}
    .movie-info h3 {{
      font-size: 16px;
      margin: 10px 0 5px;
    }}
    .movie-info p {{
      font-size: 14px;
      color: #666;
      margin: 2px 0;
    }}
  </style>
</head>
<body>
  <h1>فیلم‌های در حال اکران</h1>
  <div class="movies-grid">
    {cards_html}
  </div>
</body>
</html>
        """

        # ساخت دایرکتوری public در صورت نبود
        os.makedirs("public", exist_ok=True)

        with open("public/now_showing.html", "w", encoding="utf-8") as f:
            f.write(output_html)

        print("✅ فایل public/now_showing.html ساخته شد.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
