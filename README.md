# CursorData SDK

[![Tests](https://github.com/shaun3141/CursorData-SDK/actions/workflows/test.yml/badge.svg)](https://github.com/shaun3141/CursorData-SDK/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codecov](https://codecov.io/gh/shaun3141/CursorData-SDK/branch/main/graph/badge.svg)](https://codecov.io/gh/shaun3141/CursorData-SDK)

> **⚠️ Disclaimer:** This is an unofficial project not connected with or endorsed by AnySphere (Cursor). This SDK is developed independently and provided as-is. Use at your own risk. The Cursor editor and its database structure are property of AnySphere.

A well-documented Python SDK for interacting with the local SQLite database that contains all Cursor editor usage data on your computer.

## Features

- 🔍 **Strongly Typed**: Full type hints and dataclasses for all data models
- 📊 **Comprehensive Access**: Query AI code tracking, composer sessions, bubble conversations, and more
- 🎯 **Platform Support**: Automatically detects database location on macOS, Windows, and Linux
- 📚 **Well Documented**: Auto-generated API documentation with Sphinx
- 🔒 **Type Safe**: Full mypy type checking support

## Installation

```bash
pip install cursordata-sdk
```

Or using `uv`:

```bash
uv pip install cursordata-sdk
```

## Quick Start

```python
from cursordata import CursorDataClient
from datetime import datetime, timedelta

# Initialize the client (automatically finds the database)
with CursorDataClient() as client:
    # Get usage statistics
    stats = client.get_usage_stats()
    print(f"Total tracking entries: {stats.total_tracking_entries}")
    print(f"Total scored commits: {stats.total_scored_commits}")
    print(f"Composer sessions: {stats.composer_sessions}")
    
    # Query data using the query builder (primary API)
    # Get recent bubbles with code changes
    week_ago = datetime.now() - timedelta(days=7)
    bubbles = (
        client.query()
        .bubbles()
        .where(created_after=week_ago, has_code_blocks=True)
        .limit(10)
        .execute()
    )
    print(f"Found {len(bubbles)} recent bubbles with code changes")
    
    # Get composer sessions for Python files
    sessions = (
        client.query()
        .composer_sessions()
        .where(file_extension=".py")
        .execute()
    )
    for session in sessions:
        print(f"Session {session.composer_id}: {session.entries_count} entries")
        print(f"  Files: {len(session.files_modified)}")
        print(f"  Extensions: {', '.join(session.file_extensions)}")
    
    # Get database info
    info = client.get_database_info()
    print(f"Database path: {info.path}")
    print(f"ItemTable entries: {info.item_table_count}")
    print(f"CursorDiskKV entries: {info.cursor_disk_kv_count}")
```

## Data Models

The SDK provides strongly-typed data models:

### UsageStats
Aggregated usage statistics including total tracking entries, scored commits, and file extension usage.

### AICodeTrackingEntry
Individual AI code tracking entries with metadata about source, composer ID, file extension, and file name.

### ComposerSession
Composer sessions grouped by session ID with associated files and code entries.

### BubbleConversation
Bubble conversations stored in the database.

### DatabaseInfo
Information about the database file including counts and last modified time.

## API Reference

See the [full API documentation](docs/_build/html/index.html) (generated with Sphinx) for detailed information about all classes and methods.

## Examples

### Analyzing File Extension Usage

```python
from cursordata import CursorDataClient

with CursorDataClient() as client:
    stats = client.get_usage_stats()
    
    # Get most used file extensions
    extensions = sorted(
        stats.most_used_file_extensions.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    print("Most used file extensions:")
    for ext, count in extensions[:10]:
        print(f"  {ext}: {count} entries")
```

### Finding Files Modified by Composer

```python
from cursordata import CursorDataClient

with CursorDataClient() as client:
    sessions = client.get_composer_sessions()
    
    # Collect all unique files
    all_files = set()
    for session in sessions:
        all_files.update(session.files_modified)
    
    print(f"Total unique files modified: {len(all_files)}")
    for file_path in sorted(all_files)[:20]:
        print(f"  {file_path}")
```

### Querying with Filters

```python
from datetime import datetime, timedelta
from cursordata import CursorDataClient

with CursorDataClient() as client:
    # Query bubbles from last week
    week_ago = datetime.now() - timedelta(days=7)
    recent_bubbles = (
        client.query()
        .bubbles()
        .where(created_after=week_ago, has_code_blocks=True)
        .limit(10)
        .execute()
    )
    print(f"Found {len(recent_bubbles)} recent bubbles with code changes")
    
    # Query composer sessions for Python files
    python_sessions = (
        client.query()
        .composer_sessions()
        .where(file_extension=".py")
        .execute()
    )
    print(f"Found {len(python_sessions)} Python composer sessions")
```

## Development

### Setup

```bash
# Install development dependencies
uv pip install -e ".[dev,docs]"

# Or with pip
pip install -e ".[dev,docs]"
```

### Running Tests

```bash
pytest
```

### Building Documentation

```bash
cd docs
make html
# Documentation will be in docs/_build/html/
```

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
