from abc import ABC, abstractmethod

from interfaces import interface_creator
from interfaces import base_interface


class Scrapper(ABC):
    def __init__(self, scrapper_data, subject_id):
        self.scrapper_data = scrapper_data
        self.subject_id = subject_id
        self.interfaces = list()

    DEFAULT_FILE_REGEX = "([^\"]+\\.(pdf|png|jpg|jpeg|doc|docx|xls|xlsx|txt|java|zip|tar|rar|tar.gz))"

    @classmethod
    def get_auth_interface(cls, subject_id, interface_data) -> [base_interface.AuthenticationInterface]:
        """
        :rtype .interfaces.base_interface.AuthenticationInterface or None on failure
        @param subject_id:
        """
        try:
            interface = interface_creator.InterfaceCreator.from_json(
                subject_id, interface_data)
        except ValueError as e:
            print("VALUE_ERROR")
            print(e)
            return None
        return interface

    def get_interfaces(self):
        for interface in self.scrapper_data["interfaces"]:
            self.interfaces.append(self.get_auth_interface(self.subject_id, interface))



    def iter_urls(self):
        for url in self.root_urls:
            responses = self.scrap_url(url)
            self.data[url["url"]] = responses

    @abstractmethod
    def scrap_url(self, url_obj):
        pass
