from .http_auth_interface import HttpAuthInterface
from .studia_interface import Studia3Interface
from .base_interface import AuthenticationInterface


class InterfaceCreator:
    INTERFACES = {"Studia3": Studia3Interface,
                  "HttpAuth": HttpAuthInterface}

    @classmethod
    def determine_interface(cls, interface_name):
        try:
            return cls.INTERFACES[interface_name]
        except KeyError as e:
            raise ValueError(f"Provided incorrect http_interface name ({interface_name})") from e

    @classmethod
    def from_json(cls, json, subject_id) -> AuthenticationInterface:
        inter = cls.determine_interface(json["name"])
        return inter(subject_id, json["options"])