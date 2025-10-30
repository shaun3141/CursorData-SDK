"""Property groups for organizing related fields in models.

Groups related fields into logical properties for easier access and understanding.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dateutil.parser import parse as parse_date


@dataclass
class CodeGroup:
    """Group of code-related fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def suggested_blocks(self) -> List[Any]:
        """Get suggested code blocks."""
        return self._conv.suggested_code_blocks

    @property
    def user_responses(self) -> List[Any]:
        """Get user responses to suggested code blocks."""
        return self._conv.user_responses_to_suggested_code_blocks

    @property
    def assistant_diffs(self) -> List[Any]:
        """Get assistant suggested diffs."""
        return self._conv.assistant_suggested_diffs

    @property
    def diffs_since_apply(self) -> List[Any]:
        """Get diffs since last apply."""
        return self._conv.diffs_since_last_apply

    @property
    def git_diffs(self) -> List[Any]:
        """Get git diff information."""
        return self._conv.git_diffs

    @property
    def file_diff_trajectories(self) -> List[Any]:
        """Get file diff trajectories."""
        return self._conv.file_diff_trajectories

    @property
    def diff_histories(self) -> List[Any]:
        """Get diff histories."""
        return self._conv.diff_histories

    @property
    def codebase_context(self) -> List[Any]:
        """Get codebase context chunks."""
        return self._conv.codebase_context_chunks

    def has_code_changes(self) -> bool:
        """Check if there are any code changes."""
        return (
            len(self.suggested_blocks) > 0
            or len(self.assistant_diffs) > 0
            or len(self.diffs_since_apply) > 0
            or len(self.git_diffs) > 0
        )


@dataclass
class ContextGroup:
    """Group of context-related fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def context(self) -> Optional[Dict[str, Any]]:
        """Get the main context object."""
        return self._conv.context

    @property
    def attached_code_chunks(self) -> List[Any]:
        """Get attached code chunks."""
        return self._conv.attached_code_chunks

    @property
    def attached_files_metadata(self) -> List[Any]:
        """Get attached file metadata."""
        return self._conv.attached_file_code_chunks_metadata_only

    @property
    def attached_folders(self) -> List[Any]:
        """Get attached folders (new format)."""
        return self._conv.attached_folders_new

    @property
    def attached_folders_old(self) -> List[Any]:
        """Get attached folders (old format)."""
        return self._conv.attached_folders

    @property
    def cursor_rules(self) -> List[Any]:
        """Get cursor rules."""
        return self._conv.cursor_rules

    @property
    def knowledge_items(self) -> List[Any]:
        """Get knowledge items."""
        return self._conv.knowledge_items

    @property
    def docs_references(self) -> List[Any]:
        """Get documentation references."""
        return self._conv.docs_references

    @property
    def web_references(self) -> List[Any]:
        """Get web references."""
        return self._conv.web_references

    @property
    def ai_web_search_results(self) -> List[Any]:
        """Get AI web search results."""
        return self._conv.ai_web_search_results

    @property
    def external_links(self) -> List[Any]:
        """Get external links."""
        return self._conv.external_links

    @property
    def human_changes(self) -> List[Any]:
        """Get human changes."""
        return self._conv.human_changes

    @property
    def has_human_changes(self) -> bool:
        """Check if human changes were attached."""
        return self._conv.attached_human_changes

    def has_context(self) -> bool:
        """Check if there is any context attached."""
        return (
            self.context is not None
            or len(self.attached_code_chunks) > 0
            or len(self.attached_files_metadata) > 0
            or len(self.attached_folders) > 0
            or len(self.cursor_rules) > 0
            or len(self.knowledge_items) > 0
        )


@dataclass
class MetadataGroup:
    """Group of metadata fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def created_at(self) -> Optional[str]:
        """Get creation timestamp as ISO string."""
        return self._conv.created_at

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Get creation timestamp as datetime object."""
        if not self._conv.created_at:
            return None
        try:
            return parse_date(self._conv.created_at)
        except Exception:
            return None

    @property
    def bubble_id(self) -> Optional[str]:
        """Get bubble ID."""
        return self._conv.bubble_id

    @property
    def request_id(self) -> Optional[str]:
        """Get request ID."""
        return self._conv.request_id

    @property
    def checkpoint_id(self) -> Optional[str]:
        """Get checkpoint ID."""
        return self._conv.checkpoint_id

    @property
    def input_tokens(self) -> Optional[int]:
        """Get input token count."""
        return self._conv.input_tokens

    @property
    def output_tokens(self) -> Optional[int]:
        """Get output token count."""
        return self._conv.output_tokens

    @property
    def total_tokens(self) -> Optional[int]:
        """Get total token count."""
        if self.input_tokens is not None and self.output_tokens is not None:
            return self.input_tokens + self.output_tokens
        return None

    @property
    def model_name(self) -> Optional[str]:
        """Get model name."""
        return self._conv.model_name

    @property
    def is_agentic(self) -> bool:
        """Check if conversation is agentic."""
        return self._conv.is_agentic

    @property
    def is_refunded(self) -> bool:
        """Check if conversation was refunded."""
        return self._conv.is_refunded

    @property
    def is_nudge(self) -> bool:
        """Check if this is a nudge message."""
        return self._conv.is_nudge

    @property
    def is_quick_search(self) -> bool:
        """Check if this is a quick search query."""
        return self._conv.is_quick_search_query

    @property
    def is_plan_execution(self) -> bool:
        """Check if this is part of plan execution."""
        return self._conv.is_plan_execution

    @property
    def use_web(self) -> bool:
        """Check if web search was enabled."""
        return self._conv.use_web

    @property
    def unified_mode(self) -> Optional[int]:
        """Get unified mode setting."""
        return self._conv.unified_mode


@dataclass
class LintingGroup:
    """Group of linting-related fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def lints(self) -> List[Any]:
        """Get lint errors/warnings."""
        return self._conv.lints

    @property
    def approximate_errors(self) -> List[Any]:
        """Get approximate lint errors."""
        return self._conv.approximate_lint_errors

    @property
    def multi_file_errors(self) -> List[Any]:
        """Get multi-file linter errors."""
        return self._conv.multi_file_linter_errors

    def has_errors(self) -> bool:
        """Check if there are any lint errors."""
        return (
            len(self.lints) > 0
            or len(self.approximate_errors) > 0
            or len(self.multi_file_errors) > 0
        )

    def error_count(self) -> int:
        """Get total error count."""
        return len(self.lints) + len(self.approximate_errors) + len(self.multi_file_errors)


