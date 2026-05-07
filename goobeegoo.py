import requests
from bs4 import BeautifulSoup
import cloudscraper
from collections import Counter
import re
username = 'charlesbass'
URL = f'https://www.letterboxd.com/{username}/'
scraper = cloudscraper.create_scraper()
page = scraper.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
fav_section = soup.find('section', id='favourites')
user_film_names = [
    div['data-item-name']
    for div in fav_section.find_all('div', attrs={'data-item-name': True})
]
user_url_film_names = [
    div['data-item-slug']
    for div in fav_section.find_all('div', attrs={'data-item-slug': True})
]
all_users = [[], [], [], []]
for i in range(0, 4):
    all_users[i] = set()
    name = user_url_film_names[i]
    # new_url = f'https://www.letterboxd.com/film/{name}/'
    # new_page = scraper.get(new_url)
    # new_soup = BeautifulSoup(page.content, 'html.parser')

    for j in range(1, 257):
        new_url = f'https://www.letterboxd.com/film/{name}/fans/page/{j}/'
        new_page = scraper.get(new_url)
        new_soup = BeautifulSoup(new_page.content, 'html.parser')
        film_user_names = set([
            div['data-username']
            for div in new_soup.find_all('div', attrs={'data-username': True})
            ])
        if not film_user_names:
            break
        for user in film_user_names:
            all_users[i].add(user)

print(all_users)

combined_list = []
for user_set in all_users:
    combined_list.extend(list(user_set))

counts = Counter(combined_list)

top_fans = counts.most_common(10)

print("--- Top Taste Matches ---")
for user, score in top_fans:
    if score > 1:
        print(f"{user}: {score}/4 films shared")
