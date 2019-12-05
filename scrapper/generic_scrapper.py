from scrapper.scrapper import Scrapper

class GenericScrapper(Scrapper):
    def __init__(self, subject_id, root_urls, *args, **kwargs):
        self.subject_id = subject_id
        self.root_urls = root_urls