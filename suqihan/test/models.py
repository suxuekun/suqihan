from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
class BaseCalendar(models.Model):
    allDay = models.BooleanField(default=False)
    start = models.DateTimeField(default=datetime.now,null=True,blank=True)
    end = models.DateTimeField(default=datetime.now,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    url = models.CharField(max_length=255,null=True,blank=True)
    className = models.CharField(max_length=255,null=True,blank=True);
    color = models.CharField(max_length=255,null=True,blank=True);
    class Meta:
        abstract = True
        
class CalendarEvent(BaseCalendar):
    event_target_type = models.ForeignKey(ContentType,null=True,blank=True,default=None)
    event_target_id = models.PositiveIntegerField(null=True,blank=True,default=None)
    event_target_obj = GenericForeignKey('event_target_type','event_target_id')
    
    class Meta:
        unique_together = ('event_target_type','event_target_id')

class CalendarEventableMixin(models.Model):
    events = GenericRelation(CalendarEvent,object_id_field='event_target_id',content_type_field='event_target_type')
    @property
    def event(self):
        return self.events.get()
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        return super(CalendarEventableMixin,self).save(*args, **kwargs)
    
class ItemWithCalenderEvent(CalendarEventableMixin):
    name = models.CharField(max_length=100,null=True,blank=True)