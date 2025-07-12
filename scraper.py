from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

def fetch_movies():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.get("https://www.cinematicket.org/")

    time.sleep(10)  # صبر برای بارگذاری کامل JS

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    movies = []

    movie_sections = soup.find_all("div", class_="movie-card__info")
    for section in movie_sections:
        title = section.find("h2")
        desc = section.find("p")
        poster = section.find_previous("img")

        if title and poster:
            movies.append({
                "title": title.text.strip(),
                "description": desc.text.strip() if desc else "",
                "poster": poster['src']
            })

    return movies

def save_to_html(movies):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body {{
            font-family: sans-serif;
            background-color: #f9f9f9;
            color: #111;
            padding: 30px;
        }}
        h1 {{
            color: #000;
        }}
        .movie {{
            margin-bottom: 40px;
        }}
        .movie img {{
            width: 200px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <h1>فیلم‌های در حال اکران</h1>
    <p>آخرین بروزرسانی: {now}</p>
"""

    for m in movies:
        html += f"""
    <div class="movie">
        <h2>{m['title']}</h2>
        <img src="{m['poster']}" alt="{m['title']}">
        <p>{m['description']}</p>
    </div>
"""

    html += """
</body>
</html>
"""

    os.makedirs("public", exist_ok=True)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    movies = fetch_movies()
    save_to_html(movies)

if __name__ == "__main__":
    main()
