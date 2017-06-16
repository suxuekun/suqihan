import json
import datetime
import decimal
from django import template
from . import date,strings,csvUtil


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield strings(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (strings(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
    
def datetime_json_encoder(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    return None

def date_json_encoder(x):
    if isinstance(x, datetime.date):
        return x.isoformat()
    return None

def time_json_encoder(x):
    if isinstance(x, datetime.time):
        return x.isoformat()
    return None

def decimal_json_encoder(x):
    if isinstance(x, decimal.Decimal):
        value = str(x)
        return value
    return None

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, datetime.date):
        return x.isoformat()
    if isinstance(x, datetime.time):
        return x.isoformat()
    raise TypeError("Unknown type")

def combined_json_encoder(x):
    encoders = [datetime_json_encoder,date_json_encoder,time_json_encoder,decimal_json_encoder]
    encoders_length = len(encoders)
    i = 0;
    while i < encoders_length:
        
        current_encoder = encoders[i]
        i +=1
        res = current_encoder(x)
        if res != None:
            return res
    return 'unknown'



def toStruct(anyModel,fields = None):
    if fields ==None:
        fields = [f.name for f in anyModel._meta.fields];
    struct = dict([(attr, getattr(anyModel, attr)) for attr in fields])
    return struct

def toJSON(obj):
    return json.dumps(obj,default = combined_json_encoder);

def valid_struct(modelclass,struct):
    anymodel = modelclass._meta.concrete_model;
    fields = [f.name for f in anymodel._meta.fields];
    not_valid = []
    for attr in struct:
        if (attr not in fields):
            not_valid.append(attr)
#             del struct[attr]
    for attr in not_valid:
        del struct[attr];
    return struct;

def createFrom(modelInstance,newInstance=None):
    if newInstance == None:
        newInstance = modelInstance.__class__();
    newInstance.fromStruct(valid_struct(modelInstance.__class__, modelInstance.toStruct()))
    newInstance.id = None
    newInstance.pk = None
    return newInstance

def fromStruct(anyModel,struct,fields=None):
    if fields ==None:
        fields = [f.name for f in anyModel._meta.fields];
    for attr in fields:
        if struct.has_key(attr): 
            if struct[attr] != None:
                setattr(anyModel,attr,struct[attr])
            elif hasattr(anyModel, attr) and getattr(anyModel,attr) != None:
                setattr(anyModel,attr,struct[attr])
            else:
                pass
    return struct;

def fromJSON(anyModel,jsonStr,fields = None):
    struct = json.loads(jsonStr)
    fromStruct(anyModel, struct, fields)
    return struct;

def template_exists(value):
    try:
        template.loader.get_template(value)
        return True
    except template.TemplateDoesNotExist:
        return False
    
def getListItemByIndexOrDefault(arr,index,default=None):
    try:
        return arr[index]
    except IndexError:
        return default
        