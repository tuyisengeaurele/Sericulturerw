from django.contrib import admin
from .models import *
admin.site.register(Farm)
admin.site.register(IoTDevice)
admin.site.register(SilkwormBatch)
admin.site.register(Production)
admin.site.register(Course)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(User)
admin.site.register(PestOrDisease)
admin.site.register(Staff)
admin.site.register(WeatherMonitoring)

@admin.register(GrowthStage)
class GrowthStageAdmin(admin.ModelAdmin):
    list_display = ('silkworm_batch', 'stage', 'start_date', 'end_date', 'observations')

@admin.register(FeedingSchedule)
class FeedingScheduleAdmin(admin.ModelAdmin):
    list_display = ('silkworm_batch', 'feed_date', 'feed_time', 'feed_quantity', 'feed_type', 'remarks')    

