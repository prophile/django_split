from django.db import models

class ExperimentGroup(models.Model):
    experiment = models.CharField(max_length=48)

    user = models.ForeignKey('auth.User', related_name=None)

    group = models.IntegerField()

    class Meta:
        unique_together = (
            ('experiment', 'user'),
        )

class ExperimentState(models.Model):
    experiment = models.CharField(max_length=48, primary_key=True)

    started = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)

class ExperimentResult(models.Model):
    experiment = models.CharField(max_length=48)
    group = models.IntegerField()
    metric = models.IntegerField()

    percentile = models.IntegerField()
    value = models.FloatField()

    class Meta:
        unique_together = (
            ('experiment', 'group', 'metric', 'percentile'),
        )
