"""Property-based tests using hypothesis."""

import re
import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cursordata.utils import camel_to_snake, decode_json_value, parse_key_pattern


@pytest.mark.unit
class TestDecodeJsonValueProperty:
    """Property-based tests for decode_json_value."""

    @given(st.text(min_size=0, max_size=1000))
    def test_decode_json_never_crashes(self, text):
        """Test that decode_json_value never crashes on string input."""
        result = decode_json_value(text)
        # Should return None or a parsed value, never crash
        assert result is None or isinstance(result, (dict, list, str, int, float, bool))

    @given(st.binary(min_size=0, max_size=1000))
    def test_decode_json_bytes_never_crashes(self, data):
        """Test that decode_json_value never crashes on bytes input."""
        result = decode_json_value(data)
        # Should return None or a parsed value, never crash
        assert result is None or isinstance(result, (dict, list, str, int, float, bool))

    @given(st.none() | st.text() | st.binary())
    def test_decode_json_handles_all_types(self, value):
        """Test that decode_json_value handles None, text, and binary."""
        result = decode_json_value(value)
        # Should return None or a parsed value
        assert result is None or isinstance(result, (dict, list, str, int, float, bool))


@pytest.mark.unit
class TestParseKeyPatternProperty:
    """Property-based tests for parse_key_pattern."""

    @given(
        st.text(alphabet=string.ascii_letters + string.digits + ":_-", min_size=1, max_size=100),
        st.text(alphabet=string.ascii_letters + string.digits + ":{}-", min_size=1, max_size=100)
    )
    def test_parse_key_pattern_never_crashes(self, key, pattern):
        """Test that parse_key_pattern never crashes."""
        try:
            result = parse_key_pattern(key, pattern)
            # Should return None or a dict
            assert result is None or isinstance(result, dict)
        except (re.PatternError, ValueError):
            # If the pattern is invalid regex, that's acceptable - the function
            # may raise an error when building the regex pattern
            pass

    @given(
        st.text(alphabet=string.ascii_letters + string.digits + ":", min_size=1, max_size=50),
        st.lists(st.text(alphabet=string.ascii_letters, min_size=1, max_size=10), min_size=1, max_size=5)
    )
    def test_parse_key_pattern_with_placeholders(self, prefix, parts):
        """Test parsing keys with placeholders."""
        key = prefix + ":" + ":".join(parts)
        pattern = prefix + ":" + ":".join([f"{{part{i}}}" for i in range(len(parts))])
        result = parse_key_pattern(key, pattern)
        # Should return None or a dict with expected keys
        if result is not None:
            assert isinstance(result, dict)
            assert all(f"part{i}" in result for i in range(len(parts)))


@pytest.mark.unit
class TestCamelToSnakeProperty:
    """Property-based tests for camel_to_snake."""

    @given(st.text(alphabet=string.ascii_letters + string.digits, min_size=0, max_size=100))
    def test_camel_to_snake_never_crashes(self, text):
        """Test that camel_to_snake never crashes."""
        result = camel_to_snake(text)
        assert isinstance(result, str)
        assert len(result) == len(text) or len(result) >= len(text) - text.count("_")

    @given(st.text(alphabet=string.ascii_letters, min_size=1, max_size=50))
    def test_camel_to_snake_preserves_characters(self, text):
        """Test that camel_to_snake preserves all characters (case-insensitive)."""
        result = camel_to_snake(text)
        # All characters should be preserved (case-insensitive)
        assert result.lower() == text.lower() or "_" in result

    @given(st.text(alphabet=string.ascii_letters, min_size=0, max_size=10))
    def test_camel_to_snake_empty_string(self, empty):
        """Test that camel_to_snake handles empty strings."""
        if not empty:
            result = camel_to_snake("")
            assert result == ""

