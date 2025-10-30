"""Query builder for fluent API access to Cursor data."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from cursordata.client import CursorDataClient
    from cursordata.collections import (
        AICodeTrackingCollection,
        BubbleCollection,
        ComposerSessionCollection,
    )
    from cursordata.cursordiskkv_models import (
        BubbleConversation,
        Checkpoint,
        ComposerData,
        MessageRequestContext,
    )
    from cursordata.models import AICodeTrackingEntry, ComposerSession


class QueryBuilder:
    """Main query builder entry point."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize query builder with client."""
        self._client = client

    def bubbles(self) -> "BubbleQuery":
        """Query bubble conversations."""
        return BubbleQuery(self._client)

    def composer_sessions(self) -> "ComposerSessionQuery":
        """Query composer sessions."""
        return ComposerSessionQuery(self._client)

    def tracking_entries(self) -> "TrackingQuery":
        """Query AI code tracking entries."""
        return TrackingQuery(self._client)

    def checkpoints(self) -> "CheckpointQuery":
        """Query checkpoints."""
        return CheckpointQuery(self._client)

    def message_contexts(self) -> "MessageContextQuery":
        """Query message request contexts."""
        return MessageContextQuery(self._client)

    def composer_data(self) -> "ComposerDataQuery":
        """Query composer data."""
        return ComposerDataQuery(self._client)


class BaseQuery:
    """Base class for query builders."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize base query."""
        self._client = client
        self._limit: Optional[int] = None
        self._offset: int = 0
        self._filters: list[Callable[[Any], bool]] = []

    def limit(self, n: int) -> "BaseQuery":
        """Set the maximum number of results.

        Args:
            n: Maximum number of results.

        Returns:
            Self for chaining.
        """
        self._limit = n
        return self

    def offset(self, n: int) -> "BaseQuery":
        """Set the number of results to skip.

        Args:
            n: Number of results to skip.

        Returns:
            Self for chaining.
        """
        self._offset = n
        return self

    def page(self, page_num: int, page_size: int) -> "BaseQuery":
        """Set pagination.

        Args:
            page_num: Page number (1-indexed).
            page_size: Number of items per page.

        Returns:
            Self for chaining.
        """
        self._offset = (page_num - 1) * page_size
        self._limit = page_size
        return self

    def filter(self, predicate: Callable[[Any], bool]) -> "BaseQuery":
        """Add a filter predicate.

        Args:
            predicate: Function that returns True for items to keep.

        Returns:
            Self for chaining.
        """
        self._filters.append(predicate)
        return self


