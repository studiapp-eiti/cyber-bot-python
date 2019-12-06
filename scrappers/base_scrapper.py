from abc import ABC, abstractmethod

from interfaces import interface_creator


class Scrapper(ABC):

    @classmethod
    def get_auth_interface(cls, name, subject_id, options = None):
        """

        :type name: str
        :rtype .interfaces.base_interface.AuthenticationInterface or None on failure
        """
        try:
            interface = interface_creator.InterfaceCreator.from_name(name, subject_id, options)
        except ValueError as e:
            print("VALUE_ERROR")
            print(e)
            return None
        return interface

    @abstractmethod
    def iter_urls(self):
        pass


    @abstractmethod
    def scrap_url(self, url_obj):
        pass

