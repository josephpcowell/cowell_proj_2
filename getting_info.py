import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests
import re
from datetime import datetime


def get_movie_data(link):
    '''
    Makes a DataFrame from as many pages as requested.

    '''
    base_url = 'https://www.imdb.com'

    url = base_url + link

    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page)

    headers = ['movie title', 'imdb rating', 'imdb raters', 'mpaa', 'genres', 'director', 'writer', 'stars', 'country', 'language',
               'release date', 'budget', 'opening weekend', 'gross usa', 'cumulative worldwide', 'production companies', 'runtime (min)']

    # Collect movie title
    title = soup.find(class_='title_wrapper').find(
        'h1').text.split('\xa0')[0]

    # Collect rating out of 10
    rating_10 = float(soup.find(class_='ratingValue').span.text)

    # Collect number of raters
    raters = int(soup.find(class_='ratingValue').strong['title'].split()[
        3].replace(',', ''))

    # Segment data to make extraction easier
    subtext = soup.find(class_='subtext').text.split('\n')

    # Collection MPAA
    mpaa = subtext[1].strip()

    # Collect genres
    genre = soup.find('h4', text=re.compile('Genre')).findParent().text
    genre = [ele.strip().replace('\xa0|', '')
             for ele in genre.split('\n')[2:-1]]

    # Collect director
    director = soup.find_all(class_='credit_summary_item')[
        0].text.split('\n')[-1].strip()

    # Collect writer
    writer = soup.find_all(class_='credit_summary_item')[
        1].text.split('\n')[2].split(',')[0]
    writer = writer.split('(')[0].strip()

    # Collect and clean list of stars
    stars_unclean = soup.find_all(class_='credit_summary_item')[
        2].text.split('\n')[2].split(',')
    stars = [i.replace('|', "").strip() for i in stars_unclean]

    # Collect country
    country = soup.find('h4', text=re.compile('Country')).findNext().text

    # Collect language
    language = soup.find('h4', text=re.compile('Language')).findNext().text

    # Collect and clean release data
    release_date = soup.find('h4', text=re.compile(
        'Release Date')).findParent().text
    release_date = release_date.split(
        '\n')[1].split(':')[1].split('(')[0].strip()
    release_date = datetime.strptime(release_date, '%d %B %Y').date()

    # Collect budget
    budget = soup.find('h4', text=re.compile('Budget')).findParent().text
    budget = budget.split('\n')[1].split(':')[1]
    budget = money_to_int(budget)

    # Collect opening weekend
    try:
        opening_weekend = soup.find('h4', text=re.compile(
            'Opening Weekend')).findParent().text
        opening_weekend = opening_weekend.split(
            '\n')[1].split(':')[1].strip(' ,')
        opening_weekend = money_to_int(opening_weekend)
    except:
        opening_weekend = None

    # Collect GROSS USA
    try:
        gross_usa = soup.find('h4', text=re.compile(
            'Gross USA')).findParent().text
        gross_usa = gross_usa.split('\n')[1].split(':')[1].strip(' ,')
        gross_usa = money_to_int(gross_usa)
    except:
        gross_usa = None

    # Collect worldwide gross
    worldwide = soup.find('h4', text=re.compile(
        'Cumulative Worldwide')).findParent().text
    worldwide = worldwide.split(':')[1].strip()
    worldwide = money_to_int(worldwide)

    # Collect production companies
    production_co = soup.find('h4', text=re.compile(
        'Production Co')).findParent().text
    production_co = production_co.split('\n')[2].strip()
    production_co = [co.strip() for co in production_co.split(',')]

    # Collect runtime
    runtime = soup.find('h4', text=re.compile('Runtime')).findParent().text
    runtime = int(runtime.split('\n')[2].split(' ')[0])

    data_list = [title, rating_10, raters, mpaa, genre,
                 director, writer, stars, country, language,
                 release_date, budget, opening_weekend, gross_usa, worldwide,
                 production_co, runtime]

    movie_dict = dict(zip(headers, data_list))

    return movie_dict


def money_to_int(moneystring):
    moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)
