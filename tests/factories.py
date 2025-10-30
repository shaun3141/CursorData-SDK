"""Test data factories for creating test objects."""

from datetime import datetime
from typing import Optional

from cursordata.cursordiskkv_models import BubbleConversation
from cursordata.models import AICodeTrackingEntry, ComposerSession


class TrackingEntryFactory:
    """Factory for creating AICodeTrackingEntry test objects."""

    @staticmethod
    def create(**kwargs) -> AICodeTrackingEntry:
        """Create a tracking entry with default or custom values."""
        defaults = {
            "hash": "test_hash_001",
            "metadata": {
                "source": "composer",
                "composerId": "comp_001",
                "fileExtension": ".py",
                "fileName": "/path/to/test_file.py",
            },
        }
        defaults["metadata"].update(kwargs.pop("metadata", {}))
        defaults.update(kwargs)
        return AICodeTrackingEntry.from_dict(defaults)

    @staticmethod
    def create_batch(count: int, **kwargs) -> list[AICodeTrackingEntry]:
        """Create multiple tracking entries."""
        entries = []
        base_metadata = kwargs.pop("metadata", {})
        for i in range(count):
            metadata = {
                **base_metadata,
                "composerId": f"comp_{i:03d}",
                "fileName": f"/path/to/file_{i}.py",
            }
            entries.append(TrackingEntryFactory.create(hash=f"hash_{i:03d}", metadata=metadata))
        return entries


class ComposerSessionFactory:
    """Factory for creating ComposerSession test objects."""

    @staticmethod
    def create(composer_id: str = "comp_001", entries: Optional[list[AICodeTrackingEntry]] = None, **kwargs) -> ComposerSession:
        """Create a composer session with default or custom values."""
        if entries is None:
            entries = TrackingEntryFactory.create_batch(2, metadata={"composerId": composer_id})
        return ComposerSession.from_entries(composer_id, entries)


class BubbleConversationFactory:
    """Factory for creating BubbleConversation test objects."""

    @staticmethod
    def create(**kwargs) -> BubbleConversation:
        """Create a bubble conversation with default or custom values."""
        defaults = {
            "_v": 1,
            "type": 1,
            "bubbleId": "bubble_001",
            "requestId": "req_001",
            "checkpointId": "checkpoint_001",
            "text": "Test conversation",
            "richText": "<p>Test conversation</p>",
            "createdAt": datetime.now().isoformat() + "Z",
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
        defaults.update(kwargs)
        return BubbleConversation.from_dict(defaults, bubble_id=defaults["bubbleId"])

    @staticmethod
    def create_batch(count: int, **kwargs) -> list[BubbleConversation]:
        """Create multiple bubble conversations."""
        bubbles = []
        for i in range(count):
            bubble_data = {
                "bubbleId": f"bubble_{i:03d}",
                "requestId": f"req_{i:03d}",
                "createdAt": (datetime.now().replace(microsecond=0).isoformat() + "Z"),
                **kwargs,
            }
            bubbles.append(BubbleConversationFactory.create(**bubble_data))
        return bubbles

