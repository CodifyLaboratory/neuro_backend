from django.contrib import admin

from .models import StimuliCategory, Test, Stimulus, CortexSessionModel, TestResult, CortexObjectModel, Calculation, StimuliGroup, Parameter


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimulus)
admin.site.register(CortexSessionModel)
admin.site.register(TestResult)
admin.site.register(CortexObjectModel)
admin.site.register(Calculation)
admin.site.register(StimuliGroup)
admin.site.register(Parameter)