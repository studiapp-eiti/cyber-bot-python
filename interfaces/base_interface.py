from abc import ABC, abstractmethod
from . import studia_interface


class HttpInterface:
    INTERFACES = {"Studia3": studia_interface.Studia3Interface, "HttpAuth": None}

    @abstractmethod
    def supported_subjects(self):
        """
        This function should return list of supported subjects, and should be called in the constructor.

        :rtype: list(int)
        """
        pass

    @abstractmethod
    def get_contents(self, url, timeout=5):
        """
        :type url: str
        :rtype: requests.response
        """
        pass

    def get_scrapping_data(self, url, timeout=5):
        """
        :type url: str
        :type timeout: int
        :rtype str (requests.response.text)
        """
        pass

    def subject_supported(self, s_id):
        """
        This function checks if subject is supported. Should be called in constructor of child class.
        :type s_id: int
        """
        pass

    @classmethod
    def determine_interface(cls, interface_name):
        try:
            return cls.INTERFACES[interface_name]
        except KeyError as e:
            raise ValueError(f"Provided not correct http_interface name ({interface_name})") from e

    @classmethod
    def create_interface(cls, interface_name, subject_id, queries):
        interface = cls.determine_interface(interface_name)
        return interface({"subject_id": subject_id, "queries": queries})


