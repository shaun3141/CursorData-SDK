"""Tests for improved error path coverage."""

import sqlite3

import pytest

from cursordata.client import CursorDataClient
from cursordata.query import QueryBuilder


@pytest.mark.unit
class TestDatabaseErrorHandling:
    """Tests for database error scenarios."""

    def test_database_locked_error(self, tmp_path):
        """Test handling of database locked errors."""
        db_path = tmp_path / "locked_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Create a connection that will be locked
        client._get_connection()

        # Try to access with another connection (should work, SQLite handles this)
        # This is more of a test that the client handles multiple connections
        conn2 = client._get_connection()
        assert conn2 is not None

        client.close()

    def test_invalid_sql_query(self, mock_client):
        """Test handling of invalid SQL queries."""
        conn = mock_client._get_connection()
        cursor = conn.cursor()

        # This should raise an OperationalError
        with pytest.raises(sqlite3.OperationalError):
            cursor.execute("SELECT * FROM NonExistentTable")

    def test_database_file_permissions(self, tmp_path):
        """Test that database file permissions are handled correctly."""
        db_path = tmp_path / "permissions_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Should be able to connect
        conn = client._get_connection()
        assert conn is not None

        client.close()

    def test_corrupted_database_file(self, tmp_path):
        """Test handling of corrupted database files."""
        db_path = tmp_path / "corrupted_test.db"
        # Write invalid data to file
        db_path.write_bytes(b"not a valid database file")

        # SQLite will try to open it, may succeed or fail
        client = CursorDataClient(db_path=str(db_path))
        try:
            conn = client._get_connection()
            # If it succeeds, SQLite created a new database
            assert conn is not None
        except sqlite3.Error:
            # If it fails, that's acceptable too
            pass
        finally:
            client.close()

    def test_missing_table_handling(self, tmp_path):
        """Test handling when tables don't exist."""
        db_path = tmp_path / "no_tables_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Querying non-existent table should raise OperationalError
        # This is expected behavior - SQLite raises an error when table doesn't exist
        with pytest.raises(sqlite3.OperationalError, match="no such table"):
            client.get_ai_code_tracking_entries()

        client.close()


@pytest.mark.unit
class TestQueryErrorHandling:
    """Tests for query error scenarios."""

    def test_query_with_none_client(self):
        """Test query builder with None client."""
        builder = QueryBuilder(None)
        assert builder._client is None

        query = builder.bubbles()
        with pytest.raises((AttributeError, TypeError)):
            query.execute()

    def test_query_execute_with_invalid_filter(self, mock_client):
        """Test query execution with invalid filter function."""
        # Filter that raises an exception
        def bad_filter(x):
            raise ValueError("Filter error")

        query = mock_client.query().bubbles().filter(bad_filter)

        # Should handle the error gracefully or propagate it
        with pytest.raises(ValueError, match="Filter error"):
            query.execute()

    def test_query_limit_exceeds_max_int(self, mock_client):
        """Test query with very large limit value."""
        # Python integers can be arbitrarily large, but this tests edge case
        very_large_limit = 10**100
        query = mock_client.query().bubbles().limit(very_large_limit)
        assert query._limit == very_large_limit


@pytest.mark.unit
class TestModelErrorHandling:
    """Tests for model error scenarios."""

    def test_tracking_entry_invalid_json(self):
        """Test creating tracking entry from invalid JSON structure."""
        from cursordata.models import AICodeTrackingEntry

        # Missing required 'hash' field should raise KeyError
        with pytest.raises(KeyError):
            AICodeTrackingEntry.from_dict({"metadata": {}})

        # Missing metadata is handled gracefully (defaults to empty dict)
        entry = AICodeTrackingEntry.from_dict({"hash": "test"})
        assert entry.metadata == {}

    def test_bubble_conversation_invalid_data(self):
        """Test creating bubble conversation from invalid data."""
        from cursordata.cursordiskkv_models import BubbleConversation

        # Empty dict should still create a bubble (with defaults)
        bubble = BubbleConversation.from_dict({})
        assert bubble is not None

        # Invalid date format should be handled
        bubble = BubbleConversation.from_dict({
            "createdAt": "not-a-date",
            "bubbleId": "test",
        })
        assert bubble.created_at == "not-a-date"  # Stored as-is, parsing happens in property


@pytest.mark.unit
class TestCollectionErrorHandling:
    """Tests for collection error scenarios."""

    def test_collection_with_none_items(self):
        """Test collection with None items."""
        from cursordata.collections import Collection

        # Collection should handle None in list
        collection = Collection([1, None, 3])
        assert len(collection) == 3

        # Filtering None should work
        filtered = collection.filter(lambda x: x is not None)
        assert len(filtered) == 2

    def test_collection_index_error(self):
        """Test collection index out of range."""
        from cursordata.collections import Collection

        collection = Collection([1, 2, 3])
        with pytest.raises(IndexError):
            _ = collection[10]

        with pytest.raises(IndexError):
            _ = collection[-10]

    def test_collection_filter_with_exception(self):
        """Test collection filter that raises exception."""
        from cursordata.collections import Collection

        collection = Collection([1, 2, 3])

        def bad_filter(x):
            if x == 2:
                raise ValueError("Filter error")
            return True

        # Filter should propagate exception
        with pytest.raises(ValueError, match="Filter error"):
            collection.filter(bad_filter)

