from django.contrib import admin

from .models import StimuliCategory, Test, Stimulus, CortexSessionModel, TestResult


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimulus)
admin.site.register(CortexSessionModel)
admin.site.register(TestResult)