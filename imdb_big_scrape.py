import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests


def get_movie_links(pages):
    """
    input: number of pages you want to scrape
    """
    links = []
    url = 'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start=1&ref_=adv_nxt'
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page)
    link = soup.find_all(class_='lister-item mode-simple')
    return link
    # start = 1
    # for i in range(1, pages+1):
    #     url = f'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start={start}&ref_=adv_nxt'
    #     response = requests.get(url)
    #     page = response.text
    #     soup = BeautifulSoup(page)
    #     start += 100


# Set up page to scrape
url = 'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start=1&ref_=adv_nxt'
response = requests.get(url)
page = response.text
soup = BeautifulSoup(page)

# Select categories holding links for each movie
list1 = soup.find_all(class_='lister-item-index unbold text-primary')

# Make a list of the end of the links
list2 = [i.findNext().findChildren()[0]['href'] for i in list1]
