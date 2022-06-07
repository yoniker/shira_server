from enum import Enum

class ERROR_CONSTS:
    class STATUS_ERROR(str, Enum):
        STATUS = 'status'
        ANOTHER_USER_LOGGED_IN = 'Not authorised - another user logged in'
        MISSING_DETAILS = 'error details are missing'
        OK = 'OK'
        SUCCESSFUL_LOGIN = 'successful login'
        USER_ALREADY_EXIST = 'User already exists'

