import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_movies():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.cinematicket.org/")

    time.sleep(10)  # صبر برای بارگذاری کامل JS

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    movies = []

    for movie_card in soup.select(".movie-card"):
        title_tag = movie_card.select_one(".movie-name")
        desc_tag = movie_card.select_one(".desc")

        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "بدون عنوان"

        if desc_tag:
            description = desc_tag.text.strip()
        else:
            description = ""

        poster = movie_card.select_one("img")
        poster_url = poster["src"] if poster and "src" in poster.attrs else ""

        movies.append({
            "title": title,
            "description": description,
            "poster": poster_url
        })

    return movies

def generate_html(movies):
    now = time.strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body {{
            font-family: sans-serif;
            background: #f7f7f7;
            color: #111;
            padding: 30px;
        }}
        h1 {{
            text-align: right;
            font-size: 28px;
        }}
        .updated {{
            text-align: right;
            font-size: 14px;
            color: #666;
            margin-bottom: 30px;
        }}
        .movie {{
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
            gap: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .movie img {{
            width: 120px;
            height: auto;
            border-radius: 6px;
        }}
        .movie .info {{
            flex: 1;
        }}
        .movie .title {{
            font-size: 20px;
            margin-bottom: 8px;
        }}
        .movie .desc {{
            font-size: 15px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <h1>فیلم‌های در حال اکران</h1>
    <div class="updated">آخرین بروزرسانی: {now}</div>
"""
    for movie in movies:
        html += f"""
    <div class="movie">
        <img src="{movie['poster']}" alt="{movie['title']}">
        <div class="info">
            <div class="title">{movie['title']}</div>
            <div class="desc">{movie['description']}</div>
        </div>
    </div>
"""
    html += """
</body>
</html>
"""
    return html

def main():
    movies = fetch_movies()
    html = generate_html(movies)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
