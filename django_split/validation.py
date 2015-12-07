import datetime

def validate_experiment(experiment):
    _validate_date(experiment.start_date, "start_date")
    _validate_date(experiment.end_date, "end_date")

    groups = experiment.groups

    if len(groups) <= 2:
        raise ValueError("Experiment must have at least two groups")

    for group in groups:
        if not isinstance(group, str):
            raise TypeError(
                "Group %r is a %s, should be a string" % (
                    group,
                    type(group).__name__,
                ),
            )

    if experiment.control_group not in groups:
        raise ValueError("Control group not in groups")

    if len(set(experiment.groups)) != len(experiment.groups):
        raise ValueError("Duplicate group in groups list")

    if not experiment.metrics:
        raise ValueError("No metrics specified")

    if experiment.superuser_group is not None:
        if experiment.superuser_group not in groups:
            raise ValueError("Superuser group not in groups")

    if not experiment.include_old_users and not experiment.include_new_users:
        raise ValueError("Experiments excludes both old and new users")

def _validate_date(date, name):
    if not date:
        raise ValueError("%s not specified" % name)

    if isinstance(date, datetime.datetime):
        raise TypeError("%s is a datetime, should be a date" % name)

    if not isinstance(date, datetime.date):
        raise TypeError("%s should be a datetime.date" % name)
