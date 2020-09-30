from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests


def get_movie_value(soup):
    '''Grab all data from IMDb

    Takes in a soup variable and returns all the information
    for that movie.
    '''


    
    # Make main dataframe
    # Collect data

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
    # Collect unclean list of stars
    stars_unclean = soup.find_all(class_='credit_summary_item')[
        2].text.split('\n')[2].split(',')
    # Clean up stars
    stars = [i.replace('|', "").strip() for i in stars_unclean]
    # List of first elements
    detail_list_1 = [rating_10, raters, mpaa, genres, director, writer, stars]
    # Collect list with various interesting data points
    detail_list = [detail.findParent().text for detail in soup.find(
        id='titleDetails').find_all('h4')]
    # Select only necessary data points
    detail_list_2 = [detail_list[0], detail_list[1], detail_list[2], detail_list[5], detail_list[6],
                     detail_list[7], detail_list[8], detail_list[9], detail_list[10], detail_list[11], detail_list[13]]
    # Split up the data
    for counter, attribute in enumerate(detail_list_2):
        detail_list_2[counter] = attribute.split('\n')
    # Further selection of necessary data
    detail_list_3 = [detail_list_2[0][2], detail_list_2[1][2], detail_list_2[2][1], detail_list_2[3][1], detail_list_2[4][1],
                     detail_list_2[5][1], detail_list_2[6][1], detail_list_2[7][2], detail_list_2[8][2], detail_list_2[9][2], detail_list_2[10][1]]
    detail_list_1.extend(detail_list_3[:])
    movie_dict = {title: detail_list_1}
    return movie_dict


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
