from abc import ABC, abstractmethod



class AuthenticationInterface(ABC):


    @abstractmethod
    def append_GET_parameters(self, existing_parameters=None):
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


