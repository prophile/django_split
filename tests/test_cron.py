import datetime
import freezegun

from django.core.management import call_command
from django.test import TestCase
from django_split import Experiment
from django_split.models import ExperimentState, ExperimentResult

def null_metric(start_date, end_date, users):
    return lambda p: p

class CronExperiment(Experiment):
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2016, 2, 1)

    metrics = (null_metric,)

class CronTests(TestCase):
    def run_command(self):
        call_command('cron_update_split_experiments')

    def get_state(self):
        return ExperimentState.objects.get(experiment=CronExperiment.slug)

    def test_creates_entries_for_missing_experiments(self):
        self.run_command()
        self.get_state()  # Make sure this does not throw errors

    def test_is_idempotent(self):
        self.run_command()
        self.run_command()

    @freezegun.freeze_time('2015-12-31')
    def test_does_not_start_experiments_early(self):
        self.run_command()
        self.assertIsNone(
            self.get_state().started,
        )

    @freezegun.freeze_time('2016-01-01')
    def test_starts_experiments(self):
        self.run_command()
        self.assertEqual(
            self.get_state().started,
            datetime.datetime(2016, 1, 1),
        )

    def test_does_not_restart_experiments(self):
        with freezegun.freeze_time('2016-01-01'):
            self.run_command()

        with freezegun.freeze_time('2016-01-02'):
            self.run_command()

        self.assertEqual(
            self.get_state().started,
            datetime.datetime(2016, 1, 1),
        )

    @freezegun.freeze_time('2016-01-12')
    def test_does_not_end_experiments_early(self):
        self.run_command()
        self.assertIsNone(
            self.get_state().completed,
        )

    @freezegun.freeze_time('2016-02-01')
    def test_ends_experiments(self):
        self.run_command()
        self.assertEqual(
            self.get_state().completed,
            datetime.datetime(2016, 2, 1),
        )

    def test_does_not_double_complete_experiments(self):
        with freezegun.freeze_time('2016-02-01'):
            self.run_command()

        with freezegun.freeze_time('2016-02-02'):
            self.run_command()

        self.assertEqual(
            self.get_state().completed,
            datetime.datetime(2016, 2, 1),
        )

    @freezegun.freeze_time('2016-02-01')
    def test_records_metrics_for_completed_experiments(self):
        self.run_command()

        num_results = ExperimentResult.objects.filter(
            experiment=CronExperiment.slug,
            group=0,
            metric=0,
        ).count()

        self.assertEqual(num_results, 99)  # One for each percentile 1-99
