from abc import ABC, abstractmethod

import interfaces
import scrappers.child_scrappersgeneric_scrapper


class Scrapper(ABC):
    SCRAPPERS = {"GenericScrapper": generic_scrapper.GenericScrapper,
                 "ApacheIndexesScrapper": apache_scrapper.ApacheIndexesScrapper}

    @classmethod
    def from_json(cls, data: dict, subject_id):
        s_type = data["type"]
        root_urls = data["root_urls"]
        scrapper_class = cls.determine_scrapper(s_type)
        return scrapper_class(subject_id, root_urls)

    @classmethod
    def determine_scrapper(cls, scrapper_name):
        try:
            return cls.SCRAPPERS[scrapper_name]
        except KeyError as e:
            raise ValueError("Provided not correct scrappers name") from e

    @classmethod
    def get_auth_interface(cls, name, subject_id, options = None):
        """

        :type name: str
        :rtype .interfaces.base_interface.AuthenticationInterface or None on failure
        """
        try:
            interface = interfaces.base_interface.AuthenticationInterface.from_name(name, subject_id, options)
        except ValueError as e:
            # todo: add logging here
            return None
        return interface

    @abstractmethod
    def iter_urls(self):
        pass


    @abstractmethod
    def scrap_url(self, url_obj):
        pass

