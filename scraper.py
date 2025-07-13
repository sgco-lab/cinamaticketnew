import requests
import datetime

url = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200 and response.text.strip():
    data = response.json()

    html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>فیلم‌های در حال اکران</title>
  <style>
    body {
      font-family: sans-serif;
      background: #f9f9f9;
      color: #333;
      padding: 20px;
      direction: rtl;
      text-align: right;
    }
    .movie {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      padding: 15px;
      margin-bottom: 20px;
    }
    .movie img {
      max-width: 200px;
      border-radius: 8px;
    }
    .details {
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <h2>فیلم‌های در حال اکران</h2>
"""

    for movie in data:
        title = movie.get("fa_name", "بدون عنوان")
        poster = movie.get("poster_url", "")
        director = movie.get("director", "")
        description = movie.get("description", "")

        html += f"""
  <div class="movie">
    <img src="{poster}" alt="{title}">
    <div class="details">
      <h3>{title}</h3>
      <p><strong>کارگردان:</strong> {director}</p>
      <p>{description}</p>
    </div>
  </div>
"""

    html += f"""
  <p style="text-align:center; font-size:14px; color:#777;">به‌روزرسانی: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</body>
</html>
"""

    with open("now_showing.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ فایل now_showing.html با {len(data)} فیلم ذخیره شد.")

else:
    print(f"❌ دریافت اطلاعات ناموفق بود. کد وضعیت: {response.status_code}")
