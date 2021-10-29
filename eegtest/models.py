from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=250, unique=True, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    status = models.BooleanField(verbose_name='Status', default=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title


class StimuliCategory(models.Model):
    title = models.CharField(max_length=250, verbose_name='Stimuli category', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimuli category'
        verbose_name_plural = 'Stimuli categories'

    def __str__(self):
        return self.title


class Stimuli(models.Model):
    index = models.PositiveIntegerField(verbose_name='Order index', blank=True, null=True)
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

