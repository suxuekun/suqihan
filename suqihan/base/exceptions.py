from rest_framework import status
from rest_framework.exceptions import APIException

from suqihan import utils
from suqihan.base import error_code
from suqihan.base.response import GeneralResponseWrapper


class BaseAPIException(APIException):
    def toJson(self):
        return utils.toJSON(self.__str__())
    
class GeneralError(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = GeneralResponseWrapper(code=error_code.ERROR).__dict__
    default_code = 'error'
    
class NotAuth(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = GeneralResponseWrapper(code=error_code.NOT_LOGIN_IN).__dict__
    default_code = 'not login'

class AuthFail(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = GeneralResponseWrapper(code=error_code.LOGIN_FAIL).__dict__
    default_code = 'login fail'