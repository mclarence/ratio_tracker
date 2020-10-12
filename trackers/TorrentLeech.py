from trackers.Tracker import Tracker
import requests
from bs4 import BeautifulSoup as bs
from collections import namedtuple
import humanfriendly


class TorrentLeech(Tracker):
    def __init__(self, username, password, profilelink):
        self.username = username
        self.password = password
        self.profilelink = profilelink

    def get_stats(self):
        # Login to tracker to obtain cookies.
        session = requests.Session()
        session_res = session.post("https://www.torrentleech.org/user/account/login/",
                                   data={'username': self.username, 'password': self.password}, headers=self.headers)
        cookies = session_res.cookies.get_dict()

        # Get profile page
        req = requests.get(self.profilelink, cookies=cookies,
                           headers=self.headers)

        soup = bs(req.content, features='html.parser')

        ratio = float(soup.find_all('span', {'class': 'profile-info-details profile-ratio-details'})[0].text)
        uploaded = humanfriendly.parse_size(
            soup.find_all('span', {'class': 'profile-info-details profile-uploaded-details'})[0].text, binary=True)
        downloaded = humanfriendly.parse_size(
            soup.find_all('div', {'class': 'profile-downloaded'})[0].find_all('span', {
                'class': 'profile-info-details'})[0].text, binary=True)

        stats = namedtuple('Stats', ['ratio', 'download', 'upload'])
        stats.ratio = ratio
        stats.download = downloaded
        stats.upload = uploaded

        return stats
