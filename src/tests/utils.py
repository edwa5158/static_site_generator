import unittest
from collections.abc import Callable
from typing import Any


def expected_error(
    test_case: unittest.TestCase,
    expression_to_evaluate: Callable[[], Any],
    expected_exception: type[BaseException] | tuple[type[BaseException], ...],
):
    with test_case.assertRaises(expected_exception) as cm:
        expression_to_evaluate()

    expected_types = (
        expected_exception
        if isinstance(expected_exception, tuple)
        else (expected_exception,)
    )
    if type(cm.exception) not in expected_types:
        test_case.fail(
            f"different exception type detected: {type(cm.exception)}"
            + f"{cm.exception.__traceback__ = }"
        )

    return cm
