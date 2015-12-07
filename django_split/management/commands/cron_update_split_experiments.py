import six
import random
import datetime

from django.db import transaction
from django.core.management import BaseCommand

from django.contrib.auth.models import User

from django_split.base import EXPERIMENTS

from django_split.models import ExperimentState, ExperimentResult, \
    ExperimentGroup

class Command(BaseCommand):
    help = "Update the state of running django_split experiments"

    @transaction.atomic
    def handle(self, **options):
        verbose = int(options['verbosity']) >= 2

        today = datetime.date.today()
        now = datetime.datetime.utcnow()

        for slug, experiment in sorted(EXPERIMENTS.items()):
            state, _ = ExperimentState.objects.get_or_create(experiment=slug)

            if today >= experiment.start_date and state.started is None:
                state.started = now
                state.save(update_fields=('started',))

                if verbose:
                    self.stderr.write(
                        "Beginning experiment %s" % experiment.slug,
                    )

                if experiment.include_old_users:
                    ExperimentGroup.objects.bulk_create(
                        ExperimentGroup(
                            experiment=experiment.slug,
                            user=x,
                            group=random.randrange(len(experiment.groups)),
                        )
                        for x in User.objects.filter(
                            date_joined__lt=experiment.start_date,
                        ).iterator()
                    )

            if today >= experiment.end_date and state.completed is None:
                state.completed = now
                state.save(update_fields=('completed',))

                if verbose:
                    self.stderr.write(
                        "Completing experiment %s" % experiment.slug,
                    )

                for metric_idx, metric in enumerate(experiment.metrics):
                    for group_idx, group in enumerate(experiment.groups):
                        users = experiment.group(group)
                        ppf = metric(
                            experiment.start_date,
                            experiment.end_date,
                            users.filter(is_superuser=False),
                        )

                        ExperimentResult.objects.bulk_create(
                            ExperimentResult(
                                experiment=experiment.slug,
                                group=group_idx,
                                metric=metric_idx,
                                percentile=percentile,
                                value=ppf(percentile / 100),
                            )
                            for percentile in six.moves.range(1, 99 + 1)
                        )
