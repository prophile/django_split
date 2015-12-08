import pytest
import datetime
import freezegun

from django.core.management import call_command

from django_split import experiment_status, Experiment

def null_metric(start_date, end_date, users):
    return lambda p: p

class StatusExperiment(Experiment):
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2016, 2, 1)

    metrics = (null_metric,)

@pytest.mark.django_db
@freezegun.freeze_time('2016-03-01')
class StatusTests(object):
    def test_status(self):
        call_command('cron_update_split_experiments')

        for experiment, status, start, end, results in experiment_status():
            if experiment == 'status_experiment':
                assert start == StatusExperiment.start_date
                assert end == StatusExperiment.end_date
                assert status == 'completed'
                break
        else:
            raise AssertionError("Did not find experiment in experiments list")
