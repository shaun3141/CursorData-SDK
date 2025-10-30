"""Tests for utility functions."""

import json

import pytest

from cursordata.utils import (
    auto_map_camel_to_snake,
    camel_to_snake,
    decode_json_value,
    map_dict_to_model,
    parse_cursordiskkv_rows,
    parse_key_pattern,
)


@pytest.mark.unit
class TestDecodeJsonValue:
    """Tests for decode_json_value function."""

    def test_decode_bytes_valid_json(self):
        """Test decoding valid JSON from bytes."""
        data = {"key": "value", "number": 123}
        json_bytes = json.dumps(data).encode("utf-8")
        result = decode_json_value(json_bytes)
        assert result == data

    def test_decode_string_valid_json(self):
        """Test decoding valid JSON from string."""
        data = {"key": "value", "number": 123}
        json_str = json.dumps(data)
        result = decode_json_value(json_str)
        assert result == data

    def test_decode_invalid_json(self):
        """Test decoding invalid JSON returns None."""
        invalid_json = b"not valid json{"
        result = decode_json_value(invalid_json)
        assert result is None

    def test_decode_empty_string(self):
        """Test decoding empty string."""
        result = decode_json_value("")
        assert result is None

    def test_decode_none(self):
        """Test decoding None."""
        result = decode_json_value(None)
        # None should return None (not raise an error)
        assert result is None

    def test_decode_complex_json(self):
        """Test decoding complex nested JSON."""
        data = {
            "array": [1, 2, 3],
            "nested": {"key": "value"},
            "null": None,
            "bool": True,
        }
        json_bytes = json.dumps(data).encode("utf-8")
        result = decode_json_value(json_bytes)
        assert result == data


@pytest.mark.unit
class TestParseKeyPattern:
    """Tests for parse_key_pattern function."""

    def test_parse_bubble_key(self):
        """Test parsing bubble ID key pattern."""
        key = "bubbleId:abc123:conv456"
        pattern = "bubbleId:{bubble_id}:{conversation_id}"
        result = parse_key_pattern(key, pattern)
        assert result == {"bubble_id": "abc123", "conversation_id": "conv456"}

    def test_parse_checkpoint_key(self):
        """Test parsing checkpoint key pattern."""
        key = "checkpointId:bubble123:checkpoint789"
        pattern = "checkpointId:{bubble_id}:{checkpoint_id}"
        result = parse_key_pattern(key, pattern)
        assert result == {"bubble_id": "bubble123", "checkpoint_id": "checkpoint789"}

    def test_parse_composer_data_key(self):
        """Test parsing composer data key."""
        key = "composerData:comp_001"
        pattern = "composerData:{composer_id}"
        result = parse_key_pattern(key, pattern)
        assert result == {"composer_id": "comp_001"}

    def test_parse_inline_diffs_key(self):
        """Test parsing inline diffs key."""
        key = "inlineDiffs-workspace_001"
        pattern = "inlineDiffs-{workspace_id}"
        result = parse_key_pattern(key, pattern)
        assert result == {"workspace_id": "workspace_001"}

    def test_parse_no_match(self):
        """Test parsing key that doesn't match pattern."""
        key = "unknown:key"
        pattern = "bubbleId:{bubble_id}:{conversation_id}"
        result = parse_key_pattern(key, pattern)
        assert result is None

    def test_parse_exact_match_no_placeholders(self):
        """Test parsing key with exact match and no placeholders."""
        key = "exactKey"
        pattern = "exactKey"
        result = parse_key_pattern(key, pattern)
        assert result == {}

    def test_parse_partial_match(self):
        """Test parsing key that partially matches."""
        key = "bubbleId:abc"
        pattern = "bubbleId:{bubble_id}:{conversation_id}"
        result = parse_key_pattern(key, pattern)
        # Should not match if pattern requires more parts than key has
        # The regex expects a colon separator, so partial match should fail
        assert result is None, f"Expected None for partial match, got {result}"

    def test_parse_complex_key(self):
        """Test parsing key with multiple segments."""
        key = "prefix:part1:part2:part3:final"
        pattern = "prefix:{p1}:{p2}:{p3}:{final}"
        result = parse_key_pattern(key, pattern)
        assert result == {"p1": "part1", "p2": "part2", "p3": "part3", "final": "final"}


@pytest.mark.unit
class TestCamelToSnake:
    """Tests for camel_to_snake function."""

    def test_simple_camel_case(self):
        """Test simple camelCase conversion."""
        assert camel_to_snake("bubbleId") == "bubble_id"
        assert camel_to_snake("fileExtension") == "file_extension"

    def test_multiple_words(self):
        """Test camelCase with multiple words."""
        assert camel_to_snake("attachedCodeChunks") == "attached_code_chunks"
        assert camel_to_snake("inputTokens") == "input_tokens"

    def test_already_snake_case(self):
        """Test that snake_case remains unchanged."""
        assert camel_to_snake("already_snake") == "already_snake"

    def test_single_word(self):
        """Test single word."""
        assert camel_to_snake("key") == "key"
        assert camel_to_snake("Key") == "key"

    def test_empty_string(self):
        """Test empty string."""
        assert camel_to_snake("") == ""

    def test_all_uppercase(self):
        """Test all uppercase word."""
        assert camel_to_snake("ID") == "id"

    def test_mixed_case(self):
        """Test mixed case conversion."""
        assert camel_to_snake("HTMLContent") == "html_content"
        assert camel_to_snake("XMLParser") == "xml_parser"


