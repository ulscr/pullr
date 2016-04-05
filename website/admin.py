from django.contrib import admin

from . import models

admin.site.register(models.Place)
admin.site.register(models.Performance)
admin.site.register(models.Footnote)
admin.site.register(models.RingingName)
admin.site.register(models.Ringer)
admin.site.register(models.RingerPerformance)
