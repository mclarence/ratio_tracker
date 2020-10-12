from abc import ABC, abstractmethod


class Tracker(ABC):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    @abstractmethod
    def get_stats(self):
        pass
