"""Tests for data models."""

from datetime import datetime

import pytest

from cursordata.models import (
    AICodeTrackingEntry,
    ComposerSession,
    DatabaseInfo,
    DatabaseLocation,
    ItemTableKey,
    UsageStats,
)


@pytest.mark.unit
class TestAICodeTrackingEntry:
    """Tests for AICodeTrackingEntry model."""

    def test_from_dict(self, sample_tracking_entry_data):
        """Test creating entry from dictionary."""
        entry = AICodeTrackingEntry.from_dict(sample_tracking_entry_data)
        assert entry.hash == "abc123"
        assert entry.metadata["source"] == "composer"
        assert entry.metadata["composerId"] == "comp_001"

    def test_properties(self, sample_tracking_entry):
        """Test entry properties."""
        assert sample_tracking_entry.source == "composer"
        assert sample_tracking_entry.composer_id == "comp_001"
        assert sample_tracking_entry.file_extension == ".py"
        assert sample_tracking_entry.file_name == "/path/to/file.py"

    def test_missing_metadata_fields(self):
        """Test entry with missing metadata fields."""
        entry = AICodeTrackingEntry(hash="test", metadata={})
        assert entry.source is None
        assert entry.composer_id is None
        assert entry.file_extension is None
        assert entry.file_name is None

    def test_partial_metadata(self):
        """Test entry with partial metadata."""
        entry = AICodeTrackingEntry(
            hash="test",
            metadata={"source": "chat"},
        )
        assert entry.source == "chat"
        assert entry.composer_id is None
        assert entry.file_extension is None

    def test_from_dict_with_empty_metadata(self):
        """Test from_dict with empty metadata."""
        data = {"hash": "test"}
        entry = AICodeTrackingEntry.from_dict(data)
        assert entry.hash == "test"
        assert entry.metadata == {}


@pytest.mark.unit
class TestUsageStats:
    """Tests for UsageStats model."""

    def test_default_values(self):
        """Test UsageStats with default values."""
        stats = UsageStats()
        assert stats.total_tracking_entries == 0
        assert stats.total_scored_commits == 0
        assert stats.tracking_start_time is None
        assert stats.most_used_file_extensions == {}
        assert stats.composer_sessions == 0

    def test_populated_stats(self, sample_usage_stats):
        """Test UsageStats with populated data."""
        assert sample_usage_stats.total_tracking_entries == 10
        assert sample_usage_stats.total_scored_commits == 5
        assert sample_usage_stats.tracking_start_time == datetime(2024, 1, 1, 0, 0, 0)
        assert sample_usage_stats.most_used_file_extensions == {".py": 5, ".ts": 3, ".js": 2}
        assert sample_usage_stats.composer_sessions == 2


@pytest.mark.unit
class TestComposerSession:
    """Tests for ComposerSession model."""

    def test_from_entries(self, sample_tracking_entries):
        """Test creating session from entries."""
        entries_001 = [e for e in sample_tracking_entries if e.composer_id == "comp_001"]
        session = ComposerSession.from_entries("comp_001", entries_001)
        
        assert session.composer_id == "comp_001"
        assert session.entries_count == 2
        assert len(session.files_modified) == 2
        assert ".py" in session.file_extensions

    def test_from_entries_empty(self):
        """Test creating session from empty entries."""
        session = ComposerSession.from_entries("comp_001", [])
        assert session.composer_id == "comp_001"
        assert session.entries_count == 0
        assert session.files_modified == []
        assert session.file_extensions == []

    def test_from_entries_deduplicates_files(self):
        """Test that from_entries deduplicates files."""
        entries = [
            AICodeTrackingEntry(
                hash="h1",
                metadata={
                    "composerId": "comp_001",
                    "fileName": "/path/to/file.py",
                    "fileExtension": ".py",
                },
            ),
            AICodeTrackingEntry(
                hash="h2",
                metadata={
                    "composerId": "comp_001",
                    "fileName": "/path/to/file.py",  # Same file
                    "fileExtension": ".py",
                },
            ),
        ]
        
        session = ComposerSession.from_entries("comp_001", entries)
        assert len(session.files_modified) == 1
        assert session.files_modified[0] == "/path/to/file.py"

    def test_from_entries_deduplicates_extensions(self):
        """Test that from_entries deduplicates extensions."""
        entries = [
            AICodeTrackingEntry(
                hash="h1",
                metadata={
                    "composerId": "comp_001",
                    "fileName": "/path/to/file1.py",
                    "fileExtension": ".py",
                },
            ),
            AICodeTrackingEntry(
                hash="h2",
                metadata={
                    "composerId": "comp_001",
                    "fileName": "/path/to/file2.py",
                    "fileExtension": ".py",  # Same extension
                },
            ),
        ]
        
        session = ComposerSession.from_entries("comp_001", entries)
        assert len(session.file_extensions) == 1
        assert ".py" in session.file_extensions


@pytest.mark.unit
class TestDatabaseLocation:
    """Tests for DatabaseLocation enum."""

    def test_enum_values(self):
        """Test enum has expected values."""
        assert DatabaseLocation.MACOS.value.endswith("state.vscdb")
        assert DatabaseLocation.WINDOWS.value.endswith("state.vscdb")
        assert DatabaseLocation.LINUX.value.endswith("state.vscdb")

    def test_enum_membership(self):
        """Test enum membership."""
        assert isinstance(DatabaseLocation.MACOS, DatabaseLocation)
        assert isinstance(DatabaseLocation.WINDOWS, DatabaseLocation)
        assert isinstance(DatabaseLocation.LINUX, DatabaseLocation)


@pytest.mark.unit
class TestItemTableKey:
    """Tests for ItemTableKey enum."""

    def test_ai_code_tracking_keys(self):
        """Test AI code tracking keys."""
        assert ItemTableKey.AI_CODE_TRACKING_LINES.value == "aiCodeTrackingLines"
        assert ItemTableKey.AI_CODE_TRACKING_SCORED_COMMITS.value == "aiCodeTrackingScoredCommits"
        assert ItemTableKey.AI_CODE_TRACKING_START_TIME.value == "aiCodeTrackingStartTime"

    def test_composer_keys(self):
        """Test composer keys."""
        assert ItemTableKey.COMPOSER_HAS_REOPENED_ONCE.value == "composer.hasReopenedOnce"

    def test_all_keys_are_strings(self):
        """Test that all enum values are strings."""
        for key in ItemTableKey:
            assert isinstance(key.value, str)


@pytest.mark.unit
class TestDatabaseInfo:
    """Tests for DatabaseInfo model."""

    def test_default_values(self, tmp_path):
        """Test DatabaseInfo with default values."""
        db_path = tmp_path / "test.db"
        info = DatabaseInfo(path=db_path)
        assert info.path == db_path
        assert info.item_table_count == 0
        assert info.cursor_disk_kv_count == 0
        assert info.last_modified is None

    def test_populated_info(self, tmp_path):
        """Test DatabaseInfo with populated data."""
        db_path = tmp_path / "test.db"
        last_modified = datetime(2024, 1, 1, 0, 0, 0)
        info = DatabaseInfo(
            path=db_path,
            item_table_count=100,
            cursor_disk_kv_count=50,
            last_modified=last_modified,
        )
        assert info.path == db_path
        assert info.item_table_count == 100
        assert info.cursor_disk_kv_count == 50
        assert info.last_modified == last_modified

