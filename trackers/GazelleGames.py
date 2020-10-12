from trackers.Tracker import Tracker
import requests
from bs4 import BeautifulSoup as bs
from collections import namedtuple
import humanfriendly


class GazzelleGames(Tracker):
    def __init__(self, session_cookie, profilelink):
        self.session_cookie = session_cookie
        self.profilelink = profilelink

    def get_stats(self):
        req = requests.get(self.profilelink, cookies={'session': self.session_cookie}, headers=self.headers)
        soup = bs(req.content, features='html.parser')
        user_stats = soup.find_all('ul', { 'id' : 'user_stats'})[0]
        ratio = float(user_stats.find_all('li', { 'id' : 'ratio' })[0].find_all('span', { 'class': 'stat tooltip' })[0].text)
        uploaded = humanfriendly.parse_size(user_stats.find_all('li', {'id': 'upload'})[0].find_all('span', {'class': 'stat tooltip'})[0].text, binary=True)
        downloaded = humanfriendly.parse_size(user_stats.find_all('li', {'id': 'download'})[0].find_all('span', {'class': 'stat tooltip'})[0].text, binary=True)

        stats = namedtuple('Stats', ['ratio', 'download', 'upload'])
        stats.ratio = ratio
        stats.download = downloaded
        stats.upload = uploaded

        return stats

