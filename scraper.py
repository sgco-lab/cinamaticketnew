import requests
from pathlib import Path

url = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

response = requests.get(url)
data = response.json()

movies = data.get("data", [])

html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فیلم‌های در حال اکران</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: sans-serif;
      background: #f0f0f0;
      margin: 0;
      padding: 20px;
      direction: rtl;
    }
    h1 {
      text-align: center;
      margin-bottom: 30px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
    }
    .card {
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: transform 0.3s ease;
    }
    .card:hover {
      transform: scale(1.03);
    }
    .poster {
      width: 100%;
      height: 300px;
      object-fit: cover;
    }
    .info {
      padding: 15px;
    }
    .info h2 {
      margin: 0 0 10px;
      font-size: 18px;
    }
    .info p {
      margin: 5px 0;
      color: #444;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <h1>فیلم‌های در حال اکران</h1>
  <div class="grid">
"""

for movie in movies:
    title = movie.get("fa_name", "نامشخص")
    director = movie.get("director", "نامشخص")
    ticket = "{:,}".format(movie.get("ticket_count", 0))
    hall = "{:,}".format(movie.get("hall_count", 0))
    session = "{:,}".format(movie.get("session_count", 0))
    poster = movie.get("poster_url", "")

    html += f"""
    <div class="card">
      <img class="poster" src="{poster}" alt="{title}">
      <div class="info">
        <h2>{title}</h2>
        <p>کارگردان: {director}</p>
        <p>تعداد بلیت: {ticket}</p>
        <p>تعداد سالن: {hall}</p>
        <p>تعداد سانس: {session}</p>
      </div>
    </div>
    """

html += """
  </div>
</body>
</html>
"""

Path("now_showing.html").write_text(html, encoding="utf-8")