class BubbleQuery(BaseQuery):
    """Query builder for bubble conversations."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize bubble query."""
        super().__init__(client)
        self._bubble_id: Optional[str] = None

    def filter_by_bubble_id(self, bubble_id: str) -> "BubbleQuery":
        """Filter by bubble ID.

        Args:
            bubble_id: Bubble ID to filter by.

        Returns:
            Self for chaining.
        """
        self._bubble_id = bubble_id
        return self

    def where(
        self,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        model_name: Optional[str] = None,
        min_input_tokens: Optional[int] = None,
        min_output_tokens: Optional[int] = None,
        has_code_blocks: Optional[bool] = None,
        has_diffs: Optional[bool] = None,
        has_lint_errors: Optional[bool] = None,
        is_agentic: Optional[bool] = None,
    ) -> "BubbleQuery":
        """Add common filters for bubbles.

        Args:
            created_after: Filter bubbles created after this date.
            created_before: Filter bubbles created before this date.
            model_name: Filter by model name.
            min_input_tokens: Minimum input tokens.
            min_output_tokens: Minimum output tokens.
            has_code_blocks: Filter bubbles with/without code blocks.
            has_diffs: Filter bubbles with/without diffs.
            has_lint_errors: Filter bubbles with/without lint errors.
            is_agentic: Filter agentic/non-agentic conversations.

        Returns:
            Self for chaining.
        """

        if created_after or created_before:

            def date_filter(conv: "BubbleConversation") -> bool:
                if not conv.created_at:
                    return False
                try:
                    from dateutil.parser import parse as parse_date

                    created = parse_date(conv.created_at)
                except Exception:
                    return False
                if created_after and created < created_after:
                    return False
                if created_before and created > created_before:
                    return False
                return True

            self.filter(date_filter)

        if model_name:

            def model_filter(conv: "BubbleConversation") -> bool:
                return conv.model_name == model_name

            self.filter(model_filter)

        if min_input_tokens is not None or min_output_tokens is not None:

            def token_filter(conv: "BubbleConversation") -> bool:
                if min_input_tokens is not None and (conv.input_tokens or 0) < min_input_tokens:
                    return False
                if min_output_tokens is not None and (conv.output_tokens or 0) < min_output_tokens:
                    return False
                return True

            self.filter(token_filter)

        if has_code_blocks is not None:

            def code_filter(conv: "BubbleConversation") -> bool:
                return (len(conv.suggested_code_blocks) > 0) == has_code_blocks

            self.filter(code_filter)

        if has_diffs is not None:

            def diff_filter(conv: "BubbleConversation") -> bool:
                has = (
                    len(conv.assistant_suggested_diffs) > 0 or len(conv.diffs_since_last_apply) > 0
                )
                return has == has_diffs

            self.filter(diff_filter)

        if has_lint_errors is not None:

            def lint_filter(conv: "BubbleConversation") -> bool:
                has = len(conv.lints) > 0 or len(conv.multi_file_linter_errors) > 0
                return has == has_lint_errors

            self.filter(lint_filter)

        if is_agentic is not None:

            def agentic_filter(conv: "BubbleConversation") -> bool:
                return conv.is_agentic == is_agentic

            self.filter(agentic_filter)

        return self

    def execute(self) -> "BubbleCollection":
        """Execute the query and return results.

        Returns:
            Collection of bubble conversations matching the query.
        """
        from cursordata.collections import BubbleCollection
        from cursordata.cursordiskkv_models import BubbleConversation

        def factory(
            data: dict[str, Any], key_parts: Optional[dict[str, str]] = None
        ) -> Optional[BubbleConversation]:
            bubble_id_val = key_parts.get("bubble_id") if key_parts else None
            conversation_id = key_parts.get("conversation_id") if key_parts else None
            return BubbleConversation.from_dict(
                data, bubble_id=bubble_id_val, conversation_id=conversation_id
            )

        bubbles = self._client._query_cursordiskkv(
            key_prefix="bubbleId:",
            factory=factory,
            key_pattern="bubbleId:{bubble_id}:{conversation_id}",
            filter_id=self._bubble_id,
            limit=self._limit,
            offset=self._offset,
        )

        # Apply filters
        for filter_func in self._filters:
            bubbles = [b for b in bubbles if b and filter_func(b)]

        return BubbleCollection(bubbles)


class ComposerSessionQuery(BaseQuery):
    """Query builder for composer sessions."""

    def where(
        self,
        file_extension: Optional[str] = None,
        min_files: Optional[int] = None,
        max_files: Optional[int] = None,
    ) -> "ComposerSessionQuery":
        """Add common filters for composer sessions.

        Args:
            file_extension: Filter by file extension.
            min_files: Minimum number of files.
            max_files: Maximum number of files.

        Returns:
            Self for chaining.
        """

        if file_extension:

            def ext_filter(session: "ComposerSession") -> bool:
                return file_extension in session.file_extensions

            self.filter(ext_filter)

        if min_files is not None or max_files is not None:

            def file_count_filter(session: "ComposerSession") -> bool:
                file_count = len(session.files_modified)
                if min_files is not None and file_count < min_files:
                    return False
                if max_files is not None and file_count > max_files:
                    return False
                return True

            self.filter(file_count_filter)

        return self

    def execute(self) -> "ComposerSessionCollection":
        """Execute the query and return results.

        Returns:
            Collection of composer sessions matching the query.
        """
        from cursordata.collections import ComposerSessionCollection
        from cursordata.models import ComposerSession

        # Get raw data
        entries = self._client.get_ai_code_tracking_entries()

        # Group by composer_id
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

        # Apply pagination before filters (more efficient)
        if self._offset > 0:
            sessions = sessions[self._offset :]
        if self._limit:
            sessions = sessions[: self._limit]

        # Apply filters
        for filter_func in self._filters:
            sessions = [s for s in sessions if filter_func(s)]

        return ComposerSessionCollection(sessions)


