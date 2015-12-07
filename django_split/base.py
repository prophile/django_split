import six
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
