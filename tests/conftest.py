"""Pytest configuration and shared fixtures."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from cursordata.cursordiskkv_models import BubbleConversation
from cursordata.models import (
    AICodeTrackingEntry,
    ComposerSession,
    ItemTableKey,
    UsageStats,
)


@pytest.fixture
def sample_tracking_entry_data() -> dict[str, Any]:
    """Sample AI code tracking entry data."""
    return {
        "hash": "abc123",
        "metadata": {
            "source": "composer",
            "composerId": "comp_001",
            "fileExtension": ".py",
            "fileName": "/path/to/file.py",
        },
    }


@pytest.fixture
def sample_tracking_entry(sample_tracking_entry_data: dict[str, Any]) -> AICodeTrackingEntry:
    """Sample AICodeTrackingEntry instance."""
    return AICodeTrackingEntry.from_dict(sample_tracking_entry_data)


@pytest.fixture
def sample_tracking_entries() -> list[AICodeTrackingEntry]:
    """Multiple sample tracking entries."""
    return [
        AICodeTrackingEntry(
            hash="hash1",
            metadata={
                "source": "composer",
                "composerId": "comp_001",
                "fileExtension": ".py",
                "fileName": "/path/to/file1.py",
            },
        ),
        AICodeTrackingEntry(
            hash="hash2",
            metadata={
                "source": "composer",
                "composerId": "comp_001",
                "fileExtension": ".py",
                "fileName": "/path/to/file2.py",
            },
        ),
        AICodeTrackingEntry(
            hash="hash3",
            metadata={
                "source": "composer",
                "composerId": "comp_002",
                "fileExtension": ".ts",
                "fileName": "/path/to/file3.ts",
            },
        ),
        AICodeTrackingEntry(
            hash="hash4",
            metadata={
                "source": "chat",
                "composerId": None,
                "fileExtension": ".js",
                "fileName": "/path/to/file4.js",
            },
        ),
    ]


@pytest.fixture
def sample_composer_session_data(
    sample_tracking_entries: list[AICodeTrackingEntry],
) -> ComposerSession:
    """Sample ComposerSession."""
    entries_001 = [e for e in sample_tracking_entries if e.composer_id == "comp_001"]
    return ComposerSession.from_entries("comp_001", entries_001)


@pytest.fixture
def sample_bubble_data() -> dict[str, Any]:
    """Sample bubble conversation data."""
    return {
        "_v": 1,
        "type": 1,
        "bubbleId": "bubble_001",
        "requestId": "req_001",
        "checkpointId": "checkpoint_001",
        "text": "Test conversation",
        "richText": "<p>Test conversation</p>",
        "createdAt": "2024-01-01T00:00:00Z",
        "context": {},
        "attachedCodeChunks": [],
        "suggestedCodeBlocks": [
            {"file": "test.py", "code": "print('hello')"},
        ],
        "assistantSuggestedDiffs": [],
        "diffsSinceLastApply": [],
        "modelInfo": {"modelName": "gpt-4"},
        "tokenCount": {"inputTokens": 100, "outputTokens": 50},
        "isAgentic": False,
        "lints": [],
        "multiFileLinterErrors": [],
    }


@pytest.fixture
def sample_bubble_conversation(sample_bubble_data: dict[str, Any]) -> BubbleConversation:
    """Sample BubbleConversation instance."""
    return BubbleConversation.from_dict(sample_bubble_data, bubble_id="bubble_001")


@pytest.fixture
def mock_db_path(tmp_path: Path) -> Path:
    """Create a temporary database file path."""
    return tmp_path / "test_db.db"


@pytest.fixture
def mock_db_connection(mock_db_path: Path):
    """Create a mock SQLite database connection."""
    conn = sqlite3.connect(str(mock_db_path))
    cursor = conn.cursor()

    # Create tables
    cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")
    cursor.execute("CREATE TABLE IF NOT EXISTS cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)")

    # Insert sample data
    sample_tracking_data = [
        {
            "hash": "hash1",
            "metadata": {
                "source": "composer",
                "composerId": "comp_001",
                "fileExtension": ".py",
                "fileName": "/path/to/file1.py",
            },
        },
        {
            "hash": "hash2",
            "metadata": {
                "source": "composer",
                "composerId": "comp_001",
                "fileExtension": ".py",
                "fileName": "/path/to/file2.py",
            },
        },
    ]

    cursor.execute(
        "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
        (
            ItemTableKey.AI_CODE_TRACKING_LINES.value,
            json.dumps(sample_tracking_data).encode("utf-8"),
        ),
    )

    cursor.execute(
        "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
        (
            ItemTableKey.AI_CODE_TRACKING_SCORED_COMMITS.value,
            json.dumps(["commit1", "commit2"]).encode("utf-8"),
        ),
    )

    cursor.execute(
        "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
        (ItemTableKey.AI_CODE_TRACKING_START_TIME.value, b"1704067200.0"),
    )

    # Sample bubble conversation
    bubble_data = {
        "_v": 1,
        "type": 1,
        "bubbleId": "bubble_001",
        "requestId": "req_001",
        "createdAt": "2024-01-01T00:00:00Z",
        "modelName": "gpt-4",
        "inputTokens": 100,
        "outputTokens": 50,
        "isAgentic": False,
    }

    cursor.execute(
        "INSERT INTO cursorDiskKV (key, value) VALUES (?, ?)",
        ("bubbleId:bubble_001:conv_001", json.dumps(bubble_data)),
    )

    conn.commit()
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


@pytest.fixture
def mock_client(mock_db_path: Path, mock_db_connection):
    """Create a CursorDataClient with mocked database."""
    from cursordata.client import CursorDataClient

    client = CursorDataClient(db_path=str(mock_db_path))
    client._connection = mock_db_connection
    return client


@pytest.fixture
def mock_platform(monkeypatch):
    """Mock platform.system() to return a specific platform."""

    def _mock_platform(system_name: str = "Darwin"):
        """Create a platform mock."""
        original_system = __import__("platform").system

        def mock_system():
            return system_name

        monkeypatch.setattr("platform.system", mock_system)
        return original_system

    return _mock_platform


@pytest.fixture
def sample_usage_stats() -> UsageStats:
    """Sample UsageStats instance."""
    return UsageStats(
        total_tracking_entries=10,
        total_scored_commits=5,
        tracking_start_time=datetime(2024, 1, 1, 0, 0, 0),
        most_used_file_extensions={".py": 5, ".ts": 3, ".js": 2},
        composer_sessions=2,
    )


@pytest.fixture
def empty_db_connection(tmp_path: Path):
    """Create an empty SQLite database connection."""
    db_path = tmp_path / "empty_db.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")
    cursor.execute("CREATE TABLE IF NOT EXISTS cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)")

    conn.commit()
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()
