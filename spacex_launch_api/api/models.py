from django.db import models


from django.db.models.fields import DateTimeField
from _datetime import datetime
import time

class UCDateTimeField(DateTimeField):

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = datetime.datetime.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = getattr(model_instance, self.attname)
            if not isinstance(value, datetime):
                # assume that the value is a timestamp if it is not a datetime
                value = datetime.fromtimestamp(int(value))
                # an exception might be better than an assumption
                setattr(model_instance, self.attname, value)
            return super(UCDateTimeField, self).pre_save(model_instance, add)




class Norad(models.Model):
    norad_id = models.JSONField(blank=True, null=True)
    payload = models.ForeignKey('Payload', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.norad_id)

class Payload(models.Model):
    payload_id = models.CharField(max_length=100)
    rocket = models.ForeignKey('Rocket', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.payload_id


class Rocket(models.Model):
    rocket_id = models.CharField(max_length=100)

    def __str__(self):
        return self.rocket_id

class LaunchSite(models.Model):
    site_id = models.CharField(max_length=100)
    site_name = models.CharField(max_length=100)
    site_name_long = models.CharField(max_length=250)

    def __str__(self):
        return self.site_name

class Launch(models.Model):
    
    flight_number = models.PositiveIntegerField(default=0)
    mission_name = models.CharField(max_length=100, blank=True)
    launch_date_unix = models.FloatField(default=time.time, blank=True)
    launch_success = models.BooleanField()
    launch_site = models.ForeignKey('LaunchSite', on_delete=models.CASCADE, blank=True, null=True)
    rocket = models.ForeignKey('Rocket', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.mission_name







