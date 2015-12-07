import datetime
import freezegun

from django.test import TestCase

from django.contrib.auth.models import User

from django_split import Experiment

def null_metric(start_date, end_date, users):
    return lambda p: 0

class TestExperiment(Experiment):
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2016, 1, 15)

    metrics = (null_metric,)

@freezegun.freeze_time('2016-01-01')
class GroupingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="bees",
            email="bees@example.com",
        )

    def test_does_not_throw_exceptions(self):
        TestExperiment.in_group(self.user, 'experiment')
