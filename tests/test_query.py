"""Tests for query builder."""

from datetime import datetime, timedelta

import pytest

from cursordata.query import QueryBuilder


@pytest.mark.unit
class TestQueryBuilder:
    """Tests for QueryBuilder."""

    def test_init(self, mock_client):
        """Test query builder initialization."""
        builder = QueryBuilder(mock_client)
        assert builder._client == mock_client

    @pytest.mark.parametrize("query_method", [
        "bubbles",
        "composer_sessions",
        "tracking_entries",
        "checkpoints",
        "message_contexts",
        "composer_data",
    ])
    def test_query_methods(self, mock_client, query_method):
        """Test all query methods return valid query objects."""
        query_builder = mock_client.query()
        method = getattr(query_builder, query_method)
        query = method()
        assert query is not None, f"{query_method}() should return a query object"
        assert hasattr(query, "execute"), f"Query from {query_method} should have execute method"


@pytest.mark.unit
class TestBaseQuery:
    """Tests for BaseQuery methods."""

    def test_limit(self, mock_client):
        """Test setting limit."""
        query = mock_client.query().bubbles().limit(10)
        assert query._limit == 10

    @pytest.mark.parametrize("limit,expected", [
        (0, 0),
        (10, 10),
        (100, 100),
        (-1, -1),  # Negative limit accepted but may have special meaning
    ])
    def test_limit_various_values(self, mock_client, limit, expected):
        """Test setting limit with various values."""
        query = mock_client.query().bubbles().limit(limit)
        assert query._limit == expected

    def test_offset(self, mock_client):
        """Test setting offset."""
        query = mock_client.query().bubbles().offset(5)
        assert query._offset == 5

    @pytest.mark.parametrize("page,page_size,expected_offset,expected_limit", [
        (1, 10, 0, 10),      # First page
        (2, 10, 10, 10),      # Second page
        (3, 20, 40, 20),      # Third page with size 20
        (0, 10, -10, 10),     # Page 0 should result in negative offset
    ])
    def test_page_various_values(self, mock_client, page, page_size, expected_offset, expected_limit):
        """Test pagination with various values."""
        query = mock_client.query().bubbles().page(page, page_size)
        assert query._offset == expected_offset
        assert query._limit == expected_limit

    def test_page(self, mock_client):
        """Test pagination."""
        query = mock_client.query().bubbles().page(2, 10)
        assert query._offset == 10  # (2-1) * 10
        assert query._limit == 10

    def test_filter(self, mock_client):
        """Test adding filter predicate."""
        query = mock_client.query().bubbles().filter(lambda x: True)
        assert len(query._filters) == 1


@pytest.mark.unit
class TestBubbleQuery:
    """Tests for BubbleQuery."""

    def test_filter_by_bubble_id(self, mock_client):
        """Test filtering by bubble ID."""
        query = mock_client.query().bubbles().filter_by_bubble_id("bubble_001")
        assert query._bubble_id == "bubble_001"

    def test_where_created_after(self, mock_client):
        """Test where with created_after filter."""
        date = datetime.now() - timedelta(days=7)
        query = mock_client.query().bubbles().where(created_after=date)
        assert len(query._filters) > 0

    def test_where_created_before(self, mock_client):
        """Test where with created_before filter."""
        date = datetime.now()
        query = mock_client.query().bubbles().where(created_before=date)
        assert len(query._filters) > 0

    def test_where_model_name(self, mock_client):
        """Test where with model_name filter."""
        query = mock_client.query().bubbles().where(model_name="gpt-4")
        assert len(query._filters) > 0

    def test_where_token_filters(self, mock_client):
        """Test where with token filters."""
        query = mock_client.query().bubbles().where(
            min_input_tokens=100, min_output_tokens=50
        )
        assert len(query._filters) > 0

    def test_where_has_code_blocks(self, mock_client):
        """Test where with has_code_blocks filter."""
        query = mock_client.query().bubbles().where(has_code_blocks=True)
        assert len(query._filters) > 0

    def test_where_has_diffs(self, mock_client):
        """Test where with has_diffs filter."""
        query = mock_client.query().bubbles().where(has_diffs=True)
        assert len(query._filters) > 0

    def test_where_is_agentic(self, mock_client):
        """Test where with is_agentic filter."""
        query = mock_client.query().bubbles().where(is_agentic=True)
        assert len(query._filters) > 0

    def test_execute(self, mock_client):
        """Test executing bubble query."""
        results = mock_client.query().bubbles().execute()
        assert results is not None
        assert hasattr(results, "__len__")


