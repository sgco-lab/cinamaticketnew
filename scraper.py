from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

def fetch_html():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.samfaa.ir/")
        time.sleep(10)
        html = driver.page_source
    finally:
        driver.quit()

    return html

def extract_movies(html):
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.find_all("div", class_="v-card")

    movies = []
    for box in containers:
        img = box.find("img")
        title = box.find("h3")
        desc = box.find("p")

        if img and title:
            movies.append({
                "image": img['src'],
                "title": title.get_text(strip=True),
                "desc": desc.get_text(strip=True) if desc else "",
            })
    return movies

def generate_html(movies):
    html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <style>
    body {
      font-family: Tahoma, sans-serif;
      background-color: #f5f5f5;
      margin: 0;
      padding: 30px;
    }
    h2 {
      text-align: center;
      color: #444;
    }
    .grid {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      width: 250px;
      overflow: hidden;
      text-align: center;
    }
    .card img {
      width: 100%;
      height: 360px;
      object-fit: cover;
    }
    .card h3 {
      font-size: 18px;
      margin: 10px 0 5px 0;
      color: #333;
    }
    .card p {
      font-size: 14px;
      color: #666;
      padding: 0 10px 10px 10px;
    }
  </style>
</head>
<body>
  <h2>فیلم‌های در حال اکران</h2>
  <div class="grid">
"""
    for movie in movies:
        html += f"""
    <div class="card">
      <img src="{movie['image']}" alt="{movie['title']}">
      <h3>{movie['title']}</h3>
      <p>{movie['desc']}</p>
    </div>
"""
    html += """
  </div>
</body>
</html>
"""
    return html

def save_html(content):
    os.makedirs("public", exist_ok=True)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    html = fetch_html()
    movies = extract_movies(html)
    final_html = generate_html(movies)
    save_html(final_html)
    print("✅ فایل HTML ساخته شد: public/now_showing.html")

if __name__ == "__main__":
    main()
