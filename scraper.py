import requests

URL = "https://www.samfaa.ir/api/v1/show/recent_shows?recently=all&province=0"

def fetch_and_generate():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            print("❌ خطا در دریافت اطلاعات:", response.status_code)
            print(response.text)
            return
        
        data = response.json()
        movies = data.get("data", [])
        print(f"🎬 تعداد فیلم‌ها: {len(movies)}")

        html = """
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="utf-8">
            <title>فیلم‌های در حال اکران</title>
            <style>
                body { font-family: sans-serif; direction: rtl; padding: 20px; }
                h2 { color: #014874; }
                img { max-width: 150px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
                li { margin-bottom: 30px; list-style: none; }
            </style>
        </head>
        <body>
            <h2>فیلم‌های فعال ({}) مورد</h2>
            <ul>
        """.format(len(movies))

        for movie in movies:
            name = movie.get("movie", {}).get("title", "بدون عنوان")
            poster = movie.get("movie", {}).get("poster_url", "")
            description = movie.get("movie", {}).get("summary", "")

            html += f"""
            <li>
                <h3>{name}</h3>
                <img src="{poster}" alt="{name}">
                <p>{description}</p>
            </li>
            """

        html += "</ul></body></html>"

        with open("now_showing.html", "w", encoding="utf-8") as f:
            f.write(html)

    except Exception as e:
        print("❌ خطا در اجرای برنامه:", str(e))

if __name__ == "__main__":
    fetch_and_generate()
