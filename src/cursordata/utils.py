"""Utility functions for SDK operations."""

import json
import logging
import re
from typing import Any, Callable, Optional, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar("T")


def decode_json_value(value: Union[bytes, str, None]) -> Optional[Any]:
    """Unified JSON decoding for database values.

    Args:
        value: Database value (bytes or str).

    Returns:
        Parsed JSON value, or None if parsing fails.
    """
    if value is None:
        return None
    try:
        if isinstance(value, bytes):
            return json.loads(value.decode("utf-8"))
        else:
            return json.loads(value)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.warning(f"Failed to decode JSON value: {e}")
        return None


def parse_key_pattern(key: str, pattern: str) -> Optional[dict[str, str]]:
    """Parse a key using a pattern and extract parts.

    Supports patterns like:
    - "bubbleId:{bubble_id}:{conversation_id}" -> extracts bubble_id and conversation_id
    - "checkpointId:{bubble_id}:{checkpoint_id}" -> extracts bubble_id and checkpoint_id
    - "composerData:{composer_id}" -> extracts composer_id
    - "inlineDiffs-{workspace_id}" -> extracts workspace_id

    Args:
        key: The database key to parse.
        pattern: Pattern with named groups in {name} format.

    Returns:
        Dictionary with extracted parts, or None if pattern doesn't match.

    Example:
        >>> parse_key_pattern("bubbleId:abc:123", "bubbleId:{bubble_id}:{conversation_id}")
        {'bubble_id': 'abc', 'conversation_id': '123'}
    """
    # Convert pattern to regex: {name} -> (?P<name>[^:]+) for colon-separated,
    # or (?P<name>.*?) for the last part
    # Handle special cases like inlineDiffs-{workspace_id} where we need to match everything after -
    parts = pattern.split("{")
    if len(parts) == 1:
        # No placeholders, just check if exact match
        return {} if key == pattern else None

    regex_parts = [re.escape(parts[0])]
    for i, part in enumerate(parts[1:]):
        if "}" in part:
            name, rest = part.split("}", 1)
            if i == len(parts) - 2:
                # Last part - match everything
                regex_parts.append(f"(?P<{name}>.*)")
            else:
                # Middle part - match until next separator
                regex_parts.append(f"(?P<{name}>[^:]+)")
            if rest:
                regex_parts.append(re.escape(rest))

    regex_pattern = "".join(regex_parts)
    match = re.match(regex_pattern, key)
    if match:
        return match.groupdict()
    return None


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case.

    Args:
        name: camelCase string.

    Returns:
        snake_case string.

    Example:
        >>> camel_to_snake("bubbleId")
        'bubble_id'
        >>> camel_to_snake("attachedCodeChunks")
        'attached_code_chunks'
    """
    # Insert underscore before uppercase letters (except first char)
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def map_dict_to_model(data: dict[str, Any], field_mapping: dict[str, str]) -> dict[str, Any]:
    """Map dictionary keys using a field mapping.

    Args:
        data: Source dictionary.
        field_mapping: Mapping from source keys to target keys.

    Returns:
        New dictionary with mapped keys.
    """
    result = {}
    for source_key, target_key in field_mapping.items():
        if source_key in data:
            result[target_key] = data[source_key]
    return result


def auto_map_camel_to_snake(data: dict[str, Any], known_fields: Optional[dict[str, str]] = None) -> tuple:
    """Automatically map camelCase keys to snake_case, handling known special cases.

    Args:
        data: Source dictionary with camelCase keys.
        known_fields: Optional mapping of known fields (camelCase -> snake_case).
                     If not provided, auto-converts all keys.

    Returns:
        Tuple of (mapped_fields, unknown_fields).
    """

    mapped: dict[str, Any] = {}
    unknown: dict[str, Any] = {}

    if known_fields:
        # Use provided mapping for known fields
        for camel_key, snake_key in known_fields.items():
            if camel_key in data:
                mapped[snake_key] = data[camel_key]

        # Auto-convert any remaining keys
        for key, value in data.items():
            if key not in known_fields:
                snake_key = camel_to_snake(key)
                mapped[snake_key] = value
    else:
        # Auto-convert all keys
        for key, value in data.items():
            snake_key = camel_to_snake(key)
            mapped[snake_key] = value

    return mapped, unknown


def parse_cursordiskkv_rows(
    rows: list[Any],
    factory: Callable[[dict[str, Any], Optional[dict[str, str]]], Optional[T]],
    key_parser: Optional[Callable[[str], dict[str, str]]] = None,
    key_pattern: Optional[str] = None,
) -> list[T]:
    """Parse cursorDiskKV rows into model objects with error handling.

    Args:
        rows: Database rows (from sqlite3 cursor).
        factory: Function that creates model from dict and optional key parts.
        key_parser: Optional function to parse key into parts.
        key_pattern: Optional pattern string for key parsing.

    Returns:
        List of successfully parsed model objects.
    """
    results = []
    errors = []

    for row in rows:
        try:
            key = row["key"]
            value = row["value"]

            # Decode JSON value
            data = decode_json_value(value)
            if data is None:
                errors.append((key, "Failed to decode JSON"))
                continue

            if not isinstance(data, dict):
                errors.append((key, f"Expected dict, got {type(data).__name__}"))
                continue

            # Parse key if parser provided
            key_parts = None
            if key_parser:
                key_parts = key_parser(key)
            elif key_pattern:
                key_parts = parse_key_pattern(key, key_pattern)

            # Create model instance
            if key_parts:
                instance = factory(data, key_parts)
            else:
                instance = factory(data)

            if instance:
                results.append(instance)
            else:
                errors.append((key, "Factory returned None"))

        except Exception as e:
            try:
                key = row["key"]
            except (KeyError, TypeError, AttributeError):
                key = "unknown"
            errors.append((key, str(e)))
            logger.warning(f"Failed to parse cursorDiskKV row {key}: {e}")

    if errors:
        logger.debug(f"Parsed {len(results)}/{len(rows)} rows successfully, {len(errors)} errors")

    return results

