import six
import datetime
import inflection

from .utils import overlapping
from .validation import validate_experiment

EXPERIMENTS = {}

class ExperimentMeta(type):
    def __init__(self, name, bases, dict):
        super(ExperimentMeta, self).__init__(name, bases, dict)

        # Special case: don't do experiment processing on the base class
        if (
            name == 'Experiment' and
            self.__module__ == ExperimentMeta.__module__
        ):
            return

        slug = inflection.underscore(name)

        if len(slug) > 48:
            raise ValueError("Experiment name too long")

        if slug in EXPERIMENTS:
            raise AssertionError(
                "Experiment %s defined multiple times (as %s.%s and %s.%s)" % (
                    slug,
                    dict['__module__'],
                    dict['__qualname__'],
                    EXPERIMENTS[slug].__module__,
                    EXPERIMENTS[slug].__qualname__,
                ),
            )

        validate_experiment(self)

        self.slug = slug
        EXPERIMENTS[slug] = self

class Experiment(six.with_metaclass(ExperimentMeta)):
    groups = ('control', 'experiment')
    control_group = 'control'

    superuser_group = None

    include_new_users = True
    include_old_users = True

    metrics = ()

    start_date = None
    end_date   = None

    @classmethod
    def group(cls, group_name):
        # Lazy-load these to avoid import issues
        from django.contrib.auth.models import User
        from .models import ExperimentGroup

        # This will raise a ValueError if the group does not exist. Whilst
        # group_index is not used if we're before the experiment start date,
        # we want to catch errors from using the wrong group name immediately.
        group_index = cls.groups.index(group_name)

        # TODO: superuser logic

        # Until the start of the experiment, all users are in the control group
        if datetime.date.today() < cls.start_date:
            if group_name == cls.control_group:
                return User.objects.all()
            else:
                return User.objects.none()

        return User.objects.filter(id__in=
            ExperimentGroup.objects.filter(
                experiment=cls.slug,
                group=group_index,
            ).values('user_id'),
        )

    @classmethod
    def in_group(cls, user, group):
        return user in cls.group(group)

def experiment_status():
    """An iterable of (experiment name, status, start date, end date, results)"""

    now = datetime.date.today()

    from .models import ExperimentState, ExperimentResult  # Avoid circular import

    for experiment_state in ExperimentState.objects.order_by(
        'experiment',
    ).iterator():
        results = []

        experiment = EXPERIMENTS[experiment_state.experiment]

        if experiment_state.completed is not None:
            status = 'completed'

            for metric_idx, metric in enumerate(experiment.metrics):
                metric_name = metric.__name__
                metric_description = getattr(metric, '__doc__', "")

                by_group = {}

                for group_idx, group in enumerate(experiment.groups):
                    percentiles = dict(
                        ExperimentResult.objects.filter(
                            experiment=experiment.slug,
                            group=group_idx,
                            metric=metric_idx,
                        ).values_list('percentile', 'value')
                    )

                    by_group[group] = percentiles

                # Work out if any experiment group does not overlap with the
                # control group error bars.

                if any(not overlapping(
                        (x[5], x[95]),
                        (by_group[experiment.control_group][5],
                         by_group[experiment.control_group][95])
                    )
                    for x in by_group.values()
                ):
                    # These results are significant
                    results.append({
                        'name': metric_name,
                        'description': metric_description,
                        'significant': True,
                        'groups': by_group,
                    })
                else:
                    results.append({
                        'name': metric_name,
                        'description': metric_description,
                        'significant': False,
                    })

        elif experiment_state.started is not None:
            status = 'running'
        else:
            status = 'upcoming'

        yield (
            experiment.slug,
            status,
            experiment.start_date,
            experiment.end_date,
            results,
        )
