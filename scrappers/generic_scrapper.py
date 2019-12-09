import html
import re

import requests
import os
from scrappers.base_scrapper import Scrapper


class GenericScrapper(Scrapper):
    TIMEOUT = 5

    #TODO Add support for include regex and exclude regex
    def __init__(self, subject_id, root_urls, *args, **kwargs):
        self.subject_id = subject_id
        self.root_urls = root_urls
        self.data = dict()

    def iter_urls(self):
        for url in self.root_urls:
            htmls = self.request_data(url)
            data = self.scrap_url(htmls)
            self.data[url["url"]] = data

    def scrap_url(self, html_data):
        data = dict()
        for url in html_data:
            matches = re.findall('"' + Scrapper.DEFAULT_FILE_REGEX + '"', html_data[url], re.IGNORECASE)
            data[url[1]] = [html.unescape(x[0]) for x in matches]
        return data

    def request_data(self, url_obj):
        base_url = url_obj["url"]
        request_parameters = {"timeout": self.TIMEOUT}
        responses = dict()

        if "interface" in url_obj:
            interface = url_obj["interface"]
            if len(interface) != 0:
                i = self.get_auth_interface(interface["name"], self.subject_id)
                i.append_GET_parameters(request_parameters)

        for path_obj in url_obj["sub_paths"]:
            parameters = request_parameters.copy()
            result = requests.get(base_url + path_obj["path"], **parameters)
            responses[(path_obj["path"], path_obj["name"])] = result.text
        return responses
