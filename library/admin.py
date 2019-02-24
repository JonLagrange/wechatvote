from django.contrib import admin

# Register your models here.

from library.models import UserProfile, Mission, DoMission, MissionImage, DoMissionImage, MissionLock

admin.site.register(UserProfile)
admin.site.register(Mission)
admin.site.register(DoMission)
admin.site.register(MissionImage)
admin.site.register(DoMissionImage)
admin.site.register(MissionLock)
