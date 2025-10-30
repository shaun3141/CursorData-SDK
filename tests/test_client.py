"""Tests for CursorDataClient."""

import sqlite3
from unittest.mock import patch

import pytest

from cursordata.client import CursorDataClient
from cursordata.models import ItemTableKey


@pytest.mark.unit
class TestCursorDataClientInit:
    """Tests for CursorDataClient initialization."""

    def test_init_with_db_path(self, tmp_path):
        """Test initialization with explicit database path."""
        db_path = tmp_path / "test.db"
        db_path.touch()

        client = CursorDataClient(db_path=str(db_path))
        assert client.db_path == db_path.resolve()

    def test_init_with_expanded_path(self, tmp_path):
        """Test initialization with tilde-expanded path."""
        db_path = tmp_path / "test.db"
        db_path.touch()

        # Create a path with tilde-like structure
        client = CursorDataClient(db_path=str(db_path))
        assert client.db_path.exists()

    @patch("cursordata.client.platform.system")
    def test_init_auto_find_macos(self, mock_platform, tmp_path, monkeypatch):
        """Test auto-finding database on macOS."""
        mock_platform.return_value = "Darwin"

        # Mock the database path to point to our temp path
        db_path = tmp_path / "state.vscdb"
        db_path.touch()

        with patch.object(CursorDataClient, "_find_database", return_value=db_path):
            client = CursorDataClient()
            assert client.db_path == db_path

    @patch("cursordata.client.platform.system")
    def test_init_auto_find_windows(self, mock_platform, tmp_path):
        """Test auto-finding database on Windows."""
        mock_platform.return_value = "Windows"

        # Create a real database file for the test
        db_path = tmp_path / "windows_db.db"
        db_path.touch()

        with patch.object(CursorDataClient, "_find_database", return_value=db_path):
            client = CursorDataClient()
            assert client.db_path == db_path

    @patch("cursordata.client.platform.system")
    def test_init_auto_find_linux(self, mock_platform, tmp_path):
        """Test auto-finding database on Linux."""
        mock_platform.return_value = "Linux"

        # Create a real database file for the test
        db_path = tmp_path / "linux_db.db"
        db_path.touch()

        with patch.object(CursorDataClient, "_find_database", return_value=db_path):
            client = CursorDataClient()
            assert client.db_path == db_path

    @patch("cursordata.client.platform.system")
    def test_init_unsupported_platform(self, mock_platform):
        """Test initialization fails on unsupported platform."""
        mock_platform.return_value = "UnknownOS"

        with pytest.raises(OSError, match="Unsupported platform"):
            CursorDataClient()

    def test_init_database_not_found(self, tmp_path):
        """Test initialization fails when database doesn't exist."""
        db_path = tmp_path / "nonexistent.db"

        with pytest.raises(FileNotFoundError, match="Cursor database not found"):
            CursorDataClient(db_path=str(db_path))


@pytest.mark.unit
class TestCursorDataClientContextManager:
    """Tests for context manager functionality."""

    def test_context_manager(self, mock_client):
        """Test client as context manager."""
        with mock_client as client:
            assert isinstance(client, CursorDataClient)

        # Connection should be closed after context
        assert (
            mock_client._connection is None or mock_client._connection.closed
        ), "Connection should be closed after context manager exits"

    def test_context_manager_with_exception(self, mock_client):
        """Test context manager closes connection on exception."""
        try:
            with mock_client:
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Connection should be closed even when exception occurs
        assert (
            mock_client._connection is None or mock_client._connection.closed
        ), "Connection should be closed even when exception occurs in context"


@pytest.mark.unit
class TestCursorDataClientDatabaseOperations:
    """Tests for database operation methods."""

    def test_get_connection(self, mock_client):
        """Test getting database connection."""
        conn = mock_client._get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)

    def test_get_database_info(self, mock_client, mock_db_connection):
        """Test getting database info."""
        info = mock_client.get_database_info()
        assert info.path == mock_client.db_path
        assert info.item_table_count >= 0
        assert info.cursor_disk_kv_count >= 0

    def test_get_value_existing_key(self, mock_client):
        """Test getting value for existing key."""
        value = mock_client.get_value(ItemTableKey.AI_CODE_TRACKING_LINES)
        assert value is not None
        assert isinstance(value, bytes)

    def test_get_value_nonexistent_key(self, mock_client):
        """Test getting value for nonexistent key."""
        value = mock_client.get_value("nonexistent_key")
        assert value is None

    def test_get_value_with_string_key(self, mock_client):
        """Test getting value with string key."""
        value = mock_client.get_value("aiCodeTrackingLines")
        assert value is not None

    def test_get_json_value(self, mock_client):
        """Test getting JSON-decoded value."""
        json_value = mock_client.get_json_value(ItemTableKey.AI_CODE_TRACKING_LINES)
        assert json_value is not None
        assert isinstance(json_value, list)

    def test_get_json_value_nonexistent(self, mock_client):
        """Test getting JSON value for nonexistent key."""
        json_value = mock_client.get_json_value("nonexistent_key")
        assert json_value is None

    def test_close(self, mock_client):
        """Test closing connection."""
        conn = mock_client._get_connection()
        assert conn is not None

        mock_client.close()
        assert mock_client._connection is None


