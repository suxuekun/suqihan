import calendar
import pytz
from dateutil import relativedelta
from datetime import date#datetime,timedelta,
from datetime import datetime, timedelta
from django.conf import settings

def diffDate(d1,d2):
    return relativedelta.relativedelta(d2,d1)

def diffYears(d1,d2):
    rd = relativedelta.relativedelta(d2,d1)
    return rd.years

def diffMonths(d1,d2):
    rd = relativedelta.relativedelta(d2,d1)
    return rd.years * 12 + rd.months

def diffDays(d1,d2):
    return (d2-d1).days

def diffDaysMonthly(d1,d2):
    rd = relativedelta.relativedelta(d2,d1)
    return rd.days

def diffMonthsYearly(d1,d2):
    rd = relativedelta.relativedelta(d2,d1)
    return rd.months

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return date(year,month,day)

def getServerTimezoneDatetime():
    result = datetime.now(pytz.timezone(settings.CELERY_TIMEZONE))
    return result;

def getServerTimeString(format_str = "%Y-%m-%d_%H-%M-%S"):
    return datetime.strftime(getServerTimezoneDatetime(),format_str)

if __name__ == "__main__":
#     d2 = datetime.now()
#     d2 = date(2017,2,28)
#     d1 = add_months(d2, -12)
    d1 = date(2017,1,31)
    d2 = add_months(d1,1)
    d3 = d1 + timedelta(10)

    print d1,d2,d3
    print diffYears(d1, d2)
    print diffMonths(d1, d2)
    print diffDays(d1, d2)
    print diffDate(d1,d2)
    print diffDaysMonthly(d1,d2)
