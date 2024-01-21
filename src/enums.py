from enum import Enum

class Method(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    PATCH = 4

class UserType(Enum):
    JUNIOR = 0
    MEDIOR = 1
    SENIOR = 2
    DEFAULT = 3