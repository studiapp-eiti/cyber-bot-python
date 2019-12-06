from abc import ABC, abstractmethod
from . import studia_interface


class AuthenticationInterface:
    INTERFACES = {"Studia3": studia_interface.Studia3Interface, "HttpAuth": None}

    @abstractmethod
    def get_request_parameters(self, existing_parameters=None):
        """

        :rtype: dict(request_parameters)
        """
        pass

    @abstractmethod
    def supported_subjects(self):
        """
        This function should return object containing supported subjects, and should be called in the constructor.
        It can be dictionary or list, depending on situation.
        """
        pass

    def subject_supported(self, s_id):
        """
        This function checks if subject is supported. Should be called in constructor of child class.
        If subject is not supported it should throw ValueError.
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
    def from_name(cls, interface_name, subject_id, options=None):
        interface = cls.determine_interface(interface_name)
        return interface({"subject_id": subject_id, "options": options})
