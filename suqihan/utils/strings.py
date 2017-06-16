import string
import random
import re

def genStr(size,scope=None):
    scope = scope or string.ascii_letters + string.digits
    initial = ''
    result = initial.join(random.SystemRandom().choice(scope) for _ in range(size))
    return result

class PartialFormatter(string.Formatter):
    def __init__(self, missing='~', bad_fmt='(!!)'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val=None,field_name 
        return val 

    def format_field(self, value, spec):
        # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt   
            else: raise
            
def getDecentAttr(obj,key=None,error="(!!)"):
    try:
        if key == None:
            return None;
        arr = key.split(".");
        arr.reverse();
        while(len(arr) and (obj != None)):
            attr_name = arr.pop()
            obj= obj[attr_name]
        if obj == None:
            return error
        return obj;
    except Exception as _:
        return error

def multiReplace(template,resources,missing="",badvalue=""):
    result = template
    a = re.findall(r'\{.[^\{\}]*\}', template)
    for key in a:
        rep = key[1:-1]
        attr = getDecentAttr(resources,rep,missing)
        try:
            attr = attr.__str__()
            result = re.sub(key,attr,result)
        except Exception as e :
            print e
            result = re.sub(key,badvalue,result)
    return result

def getDecentAttrSilent(obj,key=None,error=None):
    try:
        if key == None:
            return None;
        arr = key.split(".");
        arr.reverse();
        while(len(arr) and (obj != None)):
            attr_name = arr.pop()
            obj= getattr(obj, attr_name)
        if obj == None:
            return error
        return obj;
    except Exception as _:
        return error
            
default_formatter = PartialFormatter()

if __name__ == "__main__":
    print genStr(10);
    test = "dear {customer.name} , your Policy {policy.number} {notexist} balabala"

    resources = {
        'name':'name',
        'customer':{
            'name':"suxuekun"
        },
        'policy':{
            'number':1000
        }
        
    }
#     a = default_formatter.format(test,**resources)
    b = multiReplace(test, resources, badvalue="(!!)")
    print b;
    