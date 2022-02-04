from django.contrib import admin

from .models import StimuliCategory, Test, Stimulus, TestResult, Calculation, StimuliGroup, Parameter, Operation, \
    TestResultStimuli


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimulus)
admin.site.register(TestResult)
admin.site.register(TestResultStimuli)
admin.site.register(Calculation)
admin.site.register(StimuliGroup)
admin.site.register(Parameter)
admin.site.register(Operation)