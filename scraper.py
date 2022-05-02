import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

# print(soup.prettify)

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

for container in movie_div:

    # extracting the name of the movie
    name = container.h3.a.text
    titles.append(name)

    # extracting the year of the movie
    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    # extracting the duration of the movie
    runtime = container.p.find('span', class_='runtime').text if container.p.find(
        'span', class_='runtime') else '-'
    time.append(runtime)

    # extracting imdb rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    # extracting the metascores
    m_score = container.find('span', class_='metascore').text if container.find(
        'span', class_='metascore') else '-'
    metascores.append(m_score)

    # extracting votes and gross earning
    nv = container.find_all('span', attrs={'name': 'nv'})

    # filtering nv for votes
    vote = nv[0].text
    votes.append(vote)

    # filter nv for gross
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,

})

# cleaning data with Pandas
# movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
# movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
# movies['metascore'] = movies['metascore'].astype(int)
# movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
# movies['us_grossMillions'] = movies['us_grossMillions'].map(
#     lambda x: x.lstrip('$').rstrip('M'))
# movies['us_grossMillions'] = pd.to_numeric(
#     movies['us_grossMillions'], errors='coerce')

movies.to_csv(
    '/Users/kaushikpilligundla/Desktop/web scraper/x.csv', index=False)
