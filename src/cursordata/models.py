"""Data models and type definitions for Cursor database entities."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class DatabaseLocation(str, Enum):
    """Platform-specific database locations."""

    MACOS = "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
    WINDOWS = "%APPDATA%\\Cursor\\User\\globalStorage\\state.vscdb"
    LINUX = "~/.config/Cursor/User/globalStorage/state.vscdb"


class ItemTableKey(str, Enum):
    """Known keys in the ItemTable."""

    # AI Code Tracking
    AI_CODE_TRACKING_LINES = "aiCodeTrackingLines"
    AI_CODE_TRACKING_SCORED_COMMITS = "aiCodeTrackingScoredCommits"
    AI_CODE_TRACKING_START_TIME = "aiCodeTrackingStartTime"

    # Composer
    COMPOSER_HAS_REOPENED_ONCE = "composer.hasReopenedOnce"
    BACKGROUND_COMPOSER_WINDOW_BC_MAPPING = "backgroundComposer.windowBcMapping"

    # Chat
    CHAT_WORKSPACE_TRANSFER = "chat.workspaceTransfer"

    # Feature Status
    CURSOR_FEATURE_STATUS_DATA_PRIVACY_ONBOARDING = "cursor.featureStatus.dataPrivacyOnboarding"
    CURSORAI_FEATURE_STATUS_CACHE = "cursorai/featureStatusCache"

    # Settings
    ADMIN_SETTINGS_CACHED = "adminSettings.cached"
    AI_PANE_TOOLTIP_SHOW_COUNT = "aiPane.tooltipShowCount"
    AI_CONTEXT_PERSONAL_CONTEXT = "aicontext.personalContext"

    # Workspace
    WORKBENCH_BACKGROUND_COMPOSER_PERSISTENT_DATA = "workbench.backgroundComposer.persistentData"


@dataclass
class AICodeTrackingEntry:
    """Represents a single AI code tracking entry.

    The metadata dictionary contains additional information including:
    - source: Where the code came from (e.g., "composer")
    - composerId: ID of the composer session that generated this code
    - fileExtension: File extension of the modified file
    - fileName: Full path to the modified file
    """

    hash: str
    metadata: dict[str, Any]

    @property
    def source(self) -> Optional[str]:
        """Get the source of the code entry."""
        return self.metadata.get("source")

    @property
    def composer_id(self) -> Optional[str]:
        """Get the composer session ID."""
        return self.metadata.get("composerId")

    @property
    def file_extension(self) -> Optional[str]:
        """Get the file extension."""
        return self.metadata.get("fileExtension")

    @property
    def file_name(self) -> Optional[str]:
        """Get the full file path."""
        return self.metadata.get("fileName")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AICodeTrackingEntry":
        """Create an instance from a dictionary."""
        return cls(hash=data["hash"], metadata=data.get("metadata", {}))


@dataclass
class UsageStats:
    """Aggregated usage statistics for Cursor AI code tracking."""

    total_tracking_entries: int = 0
    total_scored_commits: int = 0
    tracking_start_time: Optional[datetime] = None
    most_used_file_extensions: dict[str, int] = field(default_factory=dict)
    composer_sessions: int = 0


@dataclass
class ComposerSession:
    """Represents a composer session with associated files and entries."""

    composer_id: str
    files_modified: list[str] = field(default_factory=list)
    file_extensions: list[str] = field(default_factory=list)
    entries_count: int = 0

    @classmethod
    def from_entries(
        cls, composer_id: str, entries: list[AICodeTrackingEntry]
    ) -> "ComposerSession":
        """Create a ComposerSession from a list of tracking entries."""
        files = list(set(e.file_name for e in entries if e.file_name))
        extensions = list(set(e.file_extension for e in entries if e.file_extension))
        return cls(
            composer_id=composer_id,
            files_modified=files,
            file_extensions=extensions,
            entries_count=len(entries),
        )


# BubbleConversation has been moved to cursordiskkv_models.py
# Import it from there for backwards compatibility


@dataclass
class DatabaseInfo:
    """Information about the Cursor database file and its contents."""

    path: Path
    item_table_count: int = 0
    cursor_disk_kv_count: int = 0
    last_modified: Optional[datetime] = None
