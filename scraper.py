import requests
from bs4 import BeautifulSoup
from re import sub
from time import sleep
import pprint

# number of pages to take the articles from
# Crawl-delay: 30 requirement is built into the code
num_of_pages = 1

# points minimum for displayed articles
min_points = 100


def get_hn_stories(num_of_pages):
    articles_databank = []
    for number in range(num_of_pages):
        res = requests.get('https://news.ycombinator.com/news?p='+str(number+1))
        soup = BeautifulSoup(res.text, "html.parser")
        storylinks = soup.select('.storylink')
        subtexts = soup.select('.subtext')
        articles_databank.extend(create_custom_hn(storylinks, subtexts))
        if num_of_pages > number+1:  # Crawl-delay:30 requirement
            sleep(30)
    return sort_articles_by_points(articles_databank)


def sort_articles_by_points(articles_list):
    sorted_articles = sorted(articles_list, key=lambda a: a['points'], reverse=True)
    return sorted_articles


def create_custom_hn(storylinks, subtexts):
    filtered_articles = []
    for index, item in enumerate(storylinks):
        title = storylinks[index].getText()
        link = storylinks[index].get("href")
        scores = subtexts[index].select('.score')
        if scores:  # removing articles with no points
            points = int(sub(r'\spoints?', '', scores[0].getText()))
            if points >= min_points:
                filtered_articles.append({'title': title, 'link': link, 'points': points})
    return filtered_articles


pprint.pprint(get_hn_stories(num_of_pages))
