from urllib.parse import quote

import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def url_2_soup(url):
    """Get the BeautifulSoup object for a URL"""
    session = HTMLSession()
    resp = session.get(url)
    return BeautifulSoup(resp.html.html, "html.parser")


def get_jd_url(keywords):
    """Return the URL for a JD search based on a keyword"""
    return f"https://search.jd.com/Search?keyword={quote(keywords)}"


def get_jd_image(prod):
    """Get the image of a given JD product"""
    path = prod.find("div", class_="p-img").find("img").attrs["data-lazy-img"].strip()
    return "http:" + path


def get_df_jd(keywords):
    """Get a dataframe for the results of a JD search"""
    url = get_jd_url(keywords)
    soup = url_2_soup(url)
    products = soup.find_all("div", {"class": "gl-i-wrap"})
    data_products = [
        {
            "name": p.find("div", class_="p-name").text.strip(),
            "price": float(p.find("div", class_="p-price").find("i").text.strip()),
            "image": get_jd_image(p),
        }
        for p in products
    ]
    return pd.DataFrame(data_products)

  
# TODO: Replace ... with implementation of web scrappers

def get_amazon_url(keywords, domain="co.uk"):
    """Return the URL for an Amazon search based on a keyword"""
    ...



def get_amazon_price(prod):
    """Get the price of a given Amazon product"""
    ...


def get_df_amazon(keywords, domain="co.uk"):
    """Get a dataframe for the results of a Amazon search"""
    ...


def get_newegg_url(keywords):
    """Return the URL for an NewEgg search based on a keyword"""
    return f"https://www.newegg.com/p/pl?d={quote(keywords)}"


def get_newegg_price(price_current):
    """Process the price of a result (string) and return the string"""
    import re

    return float(re.sub(r".*?([\d\.]+).*", r"\1", price_current))


def get_df_newegg(keywords):
    """Get a dataframe for the results of a NewEgg search"""
    url = get_newegg_url(keywords)
    soup = url_2_soup(url)
    products = soup.find_all("div", class_="item-container")
    data_products = [
        {
            "name": p.find("a", class_="item-title").text.strip(),
            "price": get_newegg_price(p.find("li", class_="price-current").text),
        }
        for p in products
        if p.find("li", class_="price-current").text
    ]
    return pd.DataFrame(data_products)