class TrackingQuery(BaseQuery):
    """Query builder for AI code tracking entries."""

    def where(
        self,
        source: Optional[str] = None,
        file_extension: Optional[str] = None,
        composer_id: Optional[str] = None,
    ) -> "TrackingQuery":
        """Add common filters for tracking entries.

        Args:
            source: Filter by source (e.g., 'composer').
            file_extension: Filter by file extension.
            composer_id: Filter by composer ID.

        Returns:
            Self for chaining.
        """

        if source:

            def source_filter(entry: "AICodeTrackingEntry") -> bool:
                return entry.source == source

            self.filter(source_filter)

        if file_extension:

            def ext_filter(entry: "AICodeTrackingEntry") -> bool:
                return entry.file_extension == file_extension

            self.filter(ext_filter)

        if composer_id:

            def composer_filter(entry: "AICodeTrackingEntry") -> bool:
                return entry.composer_id == composer_id

            self.filter(composer_filter)

        return self

    def execute(self) -> "AICodeTrackingCollection":
        """Execute the query and return results.

        Returns:
            Collection of tracking entries matching the query.
        """
        from cursordata.collections import AICodeTrackingCollection

        # Get raw data
        entries = self._client.get_ai_code_tracking_entries()
        entries_list = list(entries.items)

        # Apply pagination before filters
        if self._offset > 0:
            entries_list = entries_list[self._offset :]
        if self._limit:
            entries_list = entries_list[: self._limit]

        # Apply filters
        for filter_func in self._filters:
            entries_list = [e for e in entries_list if filter_func(e)]

        return AICodeTrackingCollection(entries_list)


class CheckpointQuery(BaseQuery):
    """Query builder for checkpoints."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize checkpoint query."""
        super().__init__(client)
        self._bubble_id: Optional[str] = None

    def filter_by_bubble_id(self, bubble_id: str) -> "CheckpointQuery":
        """Filter by bubble ID.

        Args:
            bubble_id: Bubble ID to filter by.

        Returns:
            Self for chaining.
        """
        self._bubble_id = bubble_id
        return self

    def execute(self) -> list["Checkpoint"]:
        """Execute the query and return results.

        Returns:
            List of checkpoints matching the query.
        """
        from cursordata.cursordiskkv_models import Checkpoint

        def factory(
            data: dict[str, Any], key_parts: Optional[dict[str, str]] = None
        ) -> Optional[Checkpoint]:
            return Checkpoint.from_dict(data)

        checkpoints = self._client._query_cursordiskkv(
            key_prefix="checkpointId:",
            factory=factory,
            key_pattern="checkpointId:{bubble_id}:{checkpoint_id}",
            filter_id=self._bubble_id,
            limit=self._limit,
            offset=self._offset,
        )

        # Apply filters
        for filter_func in self._filters:
            checkpoints = [c for c in checkpoints if c and filter_func(c)]

        return checkpoints


class MessageContextQuery(BaseQuery):
    """Query builder for message request contexts."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize message context query."""
        super().__init__(client)
        self._bubble_id: Optional[str] = None

    def filter_by_bubble_id(self, bubble_id: str) -> "MessageContextQuery":
        """Filter by bubble ID.

        Args:
            bubble_id: Bubble ID to filter by.

        Returns:
            Self for chaining.
        """
        self._bubble_id = bubble_id
        return self

    def execute(self) -> list["MessageRequestContext"]:
        """Execute the query and return results.

        Returns:
            List of message request contexts matching the query.
        """
        from cursordata.cursordiskkv_models import MessageRequestContext

        def factory(
            data: dict[str, Any], key_parts: Optional[dict[str, str]] = None
        ) -> Optional[MessageRequestContext]:
            return MessageRequestContext.from_dict(data)

        contexts = self._client._query_cursordiskkv(
            key_prefix="messageRequestContext:",
            factory=factory,
            filter_id=self._bubble_id,
            limit=self._limit,
            offset=self._offset,
        )

        # Apply filters
        for filter_func in self._filters:
            contexts = [c for c in contexts if c and filter_func(c)]

        return contexts


class ComposerDataQuery(BaseQuery):
    """Query builder for composer data."""

    def __init__(self, client: "CursorDataClient"):
        """Initialize composer data query."""
        super().__init__(client)
        self._composer_id: Optional[str] = None

    def filter_by_composer_id(self, composer_id: str) -> "ComposerDataQuery":
        """Filter by composer ID.

        Args:
            composer_id: Composer ID to filter by.

        Returns:
            Self for chaining.
        """
        self._composer_id = composer_id
        return self

    def execute(self) -> list["ComposerData"]:
        """Execute the query and return results.

        Returns:
            List of composer data entries matching the query.
        """
        from cursordata.cursordiskkv_models import ComposerData

        def factory(
            data: dict[str, Any], key_parts: Optional[dict[str, str]] = None
        ) -> Optional[ComposerData]:
            return ComposerData.from_dict(data)

        composer_data = self._client._query_cursordiskkv(
            key_prefix="composerData:",
            factory=factory,
            filter_id=self._composer_id,
            limit=self._limit,
            offset=self._offset,
            exact_match=self._composer_id is not None,
        )

        # Apply filters
        for filter_func in self._filters:
            composer_data = [c for c in composer_data if c and filter_func(c)]

        return composer_data
