from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

def scrape_samfaa():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.samfaa.ir/")
        time.sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        films = soup.select('.card-content')
        movie_items = []

        for film in films:
            title = film.select_one('.movie-title')
            img = film.find_previous('img')
            desc = film.select_one('.movie-desc')

            name = title.text.strip() if title else "بدون عنوان"
            image_url = img['src'] if img else ""
            description = desc.text.strip() if desc else ""

            movie_items.append({
                'title': name,
                'image': image_url,
                'desc': description
            })

    finally:
        driver.quit()

    return movie_items

def generate_html(movies):
    html_content = """<!DOCTYPE html>
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

    for movie in movies:
        html_content += f"""
    <div class="movie-card">
      <img src="{movie['image']}" alt="{movie['title']}">
      <div class="movie-info">
        <h3>{movie['title']}</h3>
        <p>{movie['desc']}</p>
      </div>
    </div>
"""

    html_content += """
  </div>
</body>
</html>"""

    os.makedirs("public", exist_ok=True)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    movies = scrape_samfaa()
    generate_html(movies)
