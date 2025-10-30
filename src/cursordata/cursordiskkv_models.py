"""Comprehensive models for cursorDiskKV table entries.

This module contains strongly-typed models representing all data structures
stored in the cursorDiskKV table of the Cursor database.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cursordata.utils import auto_map_camel_to_snake

if TYPE_CHECKING:
    from cursordata.model_groups import (
        CodeGroup,
        ContextGroup,
        LintingGroup,
        MetadataGroup,
        ToolGroup,
        VersionControlGroup,
    )


@dataclass
class BubbleConversation:
    """Detailed model for bubbleId entries in cursorDiskKV.

    Bubble conversations represent individual chat interactions within Cursor.
    Each bubble contains a conversation with the AI, including messages, code blocks,
    diffs, context, and metadata.

    Key format: bubbleId:<bubble_id>:<conversation_id>

    Attributes:
        _v: Version number of the bubble format
        type: Type of bubble (internal integer code)
        bubble_id: Unique identifier for this bubble
        request_id: Unique request identifier for this conversation
        checkpoint_id: Associated checkpoint identifier
        text: Plain text content of the conversation
        rich_text: Rich text/HTML content of the conversation
        created_at: Timestamp when the bubble was created (ISO format string)

        # Context and attached items
        context: Context object containing selections, files, folders, etc.
        attached_code_chunks: List of code chunks attached to this conversation
        attached_file_code_chunks_metadata_only: Metadata-only list of attached files
        attached_folders: List of attached folders (old format)
        attached_folders_new: List of attached folders (new format)
        attached_folders_list_dir_results: Results from listing directory contents
        attached_human_changes: Whether human changes were attached
        human_changes: List of human-made changes
        cursor_rules: List of cursor rules applied
        knowledge_items: List of knowledge items referenced
        docs_references: Documentation references
        web_references: Web page references
        ai_web_search_results: Results from AI web searches
        external_links: External links included in context

        # Code and diffs
        suggested_code_blocks: Code blocks suggested by the AI
        user_responses_to_suggested_code_blocks: User interactions with suggested blocks
        assistant_suggested_diffs: Diffs suggested by the assistant
        diffs_since_last_apply: File diffs that occurred since last apply
        git_diffs: Git diff information
        file_diff_trajectories: History of file diff changes
        diff_histories: Complete history of diffs
        diffs_for_compressing_files: Diffs used for file compression
        codebase_context_chunks: Chunks of codebase used as context

        # Linting and errors
        lints: List of linting errors/warnings
        approximate_lint_errors: Approximate count of lint errors
        multi_file_linter_errors: Linter errors across multiple files

        # Terminal and tools
        terminal_files: Files related to terminal commands
        existed_previous_terminal_command: Whether there was a previous terminal command
        existed_subsequent_terminal_command: Whether there was a subsequent terminal command
        interpreter_results: Results from code interpreter
        tool_results: Results from various tools
        supported_tools: List of tools that are supported

        # Version control
        commits: List of git commits referenced
        pull_requests: List of pull requests referenced

        # UI and capabilities
        capabilities: List of available capabilities
        capability_statuses: Dictionary of capability statuses
        capability_contexts: Context for capabilities
        ui_element_picked: UI elements that were picked/selected
        notepads: Notepads associated with this bubble
        recent_locations_history: History of recent file locations
        recently_viewed_files: List of recently viewed files

        # Project and layout
        project_layouts: Layout information for the project
        relevant_files: Files relevant to this conversation

        # Composer integration
        summarized_composers: Composers that have been summarized
        edit_trail_contexts: Context from edit trails
        all_thinking_blocks: All thinking/reasoning blocks

        # Metadata
        is_agentic: Whether this is an agentic conversation
        is_refunded: Whether this conversation was refunded
        is_nudge: Whether this is a nudge message
        is_quick_search_query: Whether this is a quick search
        is_plan_execution: Whether this is part of plan execution
        use_web: Whether web search was enabled
        unified_mode: Unified mode setting (integer)
        edit_tool_supports_search_and_replace: Whether edit tool supports search/replace
        skip_rendering: Whether to skip rendering this bubble
        token_count: Dictionary with 'inputTokens' and 'outputTokens'
        model_info: Information about the AI model used (contains 'modelName')
        console_logs: Console log entries
        todos: List of todos/action items
        deleted_files: List of files that were deleted
        images: List of images attached
    """

    # Core fields
    _v: int | None = None
    type: int | None = None
    bubble_id: str | None = None
    request_id: str | None = None
    checkpoint_id: str | None = None
    text: str | None = None
    rich_text: str | None = None
    created_at: str | None = None

    # Context and attached items
    context: dict[str, Any] | None = None
    attached_code_chunks: list[Any] = field(default_factory=list)
    attached_file_code_chunks_metadata_only: list[Any] = field(default_factory=list)
    attached_folders: list[Any] = field(default_factory=list)
    attached_folders_new: list[Any] = field(default_factory=list)
    attached_folders_list_dir_results: list[Any] = field(default_factory=list)
    attached_human_changes: bool = False
    human_changes: list[Any] = field(default_factory=list)
    cursor_rules: list[Any] = field(default_factory=list)
    knowledge_items: list[Any] = field(default_factory=list)
    docs_references: list[Any] = field(default_factory=list)
    web_references: list[Any] = field(default_factory=list)
    ai_web_search_results: list[Any] = field(default_factory=list)
    external_links: list[Any] = field(default_factory=list)

    # Code and diffs
    suggested_code_blocks: list[Any] = field(default_factory=list)
    user_responses_to_suggested_code_blocks: list[Any] = field(default_factory=list)
    assistant_suggested_diffs: list[Any] = field(default_factory=list)
    diffs_since_last_apply: list[Any] = field(default_factory=list)
    git_diffs: list[Any] = field(default_factory=list)
    file_diff_trajectories: list[Any] = field(default_factory=list)
    diff_histories: list[Any] = field(default_factory=list)
    diffs_for_compressing_files: list[Any] = field(default_factory=list)
    codebase_context_chunks: list[Any] = field(default_factory=list)

    # Linting and errors
    lints: list[Any] = field(default_factory=list)
    approximate_lint_errors: list[Any] = field(default_factory=list)
    multi_file_linter_errors: list[Any] = field(default_factory=list)

    # Terminal and tools
    terminal_files: list[Any] = field(default_factory=list)
    existed_previous_terminal_command: bool = False
    existed_subsequent_terminal_command: bool = False
    interpreter_results: list[Any] = field(default_factory=list)
    tool_results: list[Any] = field(default_factory=list)
    supported_tools: list[Any] = field(default_factory=list)

    # Version control
    commits: list[Any] = field(default_factory=list)
    pull_requests: list[Any] = field(default_factory=list)

    # UI and capabilities
    capabilities: list[Any] = field(default_factory=list)
    capability_statuses: dict[str, Any] = field(default_factory=dict)
    capability_contexts: list[Any] = field(default_factory=list)
    ui_element_picked: list[Any] = field(default_factory=list)
    notepads: list[Any] = field(default_factory=list)
    recent_locations_history: list[Any] = field(default_factory=list)
    recently_viewed_files: list[Any] = field(default_factory=list)

    # Project and layout
    project_layouts: list[Any] = field(default_factory=list)
    relevant_files: list[Any] = field(default_factory=list)

    # Composer integration
    summarized_composers: list[Any] = field(default_factory=list)
    edit_trail_contexts: list[Any] = field(default_factory=list)
    all_thinking_blocks: list[Any] = field(default_factory=list)
    context_pieces: list[Any] = field(default_factory=list)

    # Metadata
    is_agentic: bool = False
    is_refunded: bool = False
    is_nudge: bool = False
    is_quick_search_query: bool = False
    is_plan_execution: bool = False
    use_web: bool = False
    unified_mode: int | None = None
    edit_tool_supports_search_and_replace: bool = False
    skip_rendering: bool = False
    token_count: dict[str, int] = field(default_factory=dict)
    model_info: dict[str, Any] | None = None
    console_logs: list[Any] = field(default_factory=list)
    todos: list[Any] = field(default_factory=list)
    deleted_files: list[Any] = field(default_factory=list)
    images: list[Any] = field(default_factory=list)
    documentation_selections: list[Any] = field(default_factory=list)

    # Raw data storage for fields not explicitly modeled
    _raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], bubble_id: str | None = None, conversation_id: str | None = None
    ) -> BubbleConversation:
        """Create a BubbleConversation from a dictionary.

        Args:
            data: Dictionary containing bubble data from database
            bubble_id: Optional bubble ID (extracted from key if not provided)
            conversation_id: Optional conversation ID (extracted from key if not provided)

        Returns:
            BubbleConversation instance with all fields populated
        """
        # Use auto-mapping with special handling for bubble_id and conversation_id
        kwargs, raw_data = auto_map_camel_to_snake(data)

        # Handle model_info - if modelName was auto-converted, move it to model_info dict
        if "model_name" in kwargs and "model_info" not in kwargs:
            kwargs["model_info"] = {"modelName": kwargs.pop("model_name")}
        elif "model_info" in kwargs and isinstance(kwargs["model_info"], dict):
            # Ensure model_info has modelName key
            if "model_name" in kwargs["model_info"]:
                kwargs["model_info"]["modelName"] = kwargs["model_info"].pop("model_name")

        # Handle token_count - if inputTokens/outputTokens were auto-converted, move to token_count dict
        if "token_count" not in kwargs or not isinstance(kwargs.get("token_count"), dict):
            kwargs["token_count"] = {}
        if "input_tokens" in kwargs:
            kwargs["token_count"]["inputTokens"] = kwargs.pop("input_tokens")
        if "output_tokens" in kwargs:
            kwargs["token_count"]["outputTokens"] = kwargs.pop("output_tokens")

        # Override with provided IDs (from key parsing)
        if bubble_id:
            kwargs["bubble_id"] = bubble_id
        if conversation_id:
            # Store conversation_id in raw_data since it's not a dataclass field
            raw_data["conversation_id"] = conversation_id

        kwargs["_raw_data"] = raw_data

        return cls(**kwargs)

    @property
    def input_tokens(self) -> int | None:
        """Get the number of input tokens."""
        return self.token_count.get("inputTokens")

    @property
    def output_tokens(self) -> int | None:
        """Get the number of output tokens."""
        return self.token_count.get("outputTokens")

    @property
    def model_name(self) -> str | None:
        """Get the model name used for this conversation."""
        if self.model_info:
            return self.model_info.get("modelName")
        return None

    # Property groups for organized access
    @property
    def code(self) -> CodeGroup:
        """Access all code-related fields."""
        from cursordata.model_groups import CodeGroup

        return CodeGroup(self)

    @property
    def context_group(self) -> ContextGroup:
        """Access all context-related fields."""
        from cursordata.model_groups import ContextGroup

        return ContextGroup(self)

    @property
    def metadata(self) -> MetadataGroup:
        """Access metadata fields."""
        from cursordata.model_groups import MetadataGroup

        return MetadataGroup(self)

    @property
    def linting(self) -> LintingGroup:
        """Access linting-related fields."""
        from cursordata.model_groups import LintingGroup

        return LintingGroup(self)

    @property
    def version_control(self) -> VersionControlGroup:
        """Access version control-related fields."""
        from cursordata.model_groups import VersionControlGroup

        return VersionControlGroup(self)

    @property
    def tools(self) -> ToolGroup:
        """Access tool-related fields."""
        from cursordata.model_groups import ToolGroup

        return ToolGroup(self)


@dataclass
class MessageRequestContext:
    """Model for messageRequestContext entries in cursorDiskKV.

    This stores context information for message requests.
    Key format: messageRequestContext:<bubble_id>:<message_id>

    Attributes:
        multi_file_linter_errors: Linter errors across multiple files
        terminal_files: Files related to terminal commands
        cursor_rules: Cursor rules applied to the request
        attached_folders_list_dir_results: Directory listing results for attached folders
        summarized_composers: Composers that have been summarized
        deleted_files: Files that were deleted
        diffs_since_last_apply: Diffs that occurred since last apply
        todos: List of todos/action items
        attached_file_code_chunks_metadata_only: Metadata for attached file code chunks
        project_layouts: Layout information for the project
        knowledge_items: Knowledge items referenced in the request
    """

    multi_file_linter_errors: list[Any] = field(default_factory=list)
    terminal_files: list[Any] = field(default_factory=list)
    cursor_rules: list[Any] = field(default_factory=list)
    attached_folders_list_dir_results: list[Any] = field(default_factory=list)
    summarized_composers: list[Any] = field(default_factory=list)
    deleted_files: list[Any] = field(default_factory=list)
    diffs_since_last_apply: list[Any] = field(default_factory=list)
    todos: list[Any] = field(default_factory=list)
    attached_file_code_chunks_metadata_only: list[Any] = field(default_factory=list)
    project_layouts: list[Any] = field(default_factory=list)
    knowledge_items: list[Any] = field(default_factory=list)

    # Raw data for any additional fields
    _raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MessageRequestContext:
        """Create a MessageRequestContext from a dictionary."""
        kwargs, raw_data = auto_map_camel_to_snake(data)
        kwargs["_raw_data"] = raw_data
        return cls(**kwargs)


@dataclass
class Checkpoint:
    """Model for checkpointId entries in cursorDiskKV.

    Checkpoints represent saved states of files at a particular point in time.
    Key format: checkpointId:<bubble_id>:<checkpoint_id>

    Attributes:
        files: Dictionary mapping file paths to their content/state
        non_existent_files: List of files that don't exist (but were referenced)
        newly_created_folders: List of folders that were newly created
        active_inline_diffs: Active inline diffs associated with this checkpoint
        inline_diff_newly_created_resources: Newly created resources from inline diffs
    """

    files: dict[str, Any] = field(default_factory=dict)
    non_existent_files: list[str] = field(default_factory=list)
    newly_created_folders: list[str] = field(default_factory=list)
    active_inline_diffs: list[Any] = field(default_factory=list)
    inline_diff_newly_created_resources: list[Any] = field(default_factory=list)

    # Raw data for any additional fields
    _raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Checkpoint:
        """Create a Checkpoint from a dictionary."""
        kwargs, raw_data = auto_map_camel_to_snake(data)
        kwargs["_raw_data"] = raw_data
        return cls(**kwargs)


@dataclass
class CodeBlockDiff:
    """Model for codeBlockDiff entries in cursorDiskKV.

    Code block diffs represent differences between code block versions.
    Key format: codeBlockDiff:<bubble_id>:<diff_id>

    Attributes:
        new_model_diff_wrt_v0: Diff of new model version relative to v0
        original_model_diff_wrt_v0: Diff of original model version relative to v0
    """

    new_model_diff_wrt_v0: dict[str, Any] | None = None
    original_model_diff_wrt_v0: dict[str, Any] | None = None

    # Raw data for any additional fields
    _raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CodeBlockDiff:
        """Create a CodeBlockDiff from a dictionary."""
        kwargs, raw_data = auto_map_camel_to_snake(data)
        kwargs["_raw_data"] = raw_data
        return cls(**kwargs)


@dataclass
class ComposerData:
    """Model for composerData entries in cursorDiskKV.

    Composer data contains information about composer sessions.
    Key format: composerData:<composer_id>

    Attributes:
        _v: Version number
        composer_id: Unique identifier for the composer session
        text: Plain text content
        rich_text: Rich text/HTML content
        has_loaded: Whether the composer data has been fully loaded
        status: Status of the composer session
        context: Context information for the composer
        full_conversation_headers_only: Headers for full conversation (metadata only)
        conversation_map: Map of conversations
        git_graph_file_suggestions: File suggestions from git graph
        generating_bubble_ids: IDs of bubbles being generated
        is_reading_long_file: Whether composer is reading a long file
        code_block_data: Data about code blocks in the composer
        original_file_states: Original states of files before composer changes
        newly_created_files: Files that were newly created by composer
    """

    _v: int | None = None
    composer_id: str | None = None
    text: str | None = None
    rich_text: str | None = None
    has_loaded: bool = False
    status: str | None = None
    context: dict[str, Any] | None = None
    full_conversation_headers_only: list[Any] | None = None
    conversation_map: dict[str, Any] | None = None
    git_graph_file_suggestions: list[Any] = field(default_factory=list)
    generating_bubble_ids: list[str] = field(default_factory=list)
    is_reading_long_file: bool = False
    code_block_data: dict[str, Any] | None = None
    original_file_states: dict[str, Any] | None = None
    newly_created_files: list[str] = field(default_factory=list)

    # Raw data for any additional fields
    _raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ComposerData:
        """Create a ComposerData from a dictionary."""
        kwargs, raw_data = auto_map_camel_to_snake(data)
        kwargs["_raw_data"] = raw_data
        return cls(**kwargs)


@dataclass
class InlineDiffs:
    """Model for inlineDiffs entries in cursorDiskKV.

    Inline diffs represent changes made inline within files.
    Key format: inlineDiffs-<workspace_id>

    Attributes:
        workspace_id: Workspace identifier this diff belongs to
        data: The inline diff data (structure varies)
    """

    workspace_id: str
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, workspace_id: str, data: dict[str, Any]) -> InlineDiffs:
        """Create an InlineDiffs from a dictionary."""
        return cls(workspace_id=workspace_id, data=data)
