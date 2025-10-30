"""Integration tests for end-to-end functionality."""

import json

import pytest

from cursordata.client import CursorDataClient
from cursordata.collections import AICodeTrackingCollection, BubbleCollection
from cursordata.models import ItemTableKey
from tests.factories import (
    BubbleConversationFactory,
    TrackingEntryFactory,
)


@pytest.mark.integration
class TestFullQueryFlow:
    """Test complete query flow with real database."""

    def test_bubble_query_end_to_end(self, tmp_path):
        """Test complete bubble query flow."""
        # Setup database
        db_path = tmp_path / "integration_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Insert test data
        conn = client._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)")

        bubbles = BubbleConversationFactory.create_batch(5)
        for i, bubble in enumerate(bubbles):
            key = f"bubbleId:bubble_{i:03d}:conv_{i:03d}"
            # Convert bubble to dict format expected by database
            bubble_dict = {
                "_v": bubble._v,
                "type": bubble.type,
                "bubbleId": bubble.bubble_id or f"bubble_{i:03d}",
                "requestId": bubble.request_id or f"req_{i:03d}",
                "createdAt": bubble.created_at or "",
                "modelName": bubble.model_name or "gpt-4",
                "inputTokens": bubble.input_tokens or 0,
                "outputTokens": bubble.output_tokens or 0,
                "isAgentic": bubble.is_agentic,
            }
            value = json.dumps(bubble_dict)
            cursor.execute("INSERT INTO cursorDiskKV (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

        # Execute query
        results = client.query().bubbles().limit(10).execute()

        # Verify results
        assert results is not None
        assert isinstance(results, BubbleCollection)
        assert len(results) == 5
        assert all(hasattr(r, "bubble_id") for r in results)

        client.close()

    def test_tracking_entries_query_end_to_end(self, tmp_path):
        """Test complete tracking entries query flow."""
        # Setup database
        db_path = tmp_path / "integration_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Insert test data
        conn = client._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")

        entries = TrackingEntryFactory.create_batch(3)
        tracking_data = [{"hash": e.hash, "metadata": e.metadata} for e in entries]
        cursor.execute(
            "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
            (ItemTableKey.AI_CODE_TRACKING_LINES.value, json.dumps(tracking_data).encode("utf-8")),
        )
        conn.commit()

        # Execute query
        results = client.query().tracking_entries().execute()

        # Verify results
        assert results is not None
        assert isinstance(results, AICodeTrackingCollection)
        assert len(results) == 3

        client.close()

    def test_query_with_filters_end_to_end(self, tmp_path):
        """Test query with filters applied."""
        # Setup database
        db_path = tmp_path / "integration_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Insert test data
        conn = client._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)")

        # Create bubbles with different model names
        bubble1_dict = {
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
        bubble2_dict = {
            "_v": 1,
            "type": 1,
            "bubbleId": "bubble_002",
            "requestId": "req_002",
            "createdAt": "2024-01-01T00:00:00Z",
            "modelName": "gpt-3.5",
            "inputTokens": 80,
            "outputTokens": 40,
            "isAgentic": False,
        }

        for bubble_dict in [bubble1_dict, bubble2_dict]:
            key = f"bubbleId:{bubble_dict['bubbleId']}:conv_001"
            value = json.dumps(bubble_dict)
            cursor.execute("INSERT INTO cursorDiskKV (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

        # Query with filter
        results = client.query().bubbles().where(model_name="gpt-4").execute()

        # Verify filtered results
        assert len(results) == 1
        assert results[0].model_name == "gpt-4"

        client.close()

    def test_query_chaining_end_to_end(self, tmp_path):
        """Test query method chaining."""
        # Setup database
        db_path = tmp_path / "integration_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Insert test data
        conn = client._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cursorDiskKV (key TEXT PRIMARY KEY, value TEXT)")

        for i in range(10):
            bubble_dict = {
                "_v": 1,
                "type": 1,
                "bubbleId": f"bubble_{i:03d}",
                "requestId": f"req_{i:03d}",
                "createdAt": "2024-01-01T00:00:00Z",
                "modelName": "gpt-4",
                "inputTokens": 100,
                "outputTokens": 50,
                "isAgentic": False,
            }
            key = f"bubbleId:bubble_{i:03d}:conv_{i:03d}"
            value = json.dumps(bubble_dict)
            cursor.execute("INSERT INTO cursorDiskKV (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

        # Execute chained query
        results = (
            client.query()
            .bubbles()
            .limit(5)
            .offset(2)
            .filter(lambda x: True)  # Filter all through
            .execute()
        )

        # Verify results
        assert len(results) <= 5  # Limit applied
        assert isinstance(results, BubbleCollection)

        client.close()


@pytest.mark.integration
class TestCollectionOperations:
    """Test collection operations with real data."""

    def test_collection_filtering(self, tmp_path):
        """Test filtering collections."""
        # Setup database
        db_path = tmp_path / "integration_test.db"
        db_path.touch()
        client = CursorDataClient(db_path=str(db_path))

        # Insert test data
        entries = TrackingEntryFactory.create_batch(
            5, metadata={"source": "composer", "fileExtension": ".py"}
        )
        entries.extend(
            TrackingEntryFactory.create_batch(
                3, metadata={"source": "chat", "fileExtension": ".ts"}
            )
        )

        conn = client._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")

        tracking_data = [{"hash": e.hash, "metadata": e.metadata} for e in entries]
        cursor.execute(
            "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
            (ItemTableKey.AI_CODE_TRACKING_LINES.value, json.dumps(tracking_data).encode("utf-8")),
        )
        conn.commit()

        # Query and filter
        results = client.query().tracking_entries().execute()
        filtered = results.filter_by_source("composer")

        assert len(filtered) == 5
        assert all(e.source == "composer" for e in filtered)

        client.close()
