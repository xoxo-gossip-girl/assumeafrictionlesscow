import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

page = scraper.get("https://letterboxd.com/film/the-chronology-of-water/fans/")

with open("output.html", "w", encoding="utf-8") as f:
    f.write(page.text)