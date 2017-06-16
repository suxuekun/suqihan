import os
from django.conf import settings
from ..utils.strings import genStr

def getFileSuffix(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension
    
def handleUploadSaveTempFile(request,renameLength = 8):
    csvfile = request.FILES['file'];
    if not csvfile:
        return None;
    suffix = getFileSuffix(csvfile.name)
    temp_file = settings.TEMP_ROOT + genStr(renameLength) + suffix;
    try:
        os.makedirs(os.path.dirname(temp_file))
    except:
        pass
    with open(temp_file, 'wb+') as destination:
        for chunk in csvfile.chunks():
            destination.write(chunk)
    return temp_file;

def deleteFile(filename):
    os.remove(filename)