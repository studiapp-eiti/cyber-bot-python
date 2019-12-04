from abc import ABC, abstractmethod
from scrapper import generic_scrapper, apache_scrapper


class Scrapper(ABC):

    @classmethod
    def from_json(cls, data: dict, subject_id):
        s_type = data["type"]
        caller_names = data["implements"]
        root_urls = data["root_urls"]
        request_interfaces = None  # Todo: add proper function

        scrapper_class = cls.determine_scrapper(s_type)
        return scrapper_class(subject_id, request_interfaces, root_urls)

    @staticmethod
    def determine_scrapper(scrapper_name):
        """
        :type scrapper_name: str
        :rtype: Scrapper
        """
        if scrapper_name == "GenericScrapper":
            return generic_scrapper.GenericScrapper
        elif scrapper_name == "ApacheIndexesScrapper":
            return apache_scrapper.ApacheIndexesScrapper
        raise ValueError(f"Scrapper with name: {scrapper_name} not found! Please provide correct scrapper name!")
