from ..base.view import PostSimpleServiceAPI
from .services import resetPassword
    
class resetPasswordAPI(PostSimpleServiceAPI):
    def getService(self):
        return resetPassword;
        