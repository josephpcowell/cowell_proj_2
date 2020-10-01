import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests
import re
from datetime import datetime


def get_movie_data(pages):
    """
    input: number of pages you want to scrape
    """
    start = 1
    for i in range(1, pages+1):
        url = f'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start={start}&ref_=adv_nxt'
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page)
        start += 100


    # https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start=1&ref_=adv_nxt
    # https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt

    # url = f'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start={start}&ref_=adv_nxt'
    # response = requests.get(url)
    # response.status_code

    # page = response.text
    # soup = BeautifulSoup(page)

    # movies = {}

    # Make main dataframe
    # Collect data


def get_movie_value(soup):
    '''
    Makes a DataFrame from as many pages as requested.

    '''
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
    genres = [genre.replace(',', '').strip() for genre in subtext[6:8]]

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

    # Collect close information in list
    data_list1 = [title, rating_10, raters,
                  mpaa, genres, director, writer, stars]
    detail_list = [detail.findParent().text for detail in soup.find(
        id='titleDetails').find_all('h4')]
    detail_list_2 = [detail_list[0], detail_list[1], detail_list[2], detail_list[5], detail_list[6],
                     detail_list[7], detail_list[8], detail_list[9], detail_list[10]]
    for counter, attribute in enumerate(detail_list_2):
        detail_list_2[counter] = attribute.split('\n')
    detail_list_3 = [detail_list_2[0][2], detail_list_2[1][2], detail_list_2[2][1], detail_list_2[3][1], detail_list_2[4][1],
                     detail_list_2[5][1], detail_list_2[6][1], detail_list_2[7][2], detail_list_2[8][2]]
    data_list1.extend(detail_list_3[:])

    # Clean sections with description
    data_list1[10:15] = [trait.split(':')[1].strip(' ,')
                         for trait in data_list1[10:15]]

    # Clean up Production Company
    data_list1[15] = [trait.strip() for trait in data_list1[15].split(',')]

    # Clean up release date
    data_list1[10] = data_list1[10].split('(')[0].strip()
    data_list1[10] = datetime.strptime(data_list1[10], '%d %B %Y').date()

    # Clean up money categories
    data_list1[11:15] = [money_to_int(trait) for trait in data_list1[11:15]]

    # Clean up runtime
    data_list1[-1] = data_list1[-1].split(' ')[0]

    return data_list1


def money_to_int(moneystring):
    moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)


headers = ['movie title', 'imdb rating', 'imdb rater', 'mpaa', 'genres', 'director', 'writer', 'stars', 'country', 'language',
           'release date', 'budget', 'opening weekend', 'gross usa', 'cumulative worldwide', 'production companies', 'runtime']

# Title
# Rating 10
# Raters
# MPAA
# Genres
# Director
# Writer
# Stars

# Country
# Language
# Release Date
# Budget
# Opening Weekend
# Gross USA
# Cumulative Worldwide
# Production Company
# Length (min)
# Color
# Aspect Ratio
