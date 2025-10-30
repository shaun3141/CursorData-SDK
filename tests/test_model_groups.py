"""Tests for model groups."""

from datetime import datetime

import pytest

from cursordata.model_groups import (
    CodeGroup,
    ContextGroup,
    LintingGroup,
    MetadataGroup,
    ToolGroup,
    VersionControlGroup,
)
from tests.factories import BubbleConversationFactory


@pytest.mark.unit
class TestCodeGroup:
    """Tests for CodeGroup."""

    def test_suggested_blocks_property(self):
        """Test accessing suggested code blocks."""
        bubble = BubbleConversationFactory.create(
            suggestedCodeBlocks=[{"file": "test.py", "code": "print('hello')"}]
        )
        code_group = CodeGroup(bubble)
        assert len(code_group.suggested_blocks) == 1

    def test_has_code_changes_with_code(self):
        """Test has_code_changes returns True when code exists."""
        bubble = BubbleConversationFactory.create(
            suggestedCodeBlocks=[{"file": "test.py", "code": "print('hello')"}]
        )
        code_group = CodeGroup(bubble)
        assert code_group.has_code_changes() is True

    def test_has_code_changes_without_code(self):
        """Test has_code_changes returns False when no code exists."""
        bubble = BubbleConversationFactory.create(
            suggestedCodeBlocks=[],
            assistantSuggestedDiffs=[],
            diffsSinceLastApply=[],
            gitDiffs=[],
        )
        code_group = CodeGroup(bubble)
        assert code_group.has_code_changes() is False

    def test_assistant_diffs_property(self):
        """Test accessing assistant diffs."""
        bubble = BubbleConversationFactory.create(
            assistantSuggestedDiffs=[{"file": "test.py", "diff": "+line"}]
        )
        code_group = CodeGroup(bubble)
        assert len(code_group.assistant_diffs) == 1


@pytest.mark.unit
class TestContextGroup:
    """Tests for ContextGroup."""

    def test_context_property(self):
        """Test accessing context."""
        bubble = BubbleConversationFactory.create(context={"selection": "test"})
        context_group = ContextGroup(bubble)
        assert context_group.context == {"selection": "test"}

    def test_has_context_with_context(self):
        """Test has_context returns True when context exists."""
        bubble = BubbleConversationFactory.create(
            context={"selection": "test"},
            attachedCodeChunks=[{"file": "test.py"}],
        )
        context_group = ContextGroup(bubble)
        assert context_group.has_context() is True

    def test_has_context_without_context(self):
        """Test has_context returns False when no context exists."""
        bubble = BubbleConversationFactory.create(
            context=None,
            attachedCodeChunks=[],
            attachedFileCodeChunksMetadataOnly=[],
            attachedFoldersNew=[],
            cursorRules=[],
            knowledgeItems=[],
        )
        context_group = ContextGroup(bubble)
        assert context_group.has_context() is False

    def test_attached_code_chunks_property(self):
        """Test accessing attached code chunks."""
        bubble = BubbleConversationFactory.create(
            attachedCodeChunks=[{"file": "test.py", "code": "code"}]
        )
        context_group = ContextGroup(bubble)
        assert len(context_group.attached_code_chunks) == 1


@pytest.mark.unit
class TestMetadataGroup:
    """Tests for MetadataGroup."""

    def test_created_at_property(self):
        """Test accessing created_at."""
        created_at = datetime.now().isoformat() + "Z"
        bubble = BubbleConversationFactory.create(createdAt=created_at)
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.created_at == created_at

    def test_created_datetime_property(self):
        """Test accessing created_datetime."""
        created_at = datetime.now().isoformat() + "Z"
        bubble = BubbleConversationFactory.create(createdAt=created_at)
        metadata_group = MetadataGroup(bubble)
        assert isinstance(metadata_group.created_datetime, datetime)

    def test_created_datetime_none(self):
        """Test created_datetime returns None when created_at is None."""
        bubble = BubbleConversationFactory.create(createdAt=None)
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.created_datetime is None

    def test_total_tokens_calculation(self):
        """Test total_tokens calculation."""
        bubble = BubbleConversationFactory.create(
            tokenCount={"inputTokens": 100, "outputTokens": 50}
        )
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.total_tokens == 150

    def test_total_tokens_none(self):
        """Test total_tokens returns None when token counts are missing."""
        bubble = BubbleConversationFactory.create(tokenCount={})
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.total_tokens is None

    def test_bubble_id_property(self):
        """Test accessing bubble_id."""
        bubble = BubbleConversationFactory.create(bubbleId="bubble_123")
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.bubble_id == "bubble_123"

    def test_model_name_property(self):
        """Test accessing model_name."""
        bubble = BubbleConversationFactory.create(modelInfo={"modelName": "gpt-4"})
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.model_name == "gpt-4"

    def test_is_agentic_property(self):
        """Test accessing is_agentic."""
        bubble = BubbleConversationFactory.create(isAgentic=True)
        metadata_group = MetadataGroup(bubble)
        assert metadata_group.is_agentic is True


