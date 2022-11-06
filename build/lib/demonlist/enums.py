from enum import Enum, IntEnum


class CountryListType(Enum):
    """
    Enumeration of country list types.
    """
    main = "main"
    "This type shows only basic information."
    advanced = "advanced"
    "This type shows advanced information."


class DemonListType(Enum):
    """
    Enumeration of demon list types.
    """
    main = "main"
    "Demons standing 1-150."
    beyond = "advanced"
    "Demons out of the top 150."
    future = "future"
    "A list of demons that may be passed in the future."


class JsonStatus(Enum):
    ok = "ok"


class RequestsAction(Enum):
    """
    Enumeration of request actions.
    """
    confirm = "request_accept"
    "Accept the request."
    reject = "request_reject"
    "Reject the request."
    delete = "request_delete"
    "Delete the request."


class Badge(Enum):
    """
    Enumeration of user badges.
    """
    PC = "P"
    "PC Player."
    Mobile = "M"
    "Mobile Player."
    Low_FPS = "L"
    "Low FPS Player."
    PC_Mobile = "PM"
    "PC/Mobile Player."
    PC_Low_FPS = "PL"
    "PC Low FPS Player."
    Former_Cheater = "C"
    "Former_Cheater."


Role = Enum(value="Role",
            names='User Moderator Editor Exposer Owner FutureListEditor ExposerEditor Coder ExposerModerator '
                  'ElderModerator', start=0)
