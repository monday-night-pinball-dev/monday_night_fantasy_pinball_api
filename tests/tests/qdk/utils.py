import json
import secrets
import string
from tokenize import String
from typing import Any, TypeVar

import pytest
from requests import Response

from tests.qdk.types import RequestOperators, TestContext
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)

T = TypeVar("T")


def generate_random_string(len: int = 12, charset: str | None = None):
    charset = charset or string.ascii_letters + string.digits

    result = "".join(secrets.choice(charset) for i in range(len))

    return result


def copy_object_when_appropriate(
    target_object: T, incoming_object: T, explicit_null_sets: list[str] | None = None
):
    explicit_null_sets = explicit_null_sets or []

    for key in incoming_object.__dict__.keys():
        if incoming_object.__dict__.get(key) is not None:
            # If incoming object contains a valid value, override it
            target_object.__dict__[key] = incoming_object.__dict__[key]

        elif key in explicit_null_sets:
            # If explicit null set lists the property and it's not None on the incoming object, override it to None
            target_object.__dict__[key] = None


def transform_operators_to_headers(request_operators: RequestOperators):
    headers: dict[str, str] = {}

    if request_operators.token is not None:
        headers["Authorization"] = f"Bearer {request_operators.token}"

    if request_operators.hydration_properties is not None:
        headers["MNFP-Hydration"] = ",".join(request_operators.hydration_properties)

    if request_operators.added_headers is not None:
        for key in request_operators.added_headers:
            headers[key] = request_operators.added_headers[key]

    return headers


T = TypeVar("T")


def assert_objects_are_equal(
    actual_object: object,
    expected_object: object,
    exempt_properties: list[str] | None = None,
):
    actual_object_dict: dict[str, Any] = {}
    excpected_object_dict: dict[str, Any] = {}

    if not isinstance(actual_object, dict):
        actual_object_dict = actual_object.__dict__
    else:
        actual_object_dict = actual_object

    if not isinstance(expected_object, dict):
        excpected_object_dict = expected_object.__dict__
    else:
        excpected_object_dict = expected_object

    exempt_properties = exempt_properties or list[str]()

    for key in actual_object_dict.keys():
        if key not in exempt_properties:
            actual_value = actual_object_dict[key]
            expected_value = excpected_object_dict[key]

            assert actual_value == expected_value, (
                f"Object Mismatch at key {key}: actual value {actual_value} did not match expected value {expected_value}"
            )


def assert_object_was_updated(
    original_object: dict[str, Any],
    update_object: dict[str, Any],
    final_object: dict[str, Any],
    exempt_properties: list[str],
):
    for key in final_object.keys():
        if key not in exempt_properties:
            if key in update_object.keys() and update_object[key] is not None:
                actual_value = final_object[key]
                expected_value = update_object[key]

                assert actual_value == expected_value, (
                    f"Object Mismatch at updated key {key}: final value {actual_value} did not match expected value from update model: {expected_value}"
                )
            else:
                actual_value = final_object[key]
                expected_value = original_object[key]

                assert actual_value == expected_value, (
                    f"Object Mismatch at non-updated key {key}: final value {actual_value} did not match expected value from original model: {expected_value}"
                )
