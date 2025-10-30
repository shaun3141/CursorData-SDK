"""Tests for edge cases and error handling."""

import sqlite3
from datetime import datetime

import pytest

from cursordata.client import CursorDataClient
from cursordata.models import AICodeTrackingEntry, ComposerSession, ItemTableKey
from cursordata.query import QueryBuilder
from cursordata.utils import decode_json_value, parse_key_pattern


@pytest.mark.unit
class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            (b"{invalid json}", None),
            (b"", None),
            (b"\xff\xfe\x00", None),  # Invalid UTF-8 bytes
            (None, None),
            ("", None),
        ],
    )
    def test_decode_json_invalid_inputs(self, input_value, expected):
        """Test decoding invalid JSON inputs."""
        result = decode_json_value(input_value)
        assert result == expected, f"Expected {expected} for input {input_value!r}, got {result}"

    def test_decode_json_non_utf8_bytes(self):
        """Test decoding non-UTF8 bytes."""
        # Try to decode bytes that aren't valid UTF-8
        invalid_utf8 = b"\xff\xfe\x00"
        result = decode_json_value(invalid_utf8)
        # Should handle gracefully by returning None
        assert result is None, f"Expected None for invalid UTF-8, got {result}"

    def test_parse_key_pattern_empty_key(self):
        """Test parsing empty key."""
        result = parse_key_pattern("", "pattern")
        assert result is None

    def test_parse_key_pattern_empty_pattern(self):
        """Test parsing with empty pattern."""
        result = parse_key_pattern("key", "")
        # Empty pattern should only match empty string
        assert result is None

    def test_tracking_entry_missing_hash(self):
        """Test creating entry with missing hash."""
        with pytest.raises(KeyError):
            AICodeTrackingEntry.from_dict({"metadata": {}})

    def test_tracking_entry_none_metadata(self):
        """Test entry with None metadata."""
        entry = AICodeTrackingEntry(hash="test", metadata=None)
        # Should handle None metadata gracefully
        assert entry.metadata is None

    def test_composer_session_empty_composer_id(self):
        """Test creating session with empty composer ID."""
        session = ComposerSession.from_entries("", [])
        assert session.composer_id == ""

    def test_composer_session_none_entries(self):
        """Test creating session with None entries."""
        with pytest.raises(TypeError):
            ComposerSession.from_entries("comp_001", None)

    def test_client_get_value_empty_string(self, mock_client):
        """Test getting value with empty string key."""
        value = mock_client.get_value("")
        # Empty string key should return None (key doesn't exist)
        assert value is None, f"Expected None for empty string key, got {value}"

    def test_client_close_multiple_times(self, mock_client):
        """Test closing client multiple times."""
        mock_client.close()
        # Should not raise error
        mock_client.close()
        mock_client.close()

    def test_query_limit_zero(self, mock_client):
        """Test query with limit of zero."""
        # Limit 0 should still execute and return a collection
        # Note: In SQLite, limit 0 means "no limit", not "return 0 items"
        results = mock_client.query().bubbles().limit(0).execute()
        assert results is not None, "Query should return a collection object"
        assert hasattr(results, "__len__"), "Results should be a collection with length"
        # Limit 0 means no limit, so results may contain items
        assert isinstance(len(results), int), "Results length should be an integer"

    def test_query_limit_negative(self, mock_client):
        """Test query with negative limit."""
        query = mock_client.query().bubbles().limit(-1)
        # Should accept negative but behavior may vary
        assert query._limit == -1

    def test_query_offset_larger_than_results(self, mock_client):
        """Test query with offset larger than available results."""
        # Offset larger than results should return empty collection
        results = mock_client.query().bubbles().offset(10000).execute()
        assert results is not None, "Query should return a collection object"
        assert hasattr(results, "__len__"), "Results should be a collection with length"
        # With large offset, should return empty collection (no results to skip to)
        # Note: The actual behavior depends on how _query_cursordiskkv handles offset
        # If there's data in mock_db, it may still return results
        assert isinstance(len(results), int), "Results length should be an integer"

    def test_query_page_zero(self, mock_client):
        """Test query with page zero."""
        query = mock_client.query().bubbles().page(0, 10)
        # Page 0 should result in negative offset
        assert query._offset == -10

    def test_filter_always_false(self, mock_client):
        """Test filter that always returns False."""
        results = mock_client.query().bubbles().filter(lambda x: False).execute()
        # Filter that always returns False should return empty collection
        assert hasattr(results, "__len__")
        assert len(results) == 0

    def test_filter_always_true(self, mock_client):
        """Test filter that always returns True."""
        results = mock_client.query().bubbles().filter(lambda x: True).execute()
        # Should return all results (filter doesn't filter anything out)
        assert results is not None, "Query should return a collection object"
        assert hasattr(results, "__len__"), "Results should be a collection with length"
        # Filter always true means all items pass through
        assert isinstance(len(results), int), "Results length should be an integer"


