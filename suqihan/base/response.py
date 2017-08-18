from suqihan import utils


class GeneralResponseWrapper(object):
    def __init__(self,code = 0 ,result = {}):
        self.code=code
        self.result=result
    def toJSON(self):
        return utils.toJSON(self.__dict__);