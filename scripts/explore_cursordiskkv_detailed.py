"""Detailed exploration of cursorDiskKV table structures."""

import sqlite3
import json
from pathlib import Path

db_path = Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"

conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def parse_value(value):
    """Parse a database value, handling both bytes and str."""
    if isinstance(value, bytes):
        text = value.decode('utf-8')
    else:
        text = value
    
    try:
        if text.startswith('{') or text.startswith('['):
            return json.loads(text)
    except:
        pass
    
    return text

print("=" * 80)
print("Detailed cursorDiskKV Structure Analysis")
print("=" * 80)

# 1. messageRequestContext detailed structure
print("\n1. messageRequestContext Detailed Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 1")
row = cursor.fetchone()
if row:
    parsed = parse_value(row['value'])
    if isinstance(parsed, dict):
        print(f"Type: dict with {len(parsed)} keys")
        print("\nTop-level structure:")
        for key, value in list(parsed.items())[:20]:
            val_type = type(value).__name__
            if isinstance(value, dict):
                val_type += f" ({len(value)} keys)"
                print(f"  {key}: {val_type}")
                print(f"    Sample sub-keys: {list(value.keys())[:8]}")
            elif isinstance(value, list):
                val_type += f" ({len(value)} items)"
                print(f"  {key}: {val_type}")
                if value and isinstance(value[0], dict):
                    print(f"    First item keys: {list(value[0].keys())[:8]}")
            else:
                print(f"  {key}: {val_type} = {str(value)[:100]}")

# 2. bubbleId structure
print("\n2. bubbleId Detailed Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 1")
row = cursor.fetchone()
if row:
    parsed = parse_value(row['value'])
    if isinstance(parsed, dict):
        print(f"Type: dict with {len(parsed)} keys")
        print("\nStructure:")
        for key, value in parsed.items():
            val_type = type(value).__name__
            if isinstance(value, dict):
                val_type += f" ({len(value)} keys)"
                print(f"  {key}: {val_type}")
                print(f"    Sub-keys: {list(value.keys())[:10]}")
            elif isinstance(value, list):
                val_type += f" ({len(value)} items)"
                print(f"  {key}: {val_type}")
                if value and isinstance(value[0], dict):
                    print(f"    First item keys: {list(value[0].keys())[:10]}")
            else:
                print(f"  {key}: {val_type}")

# 3. checkpointId structure
print("\n3. checkpointId Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'checkpointId:%' LIMIT 1")
row = cursor.fetchone()
if row:
    key = row['key']
    parsed = parse_value(row['value'])
    print(f"Key format: {key.split(':')}")
    print(f"Value type: {type(parsed).__name__}")
    if isinstance(parsed, dict):
        print(f"Keys: {list(parsed.keys())[:15]}")
    elif isinstance(parsed, list):
        print(f"Length: {len(parsed)}")
        if parsed and isinstance(parsed[0], dict):
            print(f"First item keys: {list(parsed[0].keys())[:15]}")

# 4. codeBlockDiff structure
print("\n4. codeBlockDiff Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%' LIMIT 1")
row = cursor.fetchone()
if row:
    key = row['key']
    parsed = parse_value(row['value'])
    print(f"Key format: {key.split(':')}")
    print(f"Value type: {type(parsed).__name__}")
    if isinstance(parsed, dict):
        print(f"Keys: {list(parsed.keys())[:15]}")
    elif isinstance(parsed, list):
        print(f"Length: {len(parsed)}")
        if parsed and isinstance(parsed[0], dict):
            print(f"First item keys: {list(parsed[0].keys())[:15]}")

# 5. composerData structure
print("\n5. composerData Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%' LIMIT 1")
row = cursor.fetchone()
if row:
    key = row['key']
    parsed = parse_value(row['value'])
    print(f"Key format: {key.split(':')}")
    print(f"Value type: {type(parsed).__name__}")
    if isinstance(parsed, dict):
        print(f"Keys: {list(parsed.keys())[:15]}")
    elif isinstance(parsed, list):
        print(f"Length: {len(parsed)}")
        if parsed and isinstance(parsed[0], dict):
            print(f"First item keys: {list(parsed[0].keys())[:15]}")

conn.close()

