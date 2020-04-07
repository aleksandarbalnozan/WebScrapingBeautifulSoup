import requests
from bs4 import BeautifulSoup
import pprint
from sys import argv

response = requests.get(f'https://news.ycombinator.com/news?p={argv[0]}')
# create a beatifulsoup object with html from hackernews page
soup = BeautifulSoup(response.text, 'html.parser')
# perform a css selector by class
links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    # we sord dict by votes and reverse it from higher to lower
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hacker_news(links, subtext):
    # here we will store our information
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        # if vote score exist
        if len(vote):
            # since we get int and string combined, we have to substract string
            point = int(vote[0].getText().replace(' points', ''))
            # we want just popular articles
            if point > 99:
                hn.append({'title': title, 'href': href, 'votes': point})
    return sort_stories_by_votes(hn)


# just to make it more enjoyable for eyes
pprint.pprint(create_custom_hacker_news(links, subtext))
