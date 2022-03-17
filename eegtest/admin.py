from django.contrib import admin

from .models import StimuliCategory, Test, Stimulus, TestResult, Calculation, Parameter, \
    TestResultStimuli, TestParameterResult


admin.site.register(StimuliCategory)
admin.site.register(Test)
admin.site.register(Stimulus)
admin.site.register(TestResult)
admin.site.register(TestResultStimuli)
admin.site.register(Calculation)
admin.site.register(Parameter)
admin.site.register(TestParameterResult)