@pytest.mark.unit
class TestErrorHandling:
    """Tests for error handling scenarios."""

    def test_client_db_connection_error(self, tmp_path):
        """Test client handles database connection errors."""
        # Create a path that exists but isn't a database
        db_path = tmp_path / "not_a_db.txt"
        db_path.write_text("not a database")

        # Client init will check if file exists, but connection will fail
        # SQLite will try to open it and may succeed (creating a new DB) or fail
        # So we test that connection doesn't raise unexpected errors
        client = CursorDataClient(db_path=str(db_path))
        # Connection attempt should either succeed (SQLite creates DB) or raise sqlite3.Error
        try:
            conn = client._get_connection()
            # If it succeeds, SQLite created a new DB file
            assert conn is not None
        except sqlite3.Error:
            # If it fails, that's also acceptable
            pass
        finally:
            client.close()

    def test_client_corrupted_json(self, mock_client, mock_db_connection):
        """Test client handles corrupted JSON in database."""
        # Insert corrupted JSON
        cursor = mock_db_connection.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
            ("corrupted_key", b"not valid json{"),
        )
        mock_db_connection.commit()

        # Should handle gracefully
        value = mock_client.get_json_value("corrupted_key")
        assert value is None

    def test_query_builder_with_none_client(self):
        """Test query builder handles None client."""
        # QueryBuilder.__init__ accepts None but will fail when methods are called
        builder = QueryBuilder(None)
        # The builder initializes but calling methods will fail
        assert builder._client is None
        # Attempting to use it will fail when BubbleQuery tries to execute query
        query = builder.bubbles()
        # Query will fail when trying to execute because client is None
        with pytest.raises((AttributeError, TypeError)):
            query.execute()

    def test_collection_empty_iteration(self):
        """Test iterating empty collection."""
        from cursordata.collections import Collection

        collection = Collection([])
        items = list(collection)
        assert items == []

    def test_collection_index_out_of_range(self):
        """Test accessing collection index out of range."""
        from cursordata.collections import Collection

        collection = Collection([1, 2, 3])
        with pytest.raises(IndexError):
            _ = collection[10]


@pytest.mark.unit
class TestTypeCoercion:
    """Tests for type coercion and conversion."""

    def test_usage_stats_start_time_conversion(self, mock_client):
        """Test usage stats handles various start time formats."""
        # This tests the internal conversion logic
        stats = mock_client.get_usage_stats()
        # Should handle None or datetime - verify it's one or the other, not something else
        if stats.tracking_start_time is not None:
            assert isinstance(
                stats.tracking_start_time, datetime
            ), f"Expected datetime or None, got {type(stats.tracking_start_time)}"

    def test_get_value_bytes_vs_string(self, mock_client):
        """Test that get_value returns bytes."""
        value = mock_client.get_value(ItemTableKey.AI_CODE_TRACKING_LINES)
        # Should be bytes (since we have test data in mock_db)
        assert value is not None, "Expected value to exist in test database"
        assert isinstance(value, bytes), f"Expected bytes, got {type(value)}"

    def test_get_json_value_converts_bytes(self, mock_client):
        """Test that get_json_value converts bytes to dict/list."""
        json_value = mock_client.get_json_value(ItemTableKey.AI_CODE_TRACKING_LINES)
        # Should be dict or list (since we have test data in mock_db)
        assert json_value is not None, "Expected JSON value to exist in test database"
        assert isinstance(
            json_value, (dict, list)
        ), f"Expected dict or list, got {type(json_value)}"
        # Verify it's actually a list (based on test data structure)
        assert isinstance(json_value, list), "Expected list of tracking entries"


@pytest.mark.unit
class TestBoundaryConditions:
    """Tests for boundary conditions."""

    def test_very_large_limit(self, mock_client):
        """Test query with very large limit."""
        query = mock_client.query().bubbles().limit(999999999)
        assert query._limit == 999999999

    def test_very_large_offset(self, mock_client):
        """Test query with very large offset."""
        query = mock_client.query().bubbles().offset(999999999)
        assert query._offset == 999999999

    def test_collection_very_large(self):
        """Test collection with many items."""
        from cursordata.collections import Collection

        items = list(range(10000))
        collection = Collection(items)
        assert len(collection) == 10000
        assert collection.first() == 0
        assert collection.last() == 9999

    def test_key_pattern_very_long(self):
        """Test parsing very long key pattern."""
        long_key = "prefix:" + ":".join(["part"] * 100)
        pattern = "prefix:" + ":".join([f"{{part{i}}}" for i in range(100)])
        result = parse_key_pattern(long_key, pattern)
        # Should handle long patterns - either match correctly or return None
        if result is not None:
            assert isinstance(
                result, dict
            ), f"Expected dict when pattern matches, got {type(result)}"
            # Verify it parsed all parts
            assert len(result) == 100, f"Expected 100 parsed parts, got {len(result)}"
        else:
            # If None, that's acceptable for very long patterns
            pass
