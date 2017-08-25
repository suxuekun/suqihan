from suqihan.base.viewset import BaseViewSet
from suqihan.test.models import ItemWithCalenderEvent, CalendarEvent
from suqihan.test.serializer import ItemSerializer
from suqihan.models.baseSerializer import getDefaultSerializer

class CalendarEventViewSet(BaseViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = getDefaultSerializer(CalendarEvent)

class ItemViewSet(BaseViewSet):
    queryset = ItemWithCalenderEvent.objects.prefetch_related('events')
    serializer_class = ItemSerializer