"""Collection wrappers for SDK data types.

Provides typed collections with helper methods for filtering, sorting, and grouping.
"""

from collections.abc import Iterator
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from cursordata.cursordiskkv_models import BubbleConversation
    from cursordata.models import AICodeTrackingEntry, ComposerSession

T = TypeVar("T")
U = TypeVar("U")


class Collection(Generic[T]):
    """Base collection class with common operations."""

    def __init__(self, items: list[T]):
        """Initialize collection with items."""
        self._items = items

    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        """Iterate over items in the collection."""
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        """Get item by index."""
        return self._items[index]

    def __repr__(self) -> str:
        """String representation of the collection."""
        return f"{self.__class__.__name__}({len(self._items)} items)"

    @property
    def items(self) -> list[T]:
        """Get the underlying list of items."""
        return self._items

    def filter(self, predicate: Callable[[T], bool]) -> "Collection[T]":
        """Filter items using a predicate function.

        Args:
            predicate: Function that returns True for items to keep.

        Returns:
            New collection with filtered items.
        """
        return self.__class__([item for item in self._items if predicate(item)])

    def sort(
        self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False
    ) -> "Collection[T]":
        """Sort items in the collection.

        Args:
            key: Optional key function for sorting.
            reverse: If True, sort in reverse order.

        Returns:
            New sorted collection.
        """
        items = sorted(self._items, key=key, reverse=reverse)
        return self.__class__(items)

    def map(self, func: Callable[[T], U]) -> list[U]:
        """Map items using a function.

        Args:
            func: Function to apply to each item.

        Returns:
            List of transformed items.
        """
        return [func(item) for item in self._items]

    def group_by(self, key_func: Callable[[T], str]) -> dict[str, "Collection[T]"]:
        """Group items by a key function.

        Args:
            key_func: Function that returns a key for each item.

        Returns:
            Dictionary mapping keys to collections of items.
        """
        groups: dict[str, list[T]] = {}
        for item in self._items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)

        return {k: self.__class__(v) for k, v in groups.items()}

    def take(self, n: int) -> "Collection[T]":
        """Take first n items.

        Args:
            n: Number of items to take.

        Returns:
            New collection with first n items.
        """
        return self.__class__(self._items[:n])

    def skip(self, n: int) -> "Collection[T]":
        """Skip first n items.

        Args:
            n: Number of items to skip.

        Returns:
            New collection with items after skipping n.
        """
        return self.__class__(self._items[n:])

    def first(self) -> Optional[T]:
        """Get the first item, or None if collection is empty."""
        return self._items[0] if self._items else None

    def last(self) -> Optional[T]:
        """Get the last item, or None if collection is empty."""
        return self._items[-1] if self._items else None

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """Check if any item matches the predicate.

        Args:
            predicate: Optional predicate function. If None, checks if collection is non-empty.

        Returns:
            True if any item matches.
        """
        if predicate is None:
            return len(self._items) > 0
        return any(predicate(item) for item in self._items)

    def all(self, predicate: Callable[[T], bool]) -> bool:
        """Check if all items match the predicate.

        Args:
            predicate: Predicate function.

        Returns:
            True if all items match.
        """
        return all(predicate(item) for item in self._items)

    def to_list(self) -> list[T]:
        """Convert collection to a plain list."""
        return self._items.copy()


