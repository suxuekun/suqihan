from StringIO import StringIO
import csv

from django.http.response import HttpResponse
from xlwt import Workbook

from strings import getDecentAttrSilent


def recordLine(line):
    return line;

def readCSVMakeIndex(filename,key_index=None,value_index=None):
    with open(filename, 'rU') as csvfile:
        csv_reader = csv.reader(csvfile)
        success =0;
        fail = 0;
        total = sum(1 for _ in csv_reader)
        csvfile.seek(0)
        res={
            'total':total,
            'result':{}
        }
        idx = 0;
        for line in csv_reader:
            try:
                if key_index != None:
                    key = line[key_index]
                else:
                    key = idx
                if value_index != None:
                    value = line[value_index]
                else:
                    value = line;
                success+=1;
            except Exception as _:
                print _
                fail +=1;
            res['result'][key] = value;
            idx +=1;
        res['success'] = success;
        res['fail'] = fail;
    return res;
    
def readCSVForEachRow(filename,func,*args,**kwargs):
    with open(filename, 'rU') as csvfile:
        csv_reader = csv.reader(csvfile)
        success =0;
        fail = 0;
        total = sum(1 for _ in csv_reader)
        csvfile.seek(0)
        res={
            'total':total,
            'result':[]
        }
        for line in csv_reader:
            try:
                item = func(line,*args,**kwargs);
                success+=1;
            except Exception as _:
                print _
                item = [_,line]
                fail +=1;
            res['result'].append(item)
        res['success'] = success;
        res['fail'] = fail;
    return res;

def writeCSVLines(filename,lines):
    with open(filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for line in lines:
            spamwriter.writerow(line)
            
    return filename;

def wb_download(wb,name):
    f = StringIO()
    wb.save(f)
    f.seek(0)
    response = HttpResponse(f.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % name;
    return response

def export_xls(queryset,fields):
    """
    Generic xls export admin action.
    fields = [{
        header:header,
        name:field_name,
    },{
    ...
    }
    ]
    """
    
    wb = Workbook()
    ws0 = wb.add_sheet('0')
    col = 0
    field_names = []
    # write header row
    for field in fields:
        ws0.write(0, col, field.get('header'))
        field_names.append(field.get('name'))
        col = col + 1
    
    row = 1
    # Write data rows
    for obj in queryset.all():
        col = 0
        for field in field_names:
            val = unicode(getDecentAttrSilent(obj,field)).strip()
            ws0.write(row, col, val)
            col = col + 1
        row = row + 1    

    return wb

def export_model_xls(queryset,model):
    """
    Generic xls export admin action.
    """
    opts = model._meta
    
    wb = Workbook()
    ws0 = wb.add_sheet('0')
    col = 0
    field_names = []
    # write header row
    for field in opts.fields:
        ws0.write(0, col, field.name)
        field_names.append(field.name)
        col = col + 1
    
    row = 1
    # Write data rows
    for obj in queryset:
        col = 0
        for field in field_names:
            val = unicode(getattr(obj, field)).strip()
            ws0.write(row, col, val)
            col = col + 1
        row = row + 1    

    return wb;
        
            
            