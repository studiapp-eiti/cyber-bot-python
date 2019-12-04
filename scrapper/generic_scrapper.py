from scrapper.scrapper import Scrapper

class GenericScrapper(Scrapper):
    def __init__(self, subject_id, req_interfaces, root_urls, *args, **kwargs):
        self.request_interface = req_interfaces
        self.root_urls = root_urls