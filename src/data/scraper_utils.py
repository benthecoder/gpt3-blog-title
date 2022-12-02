import logging
import random
import re
import time
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup


def base_url_builder(tag):
    """Builds base url for tag"""
    url = "https://medium.com/tag/" + tag + "/archive/"
    return url


def get_cards(soup):
    """Pulls each card from feed"""
    cards = soup.find_all("div", class_="streamItem streamItem--postPreview js-streamItem")
    return cards


def get_title(cards):
    """Pulls title from each card"""

    def title_cleaner(title):
        """Cleans title of special characters"""
        title = title.replace("\xa0", " ")
        title = title.replace("\u200a", "")
        title = title.replace("\ufe0f", "")
        title = re.sub(r"[^\x00-\x7F]+", "", title)
        return title

    titles = []
    for card in cards:
        variant1 = card.find("h3", class_="graf graf--h3 graf-after--figure graf--title")
        variant2 = card.find(
            "h3", class_="graf graf--h3 graf-after--figure graf--trailing graf--title"
        )
        variant3 = card.find("h4", class_="graf graf--h4 graf--leading")
        variant4 = card.find("h3", class_="graf graf--h3 graf--leading graf--title")
        variant5 = card.find("p", class_="graf graf--p graf--leading")
        variant6 = card.find(
            "h3",
            class_="graf graf--h3 graf--startsWithDoubleQuote graf--leading graf--title",
        )
        variant7 = card.find(
            "h3",
            class_=(
                "graf graf--h3 graf--startsWithDoubleQuote graf-after--figure graf--trailing"
                " graf--title"
            ),
        )
        variants = [
            variant1,
            variant2,
            variant3,
            variant4,
            variant5,
            variant6,
            variant7,
        ]

        saved = False
        # save the first matched entry
        for variant in variants:
            if (variant is not None) and (not saved):
                title = variant.text
                title = title_cleaner(title)
                titles.append(title)
                saved = True
        if not saved:
            titles.append("NaN")

    return titles


def get_auth_and_pubs(cards):
    """get author and publication from each card"""
    authors = []
    pubs = []
    for card in cards:
        # get the author and publication
        author = card.find(
            "a",
            class_=(
                "ds-link ds-link--styleSubtle link link--darken link--accent"
                " u-accentColor--textNormal u-accentColor--textDarken"
            ),
        )
        pub = card.find(
            "a",
            class_=(
                "ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal"
            ),
        )
        if author is not None:
            text = author.text
            text = re.sub(r"\s+[^A-Za-z]", "", text)
            text = re.sub(r"[^\x00-\x7F]+", " ", text)
            authors.append(text)
        else:
            authors.append("NaN")
        if pub is not None:
            text2 = pub.text
            text2 = re.sub(r"\s+[^A-Za-z]", "", text2)
            text2 = re.sub(r"[^\x00-\x7F]+", " ", text2)
            pubs.append(text2)
        else:
            pubs.append("NaN")
    return authors, pubs


def get_read_time(cards):
    """Pulls read time from each card"""
    read_times = []
    for card in cards:
        time = card.find("span", class_="readingTime")
        if time is not None:
            time = time["title"]
            time = time.replace(" min read", "")
            read_times.append(time)
        else:
            read_times.append("0")
    return read_times


def get_claps(cards):
    """get claps from each card"""
    applause = []
    for card in cards:
        claps = card.find(
            "button",
            class_=(
                "button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton"
                " u-disablePointerEvents"
            ),
        )
        if claps is not None:
            applause.append(claps.text)
        else:
            applause.append("0")
    return applause


def get_url(cards):
    """get url from each card"""
    urls = []
    for card in cards:
        url = card.find("a", class_="")
        if url is not None:
            urls.append(url["href"])
        else:
            raise Exception("couldnt find a url")
    return urls


def pull_data(cards):
    """pull data from card and return dictionary"""

    titles = get_title(cards)
    authors, pubs = get_auth_and_pubs(cards)
    read_times = get_read_time(cards)
    claps = get_claps(cards)
    urls = get_url(cards)

    data = {
        "title": titles,
        "claps": claps,
        "read_time": read_times,
        "author": authors,
        "publication": pubs,
        "url": urls,
    }

    return data


def scrape_tag(tag, browser, path, start_date, end_date):
    """Scrapes posts from tag from start_date to end_date"""

    base_url = base_url_builder(tag)

    # parse dates
    start_date = datetime.strptime(start_date, "%Y/%m/%d")
    end_date = datetime.strptime(end_date, "%Y/%m/%d")

    # check if end date is after start date
    if start_date > end_date:
        raise Exception("start date exceeds end date")

    current_date = start_date
    counter = 0

    while current_date <= end_date:

        # build url
        url = base_url + current_date.strftime("%Y/%m/%d")

        # get page
        browser.get(url)
        html = browser.page_source

        # get soup
        soup = BeautifulSoup(html, features="lxml")

        # get cards
        cards = get_cards(soup)

        # get data
        data_dict = pull_data(cards)

        # create dataframe
        df = pd.DataFrame.from_dict(data_dict)

        # add date and tags
        df["date"] = current_date.strftime("%Y/%m/%d")
        df["tag"] = tag

        # save to csv
        with open(path / "medium.csv", "a") as f:
            df.to_csv(f, header=f.tell() == 0, index=False)

        # increment random days
        current_date += timedelta(days=random.randint(1, 3))

        # print progress count
        counter += len(cards)
        logging.info(f"scraped {counter} posts for {tag} on {current_date.strftime('%Y/%m/%d')}")
        time.sleep(random.randint(1, 5))

    browser.close()
