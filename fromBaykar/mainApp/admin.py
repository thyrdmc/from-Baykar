from django.contrib import admin

from .models import *

class MailLogsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

class VehicleAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'created_by',)

admin.site.register(MailLogs, MailLogsAdmin)
admin.site.register(Vehicle, VehicleAdmin)

