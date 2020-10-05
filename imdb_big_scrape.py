import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests


def get_movie_links(pages, start=1):
    """
    The basis is movies released between 2015 and 2020
    input: number of pages you want to scrape and the starting page
    output: return list containing links to movie pages
    """
    links = []
    for i in range(pages):
        url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2015-01-01,2020-05-01&countries=us&languages=en&view=simple&count=100&start={start}&ref_=adv_nxt"
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page)
        search1 = soup.find_all(class_="lister-item-index unbold text-primary")
        link_list = [i.findNext().findChildren()[0]["href"] for i in search1]
        links.extend(link_list)
        start += 100
    return links
