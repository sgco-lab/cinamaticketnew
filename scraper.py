import requests
import os

def fetch_movies():
    url = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        print("خطا در دریافت داده‌ها:", response.status_code)
        return []

def generate_html(movies):
    html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <style>
    body {
      font-family: sans-serif;
      background: #f4f4f4;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .card {
      background: white;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .card img {
      width: 100%;
      height: 350px;
      object-fit: cover;
    }
    .card-content {
      padding: 15px;
    }
    .card-content h3 {
      margin: 0 0 10px;
      font-size: 18px;
      color: #014874;
    }
    .card-content p {
      margin: 5px 0;
      font-size: 14px;
      color: #555;
    }
  </style>
</head>
<body>
  <h1>فیلم‌های در حال اکران</h1>
  <div class="grid">
"""

    for movie in movies:
        info = movie.get("movie", {})
        html += f"""
    <div class="card">
      <img src="{info.get("photo", "")}" alt="{info.get("title", "فیلم")}">
      <div class="card-content">
        <h3>{info.get("title", "عنوان نامشخص")}</h3>
        <p><strong>کارگردان:</strong> {info.get("director", "نامشخص")}</p>
        <p><strong>تعداد بلیت:</strong> {movie.get("total_tickets", 0)}</p>
        <p><strong>تعداد سالن:</strong> {movie.get("total_cinemas", 0)}</p>
        <p><strong>تعداد سانس:</strong> {movie.get("total_shows", 0)}</p>
      </div>
    </div>
"""

    html += """
  </div>
</body>
</html>"""

    os.makedirs("public", exist_ok=True)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    movies = fetch_movies()
    generate_html(movies)
