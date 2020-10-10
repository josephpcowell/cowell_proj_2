"""
This file contains functions to help organize data scraped from IMDb.
"""

from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests
import re
from datetime import datetime


def get_movie_data(link):
    """
    Makes a Dicitonary of movies and it's information.

    Args:
        link: A string that is the end of a IMDb url for a specific movie.

    Returns:
        A dictionary with information regarding the movie that is associated with the link passed in.
    """
    base_url = "https://www.imdb.com"

    url = base_url + link

    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page)

    headers = [
        "movie title",
        "imdb rating",
        "imdb raters",
        "mpaa",
        "genres",
        "director",
        "writer",
        "stars",
        "country",
        "language",
        "release date",
        "budget",
        "opening weekend",
        "gross usa",
        "cumulative worldwide",
        "production companies",
        "runtime (min)",
    ]

    # Collect movie title
    try:
        title = (
            soup.find(class_="title_wrapper").find("h1").text.split("\xa0")[0]
        )
    except:
        title = None

    # Collect rating out of 10
    try:
        rating_10 = float(soup.find(class_="ratingValue").span.text)
    except:
        rating_10 = None

    # Collect number of raters
    try:
        raters = int(
            soup.find(class_="ratingValue")
            .strong["title"]
            .split()[3]
            .replace(",", "")
        )
    except:
        raters = None

    # Collection MPAA
    mpaa_options = [
        "G",
        "PG",
        "PG-13",
        "R",
        "NC-17",
        "TV-MA",
        "Unrated",
        "Not Rated",
    ]
    try:
        mpaa = soup.find(class_="subtext").text
        mpaa = mpaa.split("\n")[1].strip()
        if mpaa not in mpaa_options:
            mpaa = None
    except:
        mpaa = None

    # Collect genres
    try:
        genre = soup.find("h4", text=re.compile("Genre")).findParent().text
        genre = [
            ele.strip().replace("\xa0|", "") for ele in genre.split("\n")[2:-1]
        ]
    except:
        genre = None

    # Collect director
    try:
        director = (
            soup.find_all(class_="credit_summary_item")[0]
            .text.split("\n")[-1]
            .strip()
        )
    except:
        director = None

    # Collect writer
    try:
        writer = (
            soup.find_all(class_="credit_summary_item")[1]
            .text.split("\n")[2]
            .split(",")[0]
        )
        writer = writer.split("(")[0].strip()
    except:
        writer = None

    # Collect and clean list of stars
    try:
        stars_unclean = (
            soup.find_all(class_="credit_summary_item")[2]
            .text.split("\n")[2]
            .split(",")
        )
        stars = [i.replace("|", "").strip() for i in stars_unclean]
    except:
        stars = None

    # Collect country
    try:
        country = soup.find("h4", text=re.compile("Country")).findNext().text
    except:
        country = None

    # Collect language
    try:
        language = soup.find("h4", text=re.compile("Language")).findNext().text
    except:
        language = None

    # Collect and clean release data
    try:
        release_date = (
            soup.find("h4", text=re.compile("Release Date")).findParent().text
        )
        release_date = (
            release_date.split("\n")[1].split(":")[1].split("(")[0].strip()
        )
        release_date = datetime.strptime(release_date, "%d %B %Y").date()
    except:
        release_date = None

    # Collect budget
    try:
        budget = soup.find("h4", text=re.compile("Budget")).findParent().text
        budget = budget.split("\n")[1].split(":")[1]
        budget = money_to_int(budget)
    except:
        budget = None

    # Collect opening weekend
    try:
        opening_weekend = (
            soup.find("h4", text=re.compile("Opening Weekend"))
            .findParent()
            .text
        )
        opening_weekend = (
            opening_weekend.split("\n")[1].split(":")[1].strip(" ,")
        )
        opening_weekend = money_to_int(opening_weekend)
    except:
        opening_weekend = None

    # Collect GROSS USA
    try:
        gross_usa = (
            soup.find("h4", text=re.compile("Gross USA")).findParent().text
        )
        gross_usa = gross_usa.split("\n")[1].split(":")[1].strip(" ,")
        gross_usa = money_to_int(gross_usa)
    except:
        gross_usa = None

    # Collect worldwide gross
    try:
        worldwide = (
            soup.find("h4", text=re.compile("Cumulative Worldwide"))
            .findParent()
            .text
        )
        worldwide = worldwide.split(":")[1].strip()
        worldwide = money_to_int(worldwide)
    except:
        worldwide = None

    # Collect production companies
    try:
        production_co = (
            soup.find("h4", text=re.compile("Production Co")).findParent().text
        )
        production_co = production_co.split("\n")[2].strip()
        production_co = [co.strip() for co in production_co.split(",")]
    except:
        production_co = None

    # Collect runtime
    try:
        runtime = soup.find("h4", text=re.compile("Runtime")).findParent().text
        runtime = int(runtime.split("\n")[2].split(" ")[0])
    except:
        runtime = None

    data_list = [
        title,
        rating_10,
        raters,
        mpaa,
        genre,
        director,
        writer,
        stars,
        country,
        language,
        release_date,
        budget,
        opening_weekend,
        gross_usa,
        worldwide,
        production_co,
        runtime,
    ]

    movie_dict = dict(zip(headers, data_list))

    return movie_dict


def money_to_int(moneystring):
    """
    Cleans up money information.

    Args:
        moneystring: a string that contains commas and a dollar sign

    Returns:
        An integer representing the dollar amount passed in.
    """
    moneystring = moneystring.replace("$", "").replace(",", "")
    return int(moneystring)
