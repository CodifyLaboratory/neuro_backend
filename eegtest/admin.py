from django.contrib import admin

from .models import StimuliCategory, Test, Stimuli


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimuli)