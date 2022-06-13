import re

import requests
from bs4 import BeautifulSoup

url = "https://nl.trustpilot.com/review/{your trustpilot company}"


class Review:
    def __init__(self, title, text, stars, author, date):
        self.title = title
        self.text = text
        self.stars = stars
        self.author = author
        self.date = date

    def as_dict(self):
        return {"title": self.title, "text": self.text, "stars": self.stars, "author": self.author, "date": self.date}


def scrape_trustpilot() -> list[Review]:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    review_div_regex = re.compile(".*reviewCard*.")
    review_div = soup.find_all("div", {"class": review_div_regex})
    reviews = []

    for rd in review_div:
        title_regex = re.compile(".*reviewTitle*.")
        title = rd.findNext("h2", {"class": title_regex}).get_text()

        # For now I couldn't find a specific classname for the actual text.
        text = rd.findNext("p").get_text()

        # For now I couldn't find a specific classname for the stars emblem.
        stars = rd.findNext("img")
        if stars["src"] and stars["src"].endswith("svg"):
            # This should return an integer of the amount of stars the reviewer has given.
            stars = int(stars["src"][-5:-4])

        author_regex = re.compile(".*consumerName*.")
        author = rd.findNext("div", {"class": author_regex}).get_text()

        date = rd.findNext("time")["datetime"]

        reviews.append(Review(title=title, text=text, author=author, stars=stars, date=date))
    return reviews


scrape_trustpilot()
