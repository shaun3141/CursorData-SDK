"""Test utilities and helpers."""

from typing import Any, Optional

import pytest


def assert_dict_keys(
    d: dict[str, Any], required_keys: list[str], optional_keys: Optional[list[str]] = None
):
    """Assert that a dictionary has required keys.

    Args:
        d: Dictionary to check
        required_keys: List of keys that must be present
        optional_keys: Optional list of keys that may be present
    """
    for key in required_keys:
        assert key in d, f"Required key '{key}' missing from dictionary"

    if optional_keys:
        all_keys = set(d.keys())
        expected_keys = set(required_keys + optional_keys)
        unexpected_keys = all_keys - expected_keys
        if unexpected_keys:
            pytest.fail(f"Unexpected keys found: {unexpected_keys}")


def assert_type_or_none(value: Any, expected_type: type, message: Optional[str] = None):
    """Assert that value is either None or of expected type.

    Args:
        value: Value to check
        expected_type: Expected type if value is not None
        message: Optional custom error message
    """
    if value is not None:
        assert isinstance(value, expected_type), (
            message or f"Expected {expected_type.__name__} or None, got {type(value).__name__}"
        )


def assert_collection_not_empty(collection, message: Optional[str] = None):
    """Assert that a collection is not empty.

    Args:
        collection: Collection to check (must have __len__)
        message: Optional custom error message
    """
    assert hasattr(collection, "__len__"), "Collection must have __len__ method"
    assert len(collection) > 0, (
        message or f"Expected non-empty collection, got {len(collection)} items"
    )


def assert_collection_empty(collection, message: Optional[str] = None):
    """Assert that a collection is empty.

    Args:
        collection: Collection to check (must have __len__)
        message: Optional custom error message
    """
    assert hasattr(collection, "__len__"), "Collection must have __len__ method"
    assert len(collection) == 0, (
        message or f"Expected empty collection, got {len(collection)} items"
    )


class DatabaseAssertions:
    """Helper class for database-related assertions."""

    @staticmethod
    def assert_table_exists(connection, table_name: str):
        """Assert that a table exists in the database."""
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
        )
        result = cursor.fetchone()
        assert result is not None, f"Table '{table_name}' does not exist"

    @staticmethod
    def assert_table_empty(connection, table_name: str):
        """Assert that a table is empty."""
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        assert count == 0, f"Expected table '{table_name}' to be empty, got {count} rows"

    @staticmethod
    def assert_table_has_rows(connection, table_name: str, min_rows: int = 1):
        """Assert that a table has at least min_rows rows."""
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        assert (
            count >= min_rows
        ), f"Expected table '{table_name}' to have at least {min_rows} rows, got {count}"


class ModelAssertions:
    """Helper class for model-related assertions."""

    @staticmethod
    def assert_model_has_attributes(model, required_attrs: list[str]):
        """Assert that a model has required attributes.

        Args:
            model: Model instance to check
            required_attrs: List of attribute names that must exist
        """
        for attr in required_attrs:
            assert hasattr(
                model, attr
            ), f"Model {type(model).__name__} missing required attribute '{attr}'"

    @staticmethod
    def assert_model_attributes_not_none(model, attrs: list[str]):
        """Assert that model attributes are not None.

        Args:
            model: Model instance to check
            attrs: List of attribute names that should not be None
        """
        for attr in attrs:
            value = getattr(model, attr, None)
            assert value is not None, f"Model {type(model).__name__} attribute '{attr}' is None"


@pytest.fixture
def db_assertions():
    """Fixture providing database assertion helpers."""
    return DatabaseAssertions


@pytest.fixture
def model_assertions():
    """Fixture providing model assertion helpers."""
    return ModelAssertions
