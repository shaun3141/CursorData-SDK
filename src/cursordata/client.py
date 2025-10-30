"""Main SDK client for interacting with the Cursor database."""

import logging
import platform
import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, Union

from cursordata.collections import (
    AICodeTrackingCollection,
    ComposerSessionCollection,
)
from cursordata.cursordiskkv_models import (
    BubbleConversation,
    Checkpoint,
    CodeBlockDiff,
    ComposerData,
    InlineDiffs,
    MessageRequestContext,
)
from cursordata.models import (
    AICodeTrackingEntry,
    ComposerSession,
    DatabaseInfo,
    DatabaseLocation,
    ItemTableKey,
    UsageStats,
)
from cursordata.query import QueryBuilder
from cursordata.utils import decode_json_value, parse_cursordiskkv_rows

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CursorDataClient:
    """Client for accessing Cursor editor's local SQLite database.

    This client provides strongly-typed methods to query and analyze
    Cursor usage data stored in the local database.

    Example:
        >>> client = CursorDataClient()
        >>> stats = client.get_usage_stats()
        >>> isinstance(stats.total_tracking_entries, int)
        True
        >>> entries = client.get_ai_code_tracking_entries()
        >>> isinstance(entries, list)
        True
        >>> client.close()
    """

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the CursorData client.

        Args:
            db_path: Optional path to the database file. If not provided,
                    will attempt to find it automatically based on the platform.

        Raises:
            FileNotFoundError: If the database file cannot be found.
            sqlite3.Error: If there's an error connecting to the database.
        """
        if db_path:
            self.db_path = Path(db_path).expanduser().resolve()
        else:
            self.db_path = self._find_database()

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Cursor database not found at {self.db_path}. "
                "Make sure Cursor is installed and has been run at least once."
            )

        self._connection: Optional[sqlite3.Connection] = None

    def _find_database(self) -> Path:
        """Find the Cursor database based on the current platform."""
        system = platform.system()
        if system == "Darwin":
            location = DatabaseLocation.MACOS.value
        elif system == "Windows":
            location = DatabaseLocation.WINDOWS.value
        elif system == "Linux":
            location = DatabaseLocation.LINUX.value
        else:
            raise OSError(f"Unsupported platform: {system}")

        return Path(location).expanduser().resolve()

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create a database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "CursorDataClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def query(self) -> QueryBuilder:
        """Get a query builder for fluent queries.

        Returns:
            QueryBuilder instance for building queries.

        Example:
            >>> client.query().bubbles().where(created_after=datetime.now() - timedelta(days=7)).execute()
            >>> client.query().composer_sessions().filter_by_extension(".py").execute()
        """
        return QueryBuilder(self)

    def _query_cursordiskkv(
        self,
        key_prefix: str,
        factory: Callable[[dict[str, Any], Optional[dict[str, str]]], Optional[T]],
        key_pattern: Optional[str] = None,
        key_parser: Optional[Callable[[str], dict[str, str]]] = None,
        filter_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
        exact_match: bool = False,
    ) -> list[T]:
        """Generic helper to query cursorDiskKV table.

        Args:
            key_prefix: Key prefix to match (e.g., "bubbleId:", "checkpointId:")
            factory: Function to create model instances from data dict and optional key parts.
            key_pattern: Optional pattern for key parsing (e.g., "bubbleId:{bubble_id}:{conversation_id}").
            key_parser: Optional custom function to parse key into parts.
            filter_id: Optional ID to filter by (appended to prefix).
            limit: Maximum number of results.
            offset: Number of results to skip.
            exact_match: If True, use exact key match instead of LIKE.

        Returns:
            List of model instances.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        if filter_id:
            if exact_match:
                query = "SELECT key, value FROM cursorDiskKV WHERE key = ?"
                params = (f"{key_prefix}{filter_id}",)
            else:
                query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE ?"
                params = (f"{key_prefix}{filter_id}:%",)
        else:
            if exact_match:
                query = "SELECT key, value FROM cursorDiskKV WHERE key = ?"
                params = (key_prefix,)
            else:
                query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE ?"
                params = (f"{key_prefix}%",)

        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return parse_cursordiskkv_rows(rows, factory, key_parser, key_pattern)

    def get_database_info(self) -> DatabaseInfo:
        """Get information about the database.

        Returns:
            DatabaseInfo object with database metadata.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get counts
        cursor.execute("SELECT COUNT(*) FROM ItemTable")
        item_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM cursorDiskKV")
        kv_count = cursor.fetchone()[0]

        # Get last modified time
        last_modified = None
        if self.db_path.exists():
            mtime = self.db_path.stat().st_mtime
            from datetime import datetime

            last_modified = datetime.fromtimestamp(mtime)

        return DatabaseInfo(
            path=self.db_path,
            item_table_count=item_count,
            cursor_disk_kv_count=kv_count,
            last_modified=last_modified,
        )

    def get_value(self, key: Union[str, ItemTableKey]) -> Optional[Any]:
        """Get a raw value from ItemTable.

        Args:
            key: The key to look up (string or ItemTableKey enum).

        Returns:
            The value as bytes, or None if key doesn't exist.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        key_str = key.value if isinstance(key, ItemTableKey) else key

        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key_str,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

    def get_json_value(self, key: Union[str, ItemTableKey]) -> Optional[Any]:
        """Get a JSON-parsed value from ItemTable.

        Args:
            key: The key to look up (string or ItemTableKey enum).

        Returns:
            The parsed JSON value, or None if key doesn't exist or can't be parsed.
        """
        value = self.get_value(key)
        if value is None:
            return None
        return decode_json_value(value)

    def get_ai_code_tracking_entries(self) -> AICodeTrackingCollection:
        """Get all AI code tracking entries.

        Returns:
            Collection of AICodeTrackingEntry objects.
        """
        data = self.get_json_value(ItemTableKey.AI_CODE_TRACKING_LINES)
        if not data or not isinstance(data, list):
            return AICodeTrackingCollection([])

        entries = []
        for entry_data in data:
            if isinstance(entry_data, dict):
                try:
                    entries.append(AICodeTrackingEntry.from_dict(entry_data))
                except (KeyError, TypeError):
                    continue

        return AICodeTrackingCollection(entries)

    def get_ai_code_tracking_start_time(self) -> Optional[float]:
        """Get the AI code tracking start time.

        Returns:
            Unix timestamp as float, or None if not available.
        """
        return self.get_value(ItemTableKey.AI_CODE_TRACKING_START_TIME)

    def get_ai_scored_commits(self) -> list[str]:
        """Get list of scored commit hashes.

        Returns:
            List of commit hash strings.
        """
        data = self.get_json_value(ItemTableKey.AI_CODE_TRACKING_SCORED_COMMITS)
        if isinstance(data, list):
            return [str(commit) for commit in data if commit]
        return []

    def get_usage_stats(self) -> UsageStats:
        """Get aggregated usage statistics.

        Returns:
            UsageStats object with aggregated data.
        """
        entries_collection = self.get_ai_code_tracking_entries()
        commits = self.get_ai_scored_commits()
        start_time = self.get_ai_code_tracking_start_time()

        # Count file extensions
        extension_counts: dict[str, int] = {}
        composer_sessions: set = set()

        for entry in entries_collection:
            if entry.file_extension:
                extension_counts[entry.file_extension] = (
                    extension_counts.get(entry.file_extension, 0) + 1
                )
            if entry.composer_id:
                composer_sessions.add(entry.composer_id)

        # Parse start time
        tracking_start = None
        if start_time is not None:
            try:
                from datetime import datetime

                tracking_start = datetime.fromtimestamp(float(start_time))
            except (ValueError, TypeError, OSError):
                pass

        return UsageStats(
            total_tracking_entries=len(entries_collection),
            total_scored_commits=len(commits),
            tracking_start_time=tracking_start,
            most_used_file_extensions=extension_counts,
            composer_sessions=len(composer_sessions),
        )

    def get_composer_sessions(self) -> ComposerSessionCollection:
        """Get all composer sessions with their associated data.

        Returns:
            Collection of ComposerSession objects grouped by composer_id.
        """
        entries = self.get_ai_code_tracking_entries()

        # Group entries by composer_id
        sessions_dict: dict[str, list[AICodeTrackingEntry]] = {}
        for entry in entries:
            if entry.composer_id:
                if entry.composer_id not in sessions_dict:
                    sessions_dict[entry.composer_id] = []
                sessions_dict[entry.composer_id].append(entry)

        # Convert to ComposerSession objects
        sessions = [
            ComposerSession.from_entries(composer_id, session_entries)
            for composer_id, session_entries in sessions_dict.items()
        ]
        return ComposerSessionCollection(sessions)

    def get_cursordiskkv_entry(self, key: str) -> Optional[
        Union[
            BubbleConversation,
            MessageRequestContext,
            Checkpoint,
            CodeBlockDiff,
            ComposerData,
            InlineDiffs,
            dict[str, Any],
        ]
    ]:
        """Get a specific cursorDiskKV entry by key.

        Args:
            key: The full database key (e.g., "bubbleId:xxx:yyy").

        Returns:
            Typed model object if the key matches a known pattern, otherwise raw dict.
            Returns None if key doesn't exist.
        """
        from cursordata.utils import parse_key_pattern

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key = ?", (key,))
        row = cursor.fetchone()

        if not row:
            return None

        data = decode_json_value(row["value"])
        if data is None or not isinstance(data, dict):
            return data

        # Route to appropriate model based on key prefix
        if key.startswith("bubbleId:"):
            key_parts = parse_key_pattern(key, "bubbleId:{bubble_id}:{conversation_id}")
            bubble_id = key_parts.get("bubble_id") if key_parts else None
            conversation_id = key_parts.get("conversation_id") if key_parts else None
            return BubbleConversation.from_dict(
                data, bubble_id=bubble_id, conversation_id=conversation_id
            )
        elif key.startswith("messageRequestContext:"):
            return MessageRequestContext.from_dict(data)
        elif key.startswith("checkpointId:"):
            return Checkpoint.from_dict(data)
        elif key.startswith("codeBlockDiff:"):
            return CodeBlockDiff.from_dict(data)
        elif key.startswith("composerData:"):
            return ComposerData.from_dict(data)
        elif key.startswith("inlineDiffs-"):
            ws_id = key.replace("inlineDiffs-", "")
            return InlineDiffs.from_dict(ws_id, data)
        else:
            # Unknown pattern, return raw dict
            return data

    def search_keys(self, pattern: str, table: str = "ItemTable") -> list[str]:
        """Search for keys matching a pattern.

        Args:
            pattern: SQL LIKE pattern to search for (use % for wildcards).
            table: Table to search in ("ItemTable" or "cursorDiskKV").

        Returns:
            List of matching keys.
        """
        if table not in ["ItemTable", "cursorDiskKV"]:
            raise ValueError("table must be 'ItemTable' or 'cursorDiskKV'")

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT key FROM {table} WHERE key LIKE ?", (pattern,))
        return [row[0] for row in cursor.fetchall()]

    def iterate_all_keys(self, table: str = "ItemTable") -> Iterator[str]:
        """Iterate over all keys in a table.

        Args:
            table: Table to iterate ("ItemTable" or "cursorDiskKV").

        Yields:
            Key strings one at a time.
        """
        if table not in ["ItemTable", "cursorDiskKV"]:
            raise ValueError("table must be 'ItemTable' or 'cursorDiskKV'")

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT key FROM {table}")
        for row in cursor:
            yield row[0]
