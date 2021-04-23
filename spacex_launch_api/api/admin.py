from django.contrib import admin
from .models import *
class LaunchAdmin(admin.ModelAdmin):
    fields = ('flight_number','mission_name', 'launch_date_unix', 'launch_success', 'rocket', 'launch_site')
class RocketAdmin(admin.ModelAdmin):
    fields = ('rocket_id', 'payloads')

class LaunchSiteAdmin(admin.ModelAdmin):
    fields = ['site_id', 'site_name', 'site_name_long']

class PayloadAdmin(admin.ModelAdmin):
    fields = ('payload_id', 'norad_id')

class NoradAdmin(admin.ModelAdmin):
    fields = ('norad_id',)

admin.site.register(Launch, LaunchAdmin)
admin.site.register(Rocket, RocketAdmin)
admin.site.register(LaunchSite, LaunchSiteAdmin)
admin.site.register(Payload, PayloadAdmin)
admin.site.register(Norad, NoradAdmin)