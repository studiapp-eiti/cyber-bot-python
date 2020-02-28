import html
import re

import requests
import os
from scrappers.base_scrapper import Scrapper


class GenericScrapper(Scrapper):
    TIMEOUT = 5

    # TODO Add support for include regex and exclude regex
    def __init__(self, subject_id, scrapper_data, *args, **kwargs):
        super().__init__(scrapper_data, subject_id)
        self.subject_id = subject_id
        self.scrapped_data = dict()

    def iter_urls(self):
        root_url = self.scrapper_data["root_url"]
        for url_name, url in self.scrapper_data["sub_urls"].keys():
            raw_html = self.request_data(root_url + url)
            self.scrapped_data[url_name] = self.scrap_url(raw_html)

    def scrap_url(self, html_data):
        matches = re.findall('"' + Scrapper.DEFAULT_FILE_REGEX + '"', html_data, re.IGNORECASE)
        data = [html.unescape(x) for x in matches]
        return data

    def request_data(self, url):
        request_parameters = {"timeout": self.TIMEOUT}
        for interface in self.interfaces:
            request_parameters = interface.append_GET_parameters(request_parameters)

        response = requests.get(url, **request_parameters)
        if response.status_code != 200:
            raise ConnectionError("Unable to connect: " + str(response.status_code))
        return response.text
