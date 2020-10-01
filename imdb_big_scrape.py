import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests


def get_movie_links(pages):
    """
    input: number of pages you want to scrape
    output: return list containing links to movie pages
    """
    links = []
    num_pages = [1,101,201,301,401,501,601,701,801,901]
    for i in range(pages):
        start = num_pages[pages-1]
        url = f'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start={start}&ref_=adv_nxt'
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page)
        search1 = soup.find_all(class_='lister-item-index unbold text-primary')
        link_list = [i.findNext().findChildren()[0]['href'] for i in search1]
        links.extend(link_list)
    return links

