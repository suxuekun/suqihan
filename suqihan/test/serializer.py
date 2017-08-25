from suqihan.test.models import ItemWithCalenderEvent, CalendarEvent
from suqihan.models.baseSerializer import getDefaultSerializer, BaseSerializer
from rest_framework import serializers
from _functools import partial

BaseCalendarEventSerializer = getDefaultSerializer(CalendarEvent);
class CalendarEventSerializer(BaseCalendarEventSerializer):
    class Meta(BaseCalendarEventSerializer.Meta):
        fields = None
        exclude = ('event_target_type','event_target_id')

class WithCalendarEventSerializerMixin(BaseSerializer):
    event = CalendarEventSerializer()
    def create(self, validated_data):
        event_data = validated_data.pop('event')
        instance = super(WithCalendarEventSerializerMixin,self).create(validated_data)
        instance.events.create(**event_data)
        return instance
    
    def update(self, instance, validated_data):
        event_data = validated_data.pop('event')     
        instance = super(WithCalendarEventSerializerMixin,self).update(instance, validated_data)
        serializer = CalendarEventSerializer(instance.event,data=event_data,partial=True)
        serializer.is_valid()
        serializer.save()
#         instance.event
        return instance



class ItemSerializer(getDefaultSerializer(ItemWithCalenderEvent),WithCalendarEventSerializerMixin):
    
    pass