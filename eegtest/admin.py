from django.contrib import admin

from .models import StimuliCategory, Test, Stimulus


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimulus)