import requests
import os
from scrappers.base_scrapper import Scrapper


class GenericScrapper(Scrapper):
    TIMEOUT = 5

    def __init__(self, subject_id, root_urls, *args, **kwargs):
        self.subject_id = subject_id
        self.root_urls = root_urls
        self.data = dict()

    def iter_urls(self):
        for url in self.root_urls:
            responses = self.scrap_url(url)
            self.data[url["url"]] = responses

    def scrap_url(self, url_obj):
        base_url = url_obj["url"]
        request_parameters = {"timeout": self.TIMEOUT}
        interface = url_obj["interface"]
        responses = dict()

        if len(interface) != 0:
            i = self.get_auth_interface(interface["name"], self.subject_id)
            i.append_GET_parameters(request_parameters)

        for path_obj in url_obj["sub_paths"]:
            parameters = request_parameters.copy()
            result = requests.get(base_url + path_obj["path"], **parameters)
            responses[(path_obj["path"], path_obj["name"])] = result.text
        return responses
