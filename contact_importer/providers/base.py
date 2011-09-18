###-*- coding: utf-8 -*-#################################
class BaseContacts(object):
    """
    Abstract class for contact importing
    """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
#        self.is_success = False
#        self.error_message = None

    def get_contacts(self):
        """
        Implements a generator for iterating in contacts
        """
        raise NotImplementedError()

    def get_contact_list(self):
        """
        Returns a contact list
        """
        return [c for c in self.get_contacts()]