@pytest.mark.unit
class TestLintingGroup:
    """Tests for LintingGroup."""

    def test_lints_property(self):
        """Test accessing lints."""
        bubble = BubbleConversationFactory.create(
            lints=[{"file": "test.py", "line": 1, "message": "error"}]
        )
        linting_group = LintingGroup(bubble)
        assert len(linting_group.lints) == 1

    def test_has_errors_with_errors(self):
        """Test has_errors returns True when errors exist."""
        bubble = BubbleConversationFactory.create(
            lints=[{"file": "test.py", "line": 1, "message": "error"}]
        )
        linting_group = LintingGroup(bubble)
        assert linting_group.has_errors() is True

    def test_has_errors_without_errors(self):
        """Test has_errors returns False when no errors exist."""
        bubble = BubbleConversationFactory.create(
            lints=[],
            approximateLintErrors=[],
            multiFileLinterErrors=[],
        )
        linting_group = LintingGroup(bubble)
        assert linting_group.has_errors() is False

    def test_error_count(self):
        """Test error_count calculation."""
        bubble = BubbleConversationFactory.create(
            lints=[{"error": 1}, {"error": 2}],
            approximateLintErrors=[{"error": 3}],
            multiFileLinterErrors=[{"error": 4}],
        )
        linting_group = LintingGroup(bubble)
        assert linting_group.error_count() == 4


@pytest.mark.unit
class TestVersionControlGroup:
    """Tests for VersionControlGroup."""

    def test_commits_property(self):
        """Test accessing commits."""
        bubble = BubbleConversationFactory.create(
            commits=[{"sha": "abc123", "message": "test commit"}]
        )
        vcs_group = VersionControlGroup(bubble)
        assert len(vcs_group.commits) == 1

    def test_has_vcs_info_with_info(self):
        """Test has_vcs_info returns True when VCS info exists."""
        bubble = BubbleConversationFactory.create(
            commits=[{"sha": "abc123"}]
        )
        vcs_group = VersionControlGroup(bubble)
        assert vcs_group.has_vcs_info() is True

    def test_has_vcs_info_without_info(self):
        """Test has_vcs_info returns False when no VCS info exists."""
        bubble = BubbleConversationFactory.create(
            commits=[],
            pullRequests=[],
            gitDiffs=[],
        )
        vcs_group = VersionControlGroup(bubble)
        assert vcs_group.has_vcs_info() is False


@pytest.mark.unit
class TestToolGroup:
    """Tests for ToolGroup."""

    def test_terminal_files_property(self):
        """Test accessing terminal files."""
        bubble = BubbleConversationFactory.create(
            terminalFiles=[{"file": "test.py"}]
        )
        tool_group = ToolGroup(bubble)
        assert len(tool_group.terminal_files) == 1

    def test_has_tool_usage_with_usage(self):
        """Test has_tool_usage returns True when tools were used."""
        bubble = BubbleConversationFactory.create(
            terminalFiles=[{"file": "test.py"}]
        )
        tool_group = ToolGroup(bubble)
        assert tool_group.has_tool_usage() is True

    def test_has_tool_usage_without_usage(self):
        """Test has_tool_usage returns False when no tools were used."""
        bubble = BubbleConversationFactory.create(
            terminalFiles=[],
            interpreterResults=[],
            toolResults=[],
        )
        tool_group = ToolGroup(bubble)
        assert tool_group.has_tool_usage() is False

    def test_has_previous_terminal_command(self):
        """Test has_previous_terminal_command property."""
        bubble = BubbleConversationFactory.create(
            existedPreviousTerminalCommand=True
        )
        tool_group = ToolGroup(bubble)
        assert tool_group.has_previous_terminal_command is True