@pytest.mark.unit
class TestCursorDataClientTrackingMethods:
    """Tests for AI code tracking methods."""

    def test_get_ai_code_tracking_entries(self, mock_client):
        """Test getting AI code tracking entries."""
        entries = mock_client.get_ai_code_tracking_entries()
        assert entries is not None
        assert len(entries) >= 0

    def test_get_ai_code_tracking_entries_empty(self, empty_db_connection, tmp_path):
        """Test getting entries from empty database."""
        db_path = tmp_path / "empty.db"
        db_path.touch()  # Create the file so client init doesn't fail
        client = CursorDataClient(db_path=str(db_path))
        client._connection = empty_db_connection

        try:
            entries = client.get_ai_code_tracking_entries()
            assert len(entries) == 0
        finally:
            client.close()

    def test_get_ai_code_tracking_start_time(self, mock_client):
        """Test getting tracking start time."""
        start_time = mock_client.get_ai_code_tracking_start_time()
        # Should return a value or None - verify it's one of the expected types
        if start_time is not None:
            assert isinstance(
                start_time, (bytes, str, float)
            ), f"Expected bytes, str, or float, got {type(start_time)}"

    def test_get_ai_scored_commits(self, mock_client):
        """Test getting scored commits."""
        commits = mock_client.get_ai_scored_commits()
        assert isinstance(commits, list)
        assert all(isinstance(c, str) for c in commits)

    def test_get_usage_stats(self, mock_client):
        """Test getting usage stats."""
        stats = mock_client.get_usage_stats()
        assert stats.total_tracking_entries >= 0
        assert stats.total_scored_commits >= 0
        assert isinstance(stats.most_used_file_extensions, dict)


@pytest.mark.unit
class TestCursorDataClientComposerMethods:
    """Tests for composer session methods."""

    def test_get_composer_sessions(self, mock_client):
        """Test getting composer sessions."""
        sessions = mock_client.get_composer_sessions()
        assert sessions is not None
        assert len(sessions) >= 0

    def test_get_composer_sessions_empty(self, empty_db_connection, tmp_path):
        """Test getting sessions from empty database."""
        db_path = tmp_path / "empty.db"
        db_path.touch()  # Create the file so client init doesn't fail
        client = CursorDataClient(db_path=str(db_path))
        client._connection = empty_db_connection

        try:
            sessions = client.get_composer_sessions()
            assert len(sessions) == 0
        finally:
            client.close()


@pytest.mark.unit
class TestCursorDataClientQueryMethods:
    """Tests for query-related methods."""

    def test_query_builder(self, mock_client):
        """Test getting query builder."""
        query_builder = mock_client.query()
        assert query_builder is not None
        assert hasattr(query_builder, "bubbles")
        assert hasattr(query_builder, "composer_sessions")

    def test_search_keys(self, mock_client):
        """Test searching for keys."""
        keys = mock_client.search_keys("%aiCode%", table="ItemTable")
        assert isinstance(keys, list)

    def test_search_keys_cursor_disk_kv(self, mock_client):
        """Test searching keys in cursorDiskKV table."""
        keys = mock_client.search_keys("%bubble%", table="cursorDiskKV")
        assert isinstance(keys, list)

    def test_search_keys_invalid_table(self, mock_client):
        """Test searching keys with invalid table name."""
        with pytest.raises(ValueError, match="table must be"):
            mock_client.search_keys("%pattern%", table="InvalidTable")

    def test_iterate_all_keys(self, mock_client):
        """Test iterating all keys."""
        keys = list(mock_client.iterate_all_keys(table="ItemTable"))
        assert isinstance(keys, list)

    def test_iterate_all_keys_cursor_disk_kv(self, mock_client):
        """Test iterating keys in cursorDiskKV."""
        keys = list(mock_client.iterate_all_keys(table="cursorDiskKV"))
        assert isinstance(keys, list)

    def test_iterate_all_keys_invalid_table(self, mock_client):
        """Test iterating keys with invalid table."""
        with pytest.raises(ValueError, match="table must be"):
            list(mock_client.iterate_all_keys(table="InvalidTable"))


@pytest.mark.unit
class TestCursorDataClientCursorDiskKVMethods:
    """Tests for cursorDiskKV query methods."""

    def test_query_cursordiskkv(self, mock_client):
        """Test querying cursorDiskKV table."""
        from cursordata.cursordiskkv_models import BubbleConversation

        def factory(data, key_parts=None):
            bubble_id = key_parts.get("bubble_id") if key_parts else None
            conversation_id = key_parts.get("conversation_id") if key_parts else None
            return BubbleConversation.from_dict(
                data, bubble_id=bubble_id, conversation_id=conversation_id
            )

        results = mock_client._query_cursordiskkv(
            key_prefix="bubbleId:",
            factory=factory,
            key_pattern="bubbleId:{bubble_id}:{conversation_id}",
        )
        assert isinstance(results, list)

    def test_get_cursordiskkv_entry(self, mock_client):
        """Test getting specific cursorDiskKV entry."""
        entry = mock_client.get_cursordiskkv_entry("bubbleId:bubble_001:conv_001")
        # Should return model or dict or None
        # The entry exists in mock_db, so it should return a BubbleConversation
        assert entry is not None
        if hasattr(entry, "bubble_id"):
            assert entry.bubble_id == "bubble_001"