@dataclass
class VersionControlGroup:
    """Group of version control-related fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def commits(self) -> List[Any]:
        """Get git commits."""
        return self._conv.commits

    @property
    def pull_requests(self) -> List[Any]:
        """Get pull requests."""
        return self._conv.pull_requests

    @property
    def git_diffs(self) -> List[Any]:
        """Get git diffs."""
        return self._conv.git_diffs

    def has_vcs_info(self) -> bool:
        """Check if there is any version control information."""
        return (
            len(self.commits) > 0
            or len(self.pull_requests) > 0
            or len(self.git_diffs) > 0
        )


@dataclass
class ToolGroup:
    """Group of tool-related fields from BubbleConversation."""

    _conv: "BubbleConversation"

    @property
    def terminal_files(self) -> List[Any]:
        """Get terminal files."""
        return self._conv.terminal_files

    @property
    def interpreter_results(self) -> List[Any]:
        """Get interpreter results."""
        return self._conv.interpreter_results

    @property
    def tool_results(self) -> List[Any]:
        """Get tool results."""
        return self._conv.tool_results

    @property
    def supported_tools(self) -> List[Any]:
        """Get supported tools."""
        return self._conv.supported_tools

    @property
    def has_previous_terminal_command(self) -> bool:
        """Check if there was a previous terminal command."""
        return self._conv.existed_previous_terminal_command

    @property
    def has_subsequent_terminal_command(self) -> bool:
        """Check if there was a subsequent terminal command."""
        return self._conv.existed_subsequent_terminal_command

    def has_tool_usage(self) -> bool:
        """Check if any tools were used."""
        return (
            len(self.terminal_files) > 0
            or len(self.interpreter_results) > 0
            or len(self.tool_results) > 0
        )

