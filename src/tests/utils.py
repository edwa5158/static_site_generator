import unittest
from collections.abc import Callable
from typing import Any


def expected_error(
    test_case: unittest.TestCase,
    expression_to_evaluate: Callable[[], Any],
    expected_exception: type[BaseException],  # | tuple[type[BaseException], ...],
):
    with test_case.assertRaises(expected_exception) as cm:
        expression_to_evaluate()

    # expected_types = (
    #     expected_exception
    #     if isinstance(expected_exception, tuple)
    #     else (expected_exception,)
    # )
    if not hasattr(cm, "exception"):
        test_case.fail("no exception was raised")

    elif type(cm.exception) == expected_error:
        test_case.fail(
            f"different exception type detected:\n"
            f"\texpected exception: {expected_exception}\n"
            f"\tactual exception: {type(cm.exception)}\n"
            f"\t{cm.exception.__traceback__ = }"
        )

    return cm
