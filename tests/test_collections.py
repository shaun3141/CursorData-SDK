"""Tests for collection classes."""

import pytest

from cursordata.collections import (
    AICodeTrackingCollection,
    BubbleCollection,
    Collection,
    ComposerSessionCollection,
)
from cursordata.models import AICodeTrackingEntry, ComposerSession


@pytest.mark.unit
class TestCollection:
    """Tests for base Collection class."""

    def test_init(self):
        """Test collection initialization."""
        items = [1, 2, 3]
        collection = Collection(items)
        assert len(collection) == 3
        assert collection.items == items

    def test_len(self):
        """Test collection length."""
        collection = Collection([1, 2, 3])
        assert len(collection) == 3
        assert len(Collection([])) == 0

    def test_iteration(self):
        """Test collection iteration."""
        items = [1, 2, 3]
        collection = Collection(items)
        assert list(collection) == items

    def test_indexing(self):
        """Test collection indexing."""
        items = [1, 2, 3]
        collection = Collection(items)
        assert collection[0] == 1
        assert collection[1] == 2
        assert collection[2] == 3

    def test_filter(self):
        """Test collection filtering."""
        collection = Collection([1, 2, 3, 4, 5])
        filtered = collection.filter(lambda x: x % 2 == 0)
        assert len(filtered) == 2
        assert filtered.items == [2, 4]
        assert isinstance(filtered, Collection)

    def test_sort(self):
        """Test collection sorting."""
        collection = Collection([3, 1, 4, 2])
        sorted_collection = collection.sort()
        assert sorted_collection.items == [1, 2, 3, 4]
        
        reverse_sorted = collection.sort(reverse=True)
        assert reverse_sorted.items == [4, 3, 2, 1]

    def test_sort_with_key(self):
        """Test collection sorting with key function."""
        collection = Collection([(1, 3), (2, 1), (3, 2)])
        sorted_collection = collection.sort(key=lambda x: x[1])
        assert sorted_collection.items == [(2, 1), (3, 2), (1, 3)]

    def test_map(self):
        """Test collection mapping."""
        collection = Collection([1, 2, 3])
        mapped = collection.map(lambda x: x * 2)
        assert mapped == [2, 4, 6]

    def test_group_by(self):
        """Test collection grouping."""
        collection = Collection([1, 2, 3, 4, 5])
        groups = collection.group_by(lambda x: "even" if x % 2 == 0 else "odd")
        assert "even" in groups
        assert "odd" in groups
        assert len(groups["even"]) == 2
        assert len(groups["odd"]) == 3
        assert all(isinstance(g, Collection) for g in groups.values())

    def test_take(self):
        """Test taking first n items."""
        collection = Collection([1, 2, 3, 4, 5])
        taken = collection.take(3)
        assert len(taken) == 3
        assert taken.items == [1, 2, 3]

    def test_skip(self):
        """Test skipping first n items."""
        collection = Collection([1, 2, 3, 4, 5])
        skipped = collection.skip(2)
        assert len(skipped) == 3
        assert skipped.items == [3, 4, 5]

    def test_first(self):
        """Test getting first item."""
        collection = Collection([1, 2, 3])
        assert collection.first() == 1
        assert Collection([]).first() is None

    def test_last(self):
        """Test getting last item."""
        collection = Collection([1, 2, 3])
        assert collection.last() == 3
        assert Collection([]).last() is None

    def test_any(self):
        """Test any predicate check."""
        collection = Collection([1, 2, 3])
        assert collection.any(lambda x: x > 2) is True
        assert collection.any(lambda x: x > 10) is False
        assert collection.any() is True  # Non-empty
        assert Collection([]).any() is False  # Empty

    def test_all(self):
        """Test all predicate check."""
        collection = Collection([2, 4, 6])
        assert collection.all(lambda x: x % 2 == 0) is True
        assert collection.all(lambda x: x > 3) is False

    def test_to_list(self):
        """Test converting to list."""
        items = [1, 2, 3]
        collection = Collection(items)
        result = collection.to_list()
        assert result == items
        assert result is not items  # Should be a copy


