"""
Custom exceptions.
"""


class WrongCredentials(Exception):
    """
    Raised if the user entered the wrong data to login.
    """
    pass


class NotLoggedIn(Exception):
    """
    Raised if the user is not logged into the account.
    """
    pass
