from django.contrib import admin

from .models import AttackCategory, SecurityEvent, DataIngestionLog

#Requirement: customize 1 model in Django Admin
@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('category', 'timestamp', 'severity', 'threat_score', 'source')
    list_filter = ('severity','source','category')
    search_fields = ('category__name',)

admin.site.register(AttackCategory)
admin.site.register(DataIngestionLog)



# Register your models here.
