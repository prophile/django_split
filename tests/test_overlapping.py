from nose.tools import assert_raises

from django_split.utils import overlapping

def test_identity():
    assert overlapping(
        (10, 30),
        (10, 30),
    )

def test_contains():
    assert overlapping(
        (10, 30),
        (0, 40),
    )

def test_contained():
    assert overlapping(
        (0, 40),
        (10, 30),
    )

def test_left_equal_right_greater():
    assert overlapping(
        (0, 10),
        (0, 20),
    )

def test_left_equal_right_less():
    assert overlapping(
        (0, 10),
        (0, 5),
    )

def test_left_less_right_equal():
    assert overlapping(
        (0, 10),
        (-5, 10),
    )

def test_left_greater_right_equal():
    assert overlapping(
        (0, 10),
        (5, 10),
    )

def test_entirely_greater():
    assert not overlapping(
        (0, 10),
        (20, 30),
    )

def test_entirely_less():
    assert not overlapping(
        (0, 10),
        (-20, -10),
    )

def test_swapped_elements_in_first_argument_raises_valueerror():
    with assert_raises(ValueError):
        overlapping(
            (10, 0),
            (0, 10),
        )

def test_swapped_elements_in_second_argument_raises_valueerror():
    with assert_raises(ValueError):
        overlapping(
            (0, 10),
            (10, 0),
        )

def test_equal_arguments_do_not_raise_valueerror():
    overlapping((0, 0), (10, 10))
