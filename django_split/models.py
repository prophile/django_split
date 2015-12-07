import random
import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

class ExperimentGroup(models.Model):
    experiment = models.CharField(max_length=48)

    user = models.ForeignKey(
        'auth.User',
        related_name='django_split_experiment_groups',
    )

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

# Done here in order that the signal is always connected
@receiver(post_save, sender=User, dispatch_uid="select_experiment_groups")
def select_experiment_groups(sender, instance, created, **kwargs):
    if not created:
        return

    now = datetime.date.today()
    from .base import EXPERIMENTS # Avoid circular import

    ExperimentGroup.objects.bulk_create(
        ExperimentGroup(
            experiment=experiment.slug,
            user=instance,
            group=random.randrange(len(experiment.groups)),
        )
        for experiment in EXPERIMENTS.values()
        if experiment.start_date <= now < experiment.end_date
        and experiment.include_new_users
    )
