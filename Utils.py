from trackers import *


def get_tracker(tracker,config_section):
    if tracker == 'AnimeBytes':
        return AnimeBytes(config_section['SessionCookie'], config_section['ProfileLink'])
    elif tracker == 'TorrentLeech':
        return TorrentLeech(config_section['Username'], config_section['Password'], config_section['ProfileLink'])
    elif tracker == 'GazelleGames':
        return GazzelleGames(config_section['SessionCookie'], config_section['ProfileLink'])
