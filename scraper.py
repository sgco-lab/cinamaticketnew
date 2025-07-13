import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

BASE_URL = "https://cinematicket.org/"
HTML_PATH = "public/now_showing.html"
os.makedirs("public", exist_ok=True)

def fetch_movies():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []
    for card in soup.select(".movie-card, .movie-item"):
        name = card.select_one(".movie-title, .title")
        img = card.select_one("img")
        desc = card.select_one(".movie-summary, .summary, .description")
        if name and img:
            movies.append({
                "name": name.get_text(strip=True),
                "poster": img["src"] if img["src"].startswith("http") else BASE_URL + img["src"].lstrip("/"),
                "desc": desc.get_text(strip=True) if desc else "بدون توضیح"
            })
    return movies

def generate_html(movies):
    with open("templates/base.html", encoding="utf-8") as f:
        base_html = f.read()

    movie_items = ""
    for movie in movies:
        movie_items += f'''
        <div class="movie">
            <img src="{movie['poster']}" alt="{movie['name']}">
            <div class="movie-title">{movie['name']}</div>
            <div class="movie-desc">{movie['desc']}</div>
        </div>
        '''

    final_html = base_html.replace("{{MOVIES}}", movie_items)
    final_html = final_html.replace("{{UPDATED_AT}}", datetime.now().strftime("%Y-%m-%d %H:%M"))

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    movies = fetch_movies()
    generate_html(movies)