@pytest.mark.unit
class TestComposerSessionQuery:
    """Tests for ComposerSessionQuery."""

    def test_where_file_extension(self, mock_client):
        """Test where with file_extension filter."""
        query = mock_client.query().composer_sessions().where(file_extension=".py")
        assert len(query._filters) > 0

    def test_where_min_files(self, mock_client):
        """Test where with min_files filter."""
        query = mock_client.query().composer_sessions().where(min_files=2)
        assert len(query._filters) > 0

    def test_where_max_files(self, mock_client):
        """Test where with max_files filter."""
        query = mock_client.query().composer_sessions().where(max_files=10)
        assert len(query._filters) > 0

    def test_execute(self, mock_client):
        """Test executing composer session query."""
        results = mock_client.query().composer_sessions().execute()
        assert results is not None
        assert hasattr(results, "__len__")


@pytest.mark.unit
class TestTrackingQuery:
    """Tests for TrackingQuery."""

    def test_where_source(self, mock_client):
        """Test where with source filter."""
        query = mock_client.query().tracking_entries().where(source="composer")
        assert len(query._filters) > 0

    def test_where_file_extension(self, mock_client):
        """Test where with file_extension filter."""
        query = mock_client.query().tracking_entries().where(file_extension=".py")
        assert len(query._filters) > 0

    def test_where_composer_id(self, mock_client):
        """Test where with composer_id filter."""
        query = mock_client.query().tracking_entries().where(composer_id="comp_001")
        assert len(query._filters) > 0

    def test_execute(self, mock_client):
        """Test executing tracking query."""
        results = mock_client.query().tracking_entries().execute()
        assert results is not None
        assert hasattr(results, "__len__")


@pytest.mark.unit
class TestCheckpointQuery:
    """Tests for CheckpointQuery."""

    def test_filter_by_bubble_id(self, mock_client):
        """Test filtering by bubble ID."""
        query = mock_client.query().checkpoints().filter_by_bubble_id("bubble_001")
        assert query._bubble_id == "bubble_001"

    def test_execute(self, mock_client):
        """Test executing checkpoint query."""
        results = mock_client.query().checkpoints().execute()
        assert isinstance(results, list)


@pytest.mark.unit
class TestMessageContextQuery:
    """Tests for MessageContextQuery."""

    def test_filter_by_bubble_id(self, mock_client):
        """Test filtering by bubble ID."""
        query = mock_client.query().message_contexts().filter_by_bubble_id("bubble_001")
        assert query._bubble_id == "bubble_001"

    def test_execute(self, mock_client):
        """Test executing message context query."""
        results = mock_client.query().message_contexts().execute()
        assert isinstance(results, list)


@pytest.mark.unit
class TestComposerDataQuery:
    """Tests for ComposerDataQuery."""

    def test_filter_by_composer_id(self, mock_client):
        """Test filtering by composer ID."""
        query = mock_client.query().composer_data().filter_by_composer_id("comp_001")
        assert query._composer_id == "comp_001"

    def test_execute(self, mock_client):
        """Test executing composer data query."""
        results = mock_client.query().composer_data().execute()
        assert isinstance(results, list)


@pytest.mark.unit
class TestQueryChaining:
    """Tests for query method chaining."""

    def test_chain_filters(self, mock_client):
        """Test chaining multiple filters."""
        query = (
            mock_client.query()
            .bubbles()
            .filter_by_bubble_id("bubble_001")
            .where(has_code_blocks=True)
            .limit(10)
        )
        assert query._bubble_id == "bubble_001"
        assert len(query._filters) > 0
        assert query._limit == 10

    def test_chain_pagination(self, mock_client):
        """Test chaining pagination."""
        query = mock_client.query().composer_sessions().page(2, 20).where(file_extension=".py")
        assert query._offset == 20
        assert query._limit == 20
        assert len(query._filters) > 0

