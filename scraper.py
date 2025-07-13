import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_and_generate():
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.samfaa.ir/")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    films = soup.find_all("div", class_="movie-item")
    html_output = "<html><head><meta charset='utf-8'><title>اکران روز</title></head><body><h2>فیلم‌های در حال اکران</h2>"

    for film in films:
        title = film.find("h3").text.strip()
        desc = film.find("p").text.strip()
        img = film.find("img")["src"]

        html_output += f"<div style='margin-bottom:20px;'>"
        html_output += f"<img src='{img}' alt='{title}' width='200'><br>"
        html_output += f"<strong>{title}</strong><br><em>{desc}</em></div>"

    html_output += "</body></html>"

    os.makedirs("public", exist_ok=True)
    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html_output)

if __name__ == "__main__":
    fetch_and_generate()
