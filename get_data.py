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


def get_amazon_url(keywords, domain="co.uk"):
    """Return the URL for an Amazon search based on a keyword"""
    return f"https://www.amazon.{domain}/s?k={quote(keywords)}"


def get_amazon_price(prod):
    """Get the price of a given Amazon product"""
    import re
    # We will have to remove the currency symbol
    # We will also have to transform "," to "." if we use prices from France or Germany
    # ... However, the "," is used as separator for thousands in the prices as well
    # ... so the best way is to use regular expressions (regex) to extract the price
    price_str =  prod.find("span", class_="a-price").find("span", class_="a-offscreen")
    digits = re.findall(r"\d+", price_str.text)
    if len(digits) == 1:
        return float(digits[0])
    elif len(digits) > 1:
        return float("".join(digits[:-1]) + "." + digits[-1])


def get_df_amazon(keywords, domain="co.uk"):
    """Get a dataframe for the results of a Amazon search"""
    url = get_amazon_url(keywords, domain=domain)
    soup = url_2_soup(url)
    products = soup.find("div", class_="s-matching-dir").find_all(
        "div", class_="sg-col-inner"
    )
    data_products = [
        {
            "name": p.find("h2").text.strip(),
            "price": get_amazon_price(p),
        }
        for p in products
        if p.find("h2") and p.find("span", class_="a-price")
    ]
    return pd.DataFrame(data_products)


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
