from django.contrib import admin

from .models import AttackCategory, SecurityEvent, DataIngestionLog, City, WeatherRecord

#Requirement: customize 1 model in Django Admin
@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('category', 'timestamp', 'severity', 'threat_score', 'source')
    list_filter = ('severity','source','category')
    search_fields = ('category__name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temperature_max', 'temperature_min', 'source')
    list_filter = ('city', 'date')

admin.site.register(AttackCategory)
admin.site.register(DataIngestionLog)



# Register your models here.