@pytest.mark.unit
class TestAICodeTrackingCollection:
    """Tests for AICodeTrackingCollection."""

    def test_filter_by_source(self, sample_tracking_entries):
        """Test filtering by source."""
        collection = AICodeTrackingCollection(sample_tracking_entries)
        filtered = collection.filter_by_source("composer")
        assert len(filtered) == 3
        assert all(e.source == "composer" for e in filtered)

    def test_filter_by_extension(self, sample_tracking_entries):
        """Test filtering by extension."""
        collection = AICodeTrackingCollection(sample_tracking_entries)
        filtered = collection.filter_by_extension(".py")
        assert len(filtered) == 2
        assert all(e.file_extension == ".py" for e in filtered)

    def test_filter_by_composer_id(self, sample_tracking_entries):
        """Test filtering by composer ID."""
        collection = AICodeTrackingCollection(sample_tracking_entries)
        filtered = collection.filter_by_composer_id("comp_001")
        assert len(filtered) == 2
        assert all(e.composer_id == "comp_001" for e in filtered)

    def test_group_by_source(self, sample_tracking_entries):
        """Test grouping by source."""
        collection = AICodeTrackingCollection(sample_tracking_entries)
        groups = collection.group_by_source()
        assert "composer" in groups
        assert "chat" in groups
        assert len(groups["composer"]) == 3
        assert len(groups["chat"]) == 1

    def test_group_by_extension(self, sample_tracking_entries):
        """Test grouping by extension."""
        collection = AICodeTrackingCollection(sample_tracking_entries)
        groups = collection.group_by_extension()
        assert ".py" in groups
        assert ".ts" in groups
        assert ".js" in groups


@pytest.mark.unit
class TestComposerSessionCollection:
    """Tests for ComposerSessionCollection."""

    def test_filter_by_extension(self, sample_tracking_entries):
        """Test filtering by extension."""
        sessions = [
            ComposerSession.from_entries("comp_001", [sample_tracking_entries[0], sample_tracking_entries[1]]),
            ComposerSession.from_entries("comp_002", [sample_tracking_entries[2]]),
        ]
        collection = ComposerSessionCollection(sessions)
        filtered = collection.filter_by_extension(".py")
        assert len(filtered) == 1
        assert filtered[0].composer_id == "comp_001"

    def test_filter_by_file_count(self, sample_tracking_entries):
        """Test filtering by file count."""
        sessions = [
            ComposerSession.from_entries("comp_001", sample_tracking_entries[:2]),
            ComposerSession.from_entries("comp_002", [sample_tracking_entries[2]]),
        ]
        collection = ComposerSessionCollection(sessions)
        filtered = collection.filter_by_file_count(min_files=2)
        assert len(filtered) == 1
        assert filtered[0].composer_id == "comp_001"

    def test_group_by_extension(self, sample_tracking_entries):
        """Test grouping by extension."""
        sessions = [
            ComposerSession.from_entries("comp_001", sample_tracking_entries[:2]),
            ComposerSession.from_entries("comp_002", [sample_tracking_entries[2]]),
        ]
        collection = ComposerSessionCollection(sessions)
        groups = collection.group_by_extension()
        assert ".py" in groups
        assert ".ts" in groups
        assert len(groups[".py"]) == 1
        assert len(groups[".ts"]) == 1


@pytest.mark.unit
class TestBubbleCollection:
    """Tests for BubbleCollection."""

    def test_filter_by_date_range(self, sample_bubble_conversation):
        """Test filtering by date range."""
        from datetime import datetime, timedelta
        
        collection = BubbleCollection([sample_bubble_conversation])
        start = datetime(2023, 12, 1)
        end = datetime(2024, 12, 31)
        filtered = collection.filter_by_date_range(start, end)
        assert len(filtered) == 1
        
        future_start = datetime(2025, 1, 1)
        filtered_future = collection.filter_by_date_range(future_start)
        assert len(filtered_future) == 0

    def test_filter_by_model(self, sample_bubble_conversation):
        """Test filtering by model."""
        collection = BubbleCollection([sample_bubble_conversation])
        filtered = collection.filter_by_model("gpt-4")
        assert len(filtered) == 1
        
        filtered_wrong = collection.filter_by_model("gpt-3.5")
        assert len(filtered_wrong) == 0

    def test_filter_by_token_count(self, sample_bubble_conversation):
        """Test filtering by token count."""
        collection = BubbleCollection([sample_bubble_conversation])
        filtered = collection.filter_by_token_count(min_input=50, min_output=25)
        assert len(filtered) == 1
        
        filtered_high = collection.filter_by_token_count(min_input=200)
        assert len(filtered_high) == 0

    def test_with_code_blocks(self, sample_bubble_conversation):
        """Test filtering bubbles with code blocks."""
        collection = BubbleCollection([sample_bubble_conversation])
        filtered = collection.with_code_blocks()
        assert len(filtered) == 1

    def test_with_diffs(self, sample_bubble_conversation):
        """Test filtering bubbles with diffs."""
        collection = BubbleCollection([sample_bubble_conversation])
        filtered = collection.with_diffs()
        # Sample bubble has empty diff lists, so should return 0
        assert len(filtered) == 0

    def test_group_by_date(self, sample_bubble_conversation):
        """Test grouping by date."""
        collection = BubbleCollection([sample_bubble_conversation])
        groups = collection.group_by_date()
        assert len(groups) == 1
        assert "2024-01-01" in groups

    def test_group_by_model(self, sample_bubble_conversation):
        """Test grouping by model."""
        collection = BubbleCollection([sample_bubble_conversation])
        groups = collection.group_by_model()
        assert "gpt-4" in groups
        assert len(groups["gpt-4"]) == 1

