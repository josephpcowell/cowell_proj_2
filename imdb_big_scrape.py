"""
A helper function to turn an IMDb search into a links to be further processed.
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests


def get_movie_links(pages, start=1):
    """
    Creates a list of links to be scraped for movie data

    Args: 
        pages: An int representing the number of pages that will be scraped
        start: An int representing the starting page in regard to the search. This number starts at 1 and increased by 100.
    
    Returns:
        A list containing links to movie pages
    """
    links = []
    for i in range(pages):
        url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2015-01-01,2020-05-01&countries=us&languages=en&view=simple&count=100&start={start}&ref_=adv_nxt"
        # ^ Movies from 2015 - 2020
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page)
        search1 = soup.find_all(class_="lister-item-index unbold text-primary")
        link_list = [i.findNext().findChildren()[0]["href"] for i in search1]
        links.extend(link_list)
        start += 100
    return links
