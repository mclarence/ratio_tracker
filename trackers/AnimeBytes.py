from collections import namedtuple

from trackers.Tracker import Tracker
import requests
from bs4 import BeautifulSoup as bs
import humanfriendly

class AnimeBytes(Tracker):
    def __init__(self, session_cookie, profilelink):
        self.session_cookie = session_cookie
        self.profilelink = profilelink

    def get_stats(self):
        req = requests.get(self.profilelink, cookies={'session': self.session_cookie}, headers=self.headers)
        soup = bs(req.content, features='html.parser')
        desc_list = soup.find_all('div', { 'class': 'userstatsright' })[0].find_all('dl', { 'class': 'userprofile_list clearcont' })[0].find_all('dd')

        count = 0
        for dd in desc_list:
            if count == 0:
                uploaded = humanfriendly.parse_size(dd.find_all('span')[0].text, binary=True)
            elif count == 1:
                downloaded = humanfriendly.parse_size(dd.find_all('span')[0].text, binary=True)
            elif count == 2:
                ratio = float(dd.find_all('span')[0].text)
            elif count == 3:
                break
            count = count + 1

        stats = namedtuple('Stats', ['ratio', 'download', 'upload'])
        stats.ratio = ratio
        stats.download = downloaded
        stats.upload = uploaded

        return stats


