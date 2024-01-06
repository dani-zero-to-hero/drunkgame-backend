"""
Semantic Excetions of the drunk game
"""


class DrunkException(Exception):
    pass


class UserError(DrunkException):
    pass


class BadInput(UserError):
    pass


class DeviceError(DrunkException):
    pass


class InvalidDraw(DeviceError):
    pass
