from django.db import models
from datetime import date
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
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             blank=True, null=True, related_name='stimulus')
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
    stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, verbose_name='Stimulus',
                                 blank=True, null=True, related_name='parameters')
    fa1 = models.FloatField(verbose_name='Frontal Asymmetry 1', blank=True, null=True)
    fa2 = models.TextField(verbose_name='Frontal Asymmetry 2', blank=True, null=True)
    tar = models.DurationField(verbose_name='TAR', blank=True, null=True)
    coh = models.FileField(verbose_name='Coherence', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimuli'
        verbose_name_plural = 'Stimulus'

    def __str__(self):
        return '{}'.format(self.stimulus)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             blank=True, null=True, related_name='results')
    title = models.CharField(max_length=250, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    file = models.FileField(verbose_name='File', blank=True, null=True)
    date = models.DateField(verbose_name='Date of creation', default=date.today)
    status = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test result'
        verbose_name_plural = 'Test results'

    def __str__(self):
        return self.title
