from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from jinja2 import Environment, FileSystemLoader
import time
import os

def fetch_movies():
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.cinematicket.org/")

    time.sleep(10)  # صبر برای بارگذاری کامل JS

    movies = []

    # استخراج اطلاعات فیلم‌ها
    cards = driver.find_elements(By.CSS_SELECTOR, '.movie-card')
    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, '.movie-title').text
            desc = card.find_element(By.CSS_SELECTOR, '.movie-story').text
            img = card.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

            movies.append({
                'title': title,
                'description': desc,
                'image_url': img
            })
        except:
            continue

    driver.quit()
    return movies

def save_html(movies):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('base.html')

    output = template.render(movies=movies)
    output_path = os.path.join("public", "now_showing.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

def main():
    movies = fetch_movies()
    save_html(movies)

if __name__ == "__main__":
    main()
