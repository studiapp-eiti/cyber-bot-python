from abc import ABC, abstractmethod

from interfaces import interface_creator
from interfaces import base_interface

class Scrapper(ABC):
    DEFAULT_FILE_REGEX = "([^\"]+\\.(pdf|png|jpg|jpeg|doc|docx|xls|xlsx|txt|java|zip|tar|rar|tar.gz))"

    @classmethod
    def get_auth_interface(cls, json, subject_id) -> [base_interface.AuthenticationInterface]:
        """
        :rtype .interfaces.base_interface.AuthenticationInterface or None on failure
        @param json:
        @param subject_id:
        """
        try:
            interface = interface_creator.InterfaceCreator.from_json(
                json, subject_id
            )
        except ValueError as e:
            print("VALUE_ERROR")
            print(e)
            return None
        return interface

    def iter_urls(self):
        for url in self.root_urls:
            responses = self.scrap_url(url)
            self.data[url["url"]] = responses


    @abstractmethod
    def scrap_url(self, url_obj):
        pass

