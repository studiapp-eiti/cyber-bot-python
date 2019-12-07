from .studia_interface import Studia3Interface



class InterfaceCreator:
    INTERFACES = {"Studia3": Studia3Interface, "HttpAuth": None}

    @classmethod
    def determine_interface(cls, interface_name):
        try:
            return cls.INTERFACES[interface_name]
        except KeyError as e:
            raise ValueError(f"Provided not correct http_interface name ({interface_name})") from e

    @classmethod
    def from_name(cls, interface_name, subject_id, options=None):
        inter = cls.determine_interface(interface_name)
        print(inter)
        abb = inter(subject_id, options)
        print(abb)
        return abb