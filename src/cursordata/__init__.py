"""CursorData SDK - A Python SDK for interacting with Cursor editor's local SQLite database.

This SDK provides strongly-typed interfaces for accessing and analyzing Cursor usage data
stored locally on your computer.
"""

from cursordata.client import CursorDataClient
from cursordata.models import (
    AICodeTrackingEntry,
    ComposerSession,
    DatabaseLocation,
    ItemTableKey,
    UsageStats,
)
from cursordata.cursordiskkv_models import (
    BubbleConversation,
    MessageRequestContext,
    Checkpoint,
    CodeBlockDiff,
    ComposerData,
    InlineDiffs,
)
from cursordata.collections import (
    Collection,
    BubbleCollection,
    ComposerSessionCollection,
    AICodeTrackingCollection,
)
from cursordata.query import QueryBuilder
from cursordata.model_groups import (
    CodeGroup,
    ContextGroup,
    MetadataGroup,
    LintingGroup,
    VersionControlGroup,
    ToolGroup,
)

__version__ = "0.1.0"

__all__ = [
    "CursorDataClient",
    "QueryBuilder",
    "AICodeTrackingEntry",
    "BubbleConversation",
    "ComposerSession",
    "DatabaseLocation",
    "ItemTableKey",
    "UsageStats",
    "MessageRequestContext",
    "Checkpoint",
    "CodeBlockDiff",
    "ComposerData",
    "InlineDiffs",
    "Collection",
    "BubbleCollection",
    "ComposerSessionCollection",
    "AICodeTrackingCollection",
    "CodeGroup",
    "ContextGroup",
    "MetadataGroup",
    "LintingGroup",
    "VersionControlGroup",
    "ToolGroup",
]

