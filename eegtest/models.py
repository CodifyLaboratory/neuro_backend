from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models

from user.models import User


class Test(models.Model):
    title = models.CharField(max_length=250, unique=True, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    status = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title


class StimuliCategory(models.Model):
    title = models.CharField(max_length=250, verbose_name='Stimulus category', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimulus category'
        verbose_name_plural = 'Stimulus categories'

    def __str__(self):
        return self.title


class Stimulus(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test', related_name='stimulus',
                             blank=True, null=True)
    category = models.ForeignKey(StimuliCategory, on_delete=models.CASCADE, verbose_name='Category',
                                 blank=True, null=True)
    title = models.CharField(max_length=250, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    duration = models.DurationField(verbose_name='Duration', blank=True, null=True)
    file = models.FileField(verbose_name='File', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimuli'
        verbose_name_plural = 'Stimulus'

    def __str__(self):
        return self.title

    def get_str_id(self):
        return str(self.pk)


class Parameter(models.Model):
    title = models.CharField(max_length=250, verbose_name='Parameter', blank=True, null=True)

    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'

    def __str__(self):
        return self.title


class Operation(models.Model):
    title = models.CharField(max_length=250, verbose_name='Operation', blank=True, null=True)

    class Meta:
        verbose_name = 'Operation'
        verbose_name_plural = 'Operations'

    def __str__(self):
        return self.title


class Calculation(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, verbose_name='Test',
                                related_name='calculations', blank=True, null=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Parameter',
                                  related_name='calculations', blank=True, null=True)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name='Operation',
                                  related_name='calculations', blank=True, null=True)

    class Meta:
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'

    def __str__(self):
        return '{}'.format(self.test)


class StimuliGroup(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE, verbose_name='Calculation',
                                    related_name='stimuli_groups', blank=True, null=True)
    stimuli = models.ManyToManyField(Stimulus, verbose_name='Stimulus', related_name='stimuli_groups')

    class Meta:
        verbose_name = 'Stimuli Groups'
        verbose_name_plural = 'Stimuli Groups'

    def __str__(self):
        return '{}'.format(self.calculation)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True, related_name='results')
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Test', related_name='results')
    title = models.CharField(max_length=250, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    file = models.FileField(verbose_name='File', blank=True, null=True)
    date = models.DateField(verbose_name='Date of creation', default=date.today)
    status = models.BooleanField(verbose_name='Status', default=False)
    value = models.FloatField(verbose_name='Value of Calculation')

    class Meta:
        verbose_name = 'Test result'
        verbose_name_plural = 'Test results'

    def __str__(self):
        return '{}'.format(self.user)


class TestResultStimuli(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, verbose_name='Test Result',
                                    related_name='test_results_stimulus', blank=True, null=True)
    stimuli = models.ForeignKey(Stimulus, on_delete=models.CASCADE, verbose_name='Stimulus',
                                related_name='test_results_stimulus')
    pow = ArrayField(models.FloatField(), default=list)

    class Meta:
        verbose_name = 'Test Result Stimulus'
        verbose_name_plural = 'Test Result Stimulus'

    def __str__(self):
        return '{}'.format(self.test_result)