class BubbleCollection(Collection["BubbleConversation"]):
    """Collection of BubbleConversation objects with domain-specific methods."""

    def filter_by_date_range(
        self, start: Optional[datetime] = None, end: Optional[datetime] = None
    ) -> "BubbleCollection":
        """Filter bubbles by creation date range.

        Args:
            start: Start date (inclusive).
            end: End date (inclusive).

        Returns:
            Filtered collection.
        """

        def predicate(conv: "BubbleConversation") -> bool:
            if not conv.created_at:
                return False

            try:
                from dateutil.parser import parse as parse_date

                created = parse_date(conv.created_at)

                # Handle timezone-aware vs naive datetime comparison
                if start:
                    start_naive = start.replace(tzinfo=None) if start.tzinfo else start
                    created_naive = created.replace(tzinfo=None) if created.tzinfo else created
                    if created_naive < start_naive:
                        return False
                if end:
                    end_naive = end.replace(tzinfo=None) if end.tzinfo else end
                    created_naive = created.replace(tzinfo=None) if created.tzinfo else created
                    if created_naive > end_naive:
                        return False
            except Exception:
                return False

            return True

        return self.filter(predicate)

    def filter_by_model(self, model_name: str) -> "BubbleCollection":
        """Filter bubbles by model name.

        Args:
            model_name: Name of the model to filter by.

        Returns:
            Filtered collection.
        """

        return self.filter(lambda conv: conv.model_name == model_name)

    def filter_by_token_count(
        self, min_input: Optional[int] = None, min_output: Optional[int] = None
    ) -> "BubbleCollection":
        """Filter bubbles by token counts.

        Args:
            min_input: Minimum input tokens.
            min_output: Minimum output tokens.

        Returns:
            Filtered collection.
        """

        def predicate(conv: "BubbleConversation") -> bool:
            if min_input is not None and (conv.input_tokens or 0) < min_input:
                return False
            if min_output is not None and (conv.output_tokens or 0) < min_output:
                return False
            return True

        return self.filter(predicate)

    def with_code_blocks(self) -> "BubbleCollection":
        """Filter bubbles that have suggested code blocks."""
        return self.filter(lambda conv: len(conv.suggested_code_blocks) > 0)

    def with_diffs(self) -> "BubbleCollection":
        """Filter bubbles that have diffs."""
        return self.filter(
            lambda conv: len(conv.assistant_suggested_diffs) > 0
            or len(conv.diffs_since_last_apply) > 0
        )

    def with_lint_errors(self) -> "BubbleCollection":
        """Filter bubbles that have lint errors."""
        return self.filter(
            lambda conv: len(conv.lints) > 0 or len(conv.multi_file_linter_errors) > 0
        )

    def agentic_only(self) -> "BubbleCollection":
        """Filter for agentic conversations only."""
        return self.filter(lambda conv: conv.is_agentic)

    def group_by_date(self) -> dict[str, "BubbleCollection"]:
        """Group bubbles by date (YYYY-MM-DD).

        Returns:
            Dictionary mapping dates to collections of bubbles.
        """

        def key_func(conv: "BubbleConversation") -> str:
            if not conv.created_at:
                return "unknown"
            try:
                from dateutil.parser import parse as parse_date

                created = parse_date(conv.created_at)
                return created.strftime("%Y-%m-%d")
            except Exception:
                return "unknown"

        return self.group_by(key_func)

    def group_by_model(self) -> dict[str, "BubbleCollection"]:
        """Group bubbles by model name.

        Returns:
            Dictionary mapping model names to collections of bubbles.
        """

        def key_func(conv: "BubbleConversation") -> str:
            return conv.model_name or "unknown"

        return self.group_by(key_func)


class ComposerSessionCollection(Collection["ComposerSession"]):
    """Collection of ComposerSession objects with domain-specific methods."""

    def filter_by_extension(self, extension: str) -> "ComposerSessionCollection":
        """Filter sessions by file extension.

        Args:
            extension: File extension to filter by (e.g., '.py').

        Returns:
            Filtered collection.
        """
        return self.filter(lambda session: extension in session.file_extensions)

    def filter_by_file_count(
        self, min_files: Optional[int] = None, max_files: Optional[int] = None
    ) -> "ComposerSessionCollection":
        """Filter sessions by number of files modified.

        Args:
            min_files: Minimum number of files.
            max_files: Maximum number of files.

        Returns:
            Filtered collection.
        """

        def predicate(session: "ComposerSession") -> bool:
            file_count = len(session.files_modified)
            if min_files is not None and file_count < min_files:
                return False
            if max_files is not None and file_count > max_files:
                return False
            return True

        return self.filter(predicate)

    def group_by_extension(self) -> dict[str, "ComposerSessionCollection"]:
        """Group sessions by file extension.

        Returns:
            Dictionary mapping extensions to collections of sessions.
        """

        result: dict[str, list[ComposerSession]] = {}
        for session in self._items:
            for ext in session.file_extensions:
                if ext not in result:
                    result[ext] = []
                result[ext].append(session)

        return {ext: ComposerSessionCollection(sessions) for ext, sessions in result.items()}


class AICodeTrackingCollection(Collection["AICodeTrackingEntry"]):
    """Collection of AICodeTrackingEntry objects with domain-specific methods."""

    def filter_by_source(self, source: str) -> "AICodeTrackingCollection":
        """Filter entries by source (e.g., 'composer').

        Args:
            source: Source to filter by.

        Returns:
            Filtered collection.
        """
        return self.filter(lambda entry: entry.source == source)

    def filter_by_extension(self, extension: str) -> "AICodeTrackingCollection":
        """Filter entries by file extension.

        Args:
            extension: File extension to filter by.

        Returns:
            Filtered collection.
        """
        return self.filter(lambda entry: entry.file_extension == extension)

    def filter_by_composer_id(self, composer_id: str) -> "AICodeTrackingCollection":
        """Filter entries by composer ID.

        Args:
            composer_id: Composer session ID to filter by.

        Returns:
            Filtered collection.
        """
        return self.filter(lambda entry: entry.composer_id == composer_id)

    def group_by_source(self) -> dict[str, "AICodeTrackingCollection"]:
        """Group entries by source.

        Returns:
            Dictionary mapping sources to collections of entries.
        """

        def key_func(entry: "AICodeTrackingEntry") -> str:
            return entry.source or "unknown"

        return self.group_by(key_func)

    def group_by_extension(self) -> dict[str, "AICodeTrackingCollection"]:
        """Group entries by file extension.

        Returns:
            Dictionary mapping extensions to collections of entries.
        """

        def key_func(entry: "AICodeTrackingEntry") -> str:
            return entry.file_extension or "unknown"

        return self.group_by(key_func)
