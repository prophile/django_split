from unittest import TestCase

from django_split.utils import overlapping

class OverlappingTests(TestCase):
    def test_identity(self):
        assert overlapping(
            (10, 30),
            (10, 30),
        )

    def test_contains(self):
        assert overlapping(
            (10, 30),
            (0, 40),
        )

    def test_contained(self):
        assert overlapping(
            (0, 40),
            (10, 30),
        )

    def test_left_equal_right_greater(self):
        assert overlapping(
            (0, 10),
            (0, 20),
        )

    def test_left_equal_right_less(self):
        assert overlapping(
            (0, 10),
            (0, 5),
        )

    def test_left_less_right_equal(self):
        assert overlapping(
            (0, 10),
            (-5, 10),
        )

    def test_left_greater_right_equal(self):
        assert overlapping(
            (0, 10),
            (5, 10),
        )

    def test_entirely_greater(self):
        assert not overlapping(
            (0, 10),
            (20, 30),
        )

    def test_entirely_less(self):
        assert not overlapping(
            (0, 10),
            (-20, -10),
        )

    def test_swapped_elements_in_first_argument_raises_valueerror(self):
        with self.assertRaises(ValueError):
            overlapping(
                (10, 0),
                (0, 10),
            )

    def test_swapped_elements_in_second_argument_raises_valueerror(self):
        with self.assertRaises(ValueError):
            overlapping(
                (0, 10),
                (10, 0),
            )

    def test_equal_arguments_do_not_raise_valueerror(self):
        overlapping((0, 0), (10, 10))
