from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import shutil
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
        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        movie_cards = soup.select(".v-card.v-sheet.theme--light")  # انتخاب کارت‌های فیلم

        movies = []
        for card in movie_cards:
            title_tag = card.select_one(".title.font-weight-bold")
            director_tag = card.select_one(".mt-1.font-italic")
            duration_tag = card.select_one(".caption.mt-1")
            img_tag = card.select_one("img")

            if not title_tag or not img_tag:
                continue

            title = title_tag.text.strip()
            director = director_tag.text.strip() if director_tag else "—"
            duration = duration_tag.text.strip() if duration_tag else "—"
            img = img_tag["src"]

            movies.append({
                "title": title,
                "director": director,
                "duration": duration,
                "img": img
            })

        # تولید HTML
        html_output = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <style>
    body { font-family: sans-serif; background: #f9f9f9; padding: 20px; }
    h1 { text-align: center; color: #333; }
    .movies-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .movie-card {
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      overflow: hidden;
      text-align: center;
      transition: transform 0.2s;
    }
    .movie-card:hover {
      transform: scale(1.02);
    }
    .movie-card img {
      width: 100%;
      height: 340px;
      object-fit: cover;
    }
    .movie-info {
      padding: 10px 15px;
    }
    .movie-info h3 {
      font-size: 16px;
      margin: 10px 0 5px;
    }
    .movie-info p {
      font-size: 14px;
      color: #666;
      margin: 2px 0;
    }
  </style>
</head>
<body>
  <h1>فیلم‌های در حال اکران</h1>
  <div class="movies-grid">
        """

        for m in movies:
            html_output += f"""
    <div class="movie-card">
      <img src="{m['img']}" alt="{m['title']}">
      <div class="movie-info">
        <h3>{m['title']}</h3>
        <p>کارگردان: {m['director']}</p>
        <p>مدت زمان: {m['duration']}</p>
      </div>
    </div>
            """

        html_output += """
  </div>
</body>
</html>
        """

        # ذخیره در فایل موقت
        with open("samfaa_page.html", "w", encoding="utf-8") as f:
            f.write(html_output)

        # اطمینان از وجود پوشه public
        os.makedirs("public", exist_ok=True)
        shutil.copyfile("samfaa_page.html", "public/now_showing.html")
        print("فایل HTML با موفقیت ساخته و کپی شد.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
