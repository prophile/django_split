import six
import datetime
import inflection

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
            ),
        )

    @classmethod
    def in_group(cls, user, group):
        return user in cls.group(group)