@pytest.mark.unit
class TestMapDictToModel:
    """Tests for map_dict_to_model function."""

    def test_simple_mapping(self):
        """Test simple field mapping."""
        data = {"camelKey": "value", "otherKey": "other"}
        mapping = {"camelKey": "snake_key"}
        result = map_dict_to_model(data, mapping)
        assert result == {"snake_key": "value"}
        assert "otherKey" not in result

    def test_multiple_mappings(self):
        """Test mapping multiple fields."""
        data = {"key1": "val1", "key2": "val2", "key3": "val3"}
        mapping = {"key1": "field1", "key2": "field2"}
        result = map_dict_to_model(data, mapping)
        assert result == {"field1": "val1", "field2": "val2"}
        assert "key3" not in result

    def test_missing_source_key(self):
        """Test mapping when source key doesn't exist."""
        data = {"key1": "val1"}
        mapping = {"key1": "field1", "missingKey": "field2"}
        result = map_dict_to_model(data, mapping)
        assert result == {"field1": "val1"}
        assert "field2" not in result

    def test_empty_mapping(self):
        """Test mapping with empty mapping dict."""
        data = {"key1": "val1", "key2": "val2"}
        mapping = {}
        result = map_dict_to_model(data, mapping)
        assert result == {}

    def test_empty_data(self):
        """Test mapping with empty data dict."""
        data = {}
        mapping = {"key1": "field1"}
        result = map_dict_to_model(data, mapping)
        assert result == {}


@pytest.mark.unit
class TestAutoMapCamelToSnake:
    """Tests for auto_map_camel_to_snake function."""

    def test_auto_map_without_known_fields(self):
        """Test auto-mapping without known fields."""
        data = {"bubbleId": "b123", "fileExtension": ".py"}
        mapped, unknown = auto_map_camel_to_snake(data)
        assert mapped == {"bubble_id": "b123", "file_extension": ".py"}
        assert unknown == {}

    def test_auto_map_with_known_fields(self):
        """Test auto-mapping with known fields."""
        data = {"bubbleId": "b123", "fileExtension": ".py", "unknownKey": "value"}
        known_fields = {"bubbleId": "bubble_id"}
        mapped, unknown = auto_map_camel_to_snake(data, known_fields)
        assert mapped["bubble_id"] == "b123"
        assert "file_extension" in mapped  # Auto-converted
        assert "unknownKey" not in mapped
        assert unknown == {}

    def test_empty_data(self):
        """Test auto-mapping empty data."""
        data = {}
        mapped, unknown = auto_map_camel_to_snake(data)
        assert mapped == {}
        assert unknown == {}


@pytest.mark.unit
class TestParseCursordiskkvRows:
    """Tests for parse_cursordiskkv_rows function."""

    def test_parse_valid_rows(self):
        """Test parsing valid cursorDiskKV rows."""
        class MockRow:
            def __getitem__(self, key):
                if key == "key":
                    return "bubbleId:b1:c1"
                elif key == "value":
                    return json.dumps({"type": 1})
                raise KeyError(key)

        rows = [MockRow()]

        def factory(data, key_parts=None):
            return data

        result = parse_cursordiskkv_rows(rows, factory, key_pattern="bubbleId:{id}:{conv}")
        assert len(result) == 1

    def test_parse_invalid_json(self):
        """Test parsing rows with invalid JSON."""
        class MockRow:
            def __getitem__(self, key):
                if key == "key":
                    return "bubbleId:b1:c1"
                elif key == "value":
                    return "invalid json{"
                raise KeyError(key)

        rows = [MockRow()]

        def factory(data, key_parts=None):
            return data

        result = parse_cursordiskkv_rows(rows, factory)
        assert len(result) == 0

    def test_parse_non_dict_json(self):
        """Test parsing rows with non-dict JSON."""
        class MockRow:
            def __getitem__(self, key):
                if key == "key":
                    return "bubbleId:b1:c1"
                elif key == "value":
                    return json.dumps([1, 2, 3])
                raise KeyError(key)

        rows = [MockRow()]

        def factory(data, key_parts=None):
            return data

        result = parse_cursordiskkv_rows(rows, factory)
        assert len(result) == 0

    def test_parse_with_key_parser(self):
        """Test parsing rows with custom key parser."""
        class MockRow:
            def __getitem__(self, key):
                if key == "key":
                    return "bubbleId:b1:c1"
                elif key == "value":
                    return json.dumps({"type": 1})
                raise KeyError(key)

        rows = [MockRow()]

        def factory(data, key_parts=None):
            return {"data": data, "parts": key_parts}

        def key_parser(key):
            return {"bubble_id": key.split(":")[1]}

        result = parse_cursordiskkv_rows(rows, factory, key_parser=key_parser)
        assert len(result) == 1
        assert result[0]["parts"] == {"bubble_id": "b1"}

