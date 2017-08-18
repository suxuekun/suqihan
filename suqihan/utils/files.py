import os
from django.conf import settings
import datetime
def move(src,dest):
    try:
        os.makedirs(os.path.dirname(dest))
    except:
        pass
    os.rename(src,dest)
    
def moveModelFile(modelfile,dest):
    move(modelfile.path,dest)
    
def getFilePathNameSuffix(filename):
    pathParts = filename.split(os.sep)
    p = pathParts.pop();
    nameParts = p.split(".");
    
    if len(nameParts)>1:
        suffix = nameParts.pop();
        name = ".".join(nameParts)
    else:
        suffix = ""
        name = nameParts[0]
        
    if len(pathParts) > 0:
        path = os.path.join(*pathParts)
    else:
        path = ""
    return path,name,suffix;
    
def getTrashPath(modelfileName):
    p,n,s = getFilePathNameSuffix(modelfileName);
    trash = settings.TRASH_ROOT
    today = datetime.datetime.today()
    today_date_str = today.strftime('%Y-%m-%d');
    today_time_str = today.strftime('%H-%M-%S');
    trash_today = trash + today_date_str + os.sep
    
    trash_file_name = n+"."+today_time_str+"."+s;
    
    trash_paths = [trash_today,p,trash_file_name]
    trash_file = os.path.join(*trash_paths);
    return trash_file

def moveModelFileToTrash(modelfile):
    trash_file = getTrashPath(modelfile.name)
    moveModelFile(modelfile, trash_file)