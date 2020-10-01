import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests
import re
from datetime import datetime


def get_movie_value(link):
    '''
    Makes a DataFrame from as many pages as requested.

    '''
    base_url = 'https://www.imdb.com'

    url = base_url + link

    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page)

    headers = ['movie title', 'imdb rating', 'imdb raters', 'mpaa', 'genres', 'director', 'writer', 'stars', 'country', 'language',
               'release date', 'budget', 'opening weekend', 'gross usa', 'cumulative worldwide', 'production companies', 'runtime']

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

    # Collect country
    

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
    try:
        data_list1[10] = datetime.strptime(data_list1[10], '%d %B %Y').date()
    except:
        None

    # Clean up money categories
    try:
        data_list1[11:15] = [money_to_int(trait)
                             for trait in data_list1[11:15]]
    except:
        None

    # Clean up runtime
    data_list1[-1] = data_list1[-1].split(' ')[0]

    # Create movie dictionary and return
    movie_dict = dict(zip(headers, data_list1))

    return movie_dict


def money_to_int(moneystring):
    moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)
