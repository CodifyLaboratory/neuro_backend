from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Sum
from user.models import User
from scipy import signal
import numpy as np


class Test(models.Model):
    """ Test model """
    title = models.CharField(max_length=250, unique=True, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    status = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title


class StimuliCategory(models.Model):
    """ Stimuli Category Model """
    title = models.CharField(max_length=250, verbose_name='Stimulus category', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimulus category'
        verbose_name_plural = 'Stimulus categories'

    def __str__(self):
        return self.title


class Stimulus(models.Model):
    """ Stimuli of the test Model """
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
    """ Parameter of the calculation Model """
    title = models.CharField(max_length=250, verbose_name='Parameter', blank=True, null=True)

    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'

    def __str__(self):
        return self.title


class Calculation(models.Model):
    """ Calculation Model """
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             related_name='calculations', blank=True, null=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Parameter',
                                  related_name='calculations', blank=True, null=True)
    test_stimuli_group = models.ManyToManyField(Stimulus, verbose_name='Stimulus', related_name='test_stimuli_groups',
                                                blank=True, null=True)
    rest_stimuli_group = models.ManyToManyField(Stimulus, verbose_name='Stimulus', related_name='rest_stimuli_groups',
                                                blank=True, null=True)

    class Meta:
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'

    def __str__(self):
        return '{}'.format(self.test)


class TestResult(models.Model):
    """ Result of the test Model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True, related_name='results')
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Test',
                             related_name='results')
    title = models.CharField(max_length=250, verbose_name='Title of Test Result', blank=True, null=True)
    description = models.TextField(verbose_name='Description of Test Result', blank=True, null=True)
    file = models.FileField(verbose_name='File', blank=True, null=True)
    date = models.DateField(verbose_name='Date of creation', default=date.today)
    status = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test result'
        verbose_name_plural = 'Test results'

    def __str__(self):
        return '{}'.format(self.user)

    def save(self, *args, **kwargs):
        self.title = 'Test result of {}'.format(self.test)
        super(TestResult, self).save(*args, **kwargs)


class TestResultStimuli(models.Model):
    """ Result of each stimulus of the test Model """
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, verbose_name='Test Result',
                                    related_name='test_results_stimulus', blank=True, null=True)
    stimuli = models.ForeignKey(Stimulus, on_delete=models.CASCADE, verbose_name='Stimulus',
                                related_name='test_results_stimulus')
    pow = ArrayField(models.FloatField(), default=list)
    fa1 = models.FloatField(verbose_name='Frontal Asymmetry 1 Value', blank=True, null=True)
    fa2 = models.FloatField(verbose_name='Frontal Asymmetry 2 Value', blank=True, null=True)
    tar = models.FloatField(verbose_name='Cognitive Load TAR Value', blank=True, null=True)
    coh = models.FloatField(verbose_name='Beta Coherence Value', blank=True, null=True)
    wave1 = models.FloatField(verbose_name='Beta Coherence Value - Wave1', blank=True, null=True)
    wave2 = models.FloatField(verbose_name='Beta Coherence Value - Wave2', blank=True, null=True)
    wave3 = models.FloatField(verbose_name='Beta Coherence Value - Wave3', blank=True, null=True)

    class Meta:
        verbose_name = 'Test Result Stimulus'
        verbose_name_plural = 'Test Result Stimulus'

    def __str__(self):
        return '{}'.format(self.test_result)

    def save(self, *args, **kwargs):
        self.fa1 = np.log(self.pow[56] / self.pow[11])
        self.fa2 = np.log(self.pow[61] / self.pow[6])
        self.tar = (self.pow[10] + self.pow[55]) / (self.pow[26] + self.pow[41])
        PC1 = np.nanmean(signal.coherence([self.pow[67]], [self.pow[57]])[1]) if np.any(
            np.isfinite(signal.coherence([self.pow[67]], [self.pow[57]])[1])) else 1
        PC2 = np.nanmean(signal.coherence([self.pow[67]], [self.pow[62]])[1]) if np.any(
            np.isfinite(signal.coherence([self.pow[67]], [self.pow[62]])[1])) else 1
        PC3 = np.nanmean(signal.coherence([self.pow[57]], [self.pow[62]])[1]) if np.any(
            np.isfinite(signal.coherence([self.pow[57]], [self.pow[62]])[1])) else 1
        self.coh = (PC1 + PC2 + PC3) / 3 * 100
        self.wave1 = self.pow[67]
        self.wave2 = self.pow[57]
        self.wave3 = self.pow[62]
        super(TestResultStimuli, self).save(*args, **kwargs)
