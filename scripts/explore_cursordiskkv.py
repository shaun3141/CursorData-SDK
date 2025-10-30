"""Script to explore cursorDiskKV table structure."""

import sqlite3
import json
from pathlib import Path
from collections import Counter

db_path = Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"

conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 80)
print("Exploring cursorDiskKV Table")
print("=" * 80)

# Get key pattern statistics
print("\n1. Key Pattern Statistics:")
print("-" * 80)
cursor.execute("""
    SELECT 
        CASE 
            WHEN key LIKE 'bubbleId:%' THEN 'bubbleId'
            WHEN key LIKE 'messageRequestContext:%' THEN 'messageRequestContext'
            ELSE SUBSTR(key, 1, INSTR(key || ':', ':') - 1)
        END as prefix,
        COUNT(*) as count
    FROM cursorDiskKV
    GROUP BY prefix
    ORDER BY count DESC
    LIMIT 20
""")

for row in cursor.fetchall():
    print(f"  {row['prefix']}: {row['count']} entries")

# Sample bubbleId entries
print("\n2. Sample bubbleId Key Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 3")
for row in cursor.fetchall():
    key = row['key']
    value = row['value']
    key_parts = key.split(':')
    print(f"\n  Key: {key[:80]}...")
    print(f"  Parts: {key_parts}")
    print(f"  Value length: {len(value)} bytes")
    
    # Try to parse
    if isinstance(value, bytes):
        try:
            text = value.decode('utf-8')
            if text.startswith('{') or text.startswith('['):
                parsed = json.loads(text)
                print(f"  Parsed type: {type(parsed).__name__}")
                if isinstance(parsed, dict):
                    print(f"  Keys: {list(parsed.keys())[:10]}")
                elif isinstance(parsed, list) and parsed:
                    print(f"  List length: {len(parsed)}")
                    if isinstance(parsed[0], dict):
                        print(f"  First item keys: {list(parsed[0].keys())[:10]}")
        except Exception as e:
            print(f"  Could not parse as JSON: {type(e).__name__}")

# Sample messageRequestContext entries
print("\n3. Sample messageRequestContext Key Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 3")
for row in cursor.fetchall():
    key = row['key']
    value = row['value']
    key_parts = key.split(':')
    print(f"\n  Key: {key[:80]}...")
    print(f"  Parts: {key_parts}")
    print(f"  Value length: {len(value)} bytes")
    
    # Try to parse
    if isinstance(value, bytes):
        try:
            text = value.decode('utf-8')
            if text.startswith('{') or text.startswith('['):
                parsed = json.loads(text)
                print(f"  Parsed type: {type(parsed).__name__}")
                if isinstance(parsed, dict):
                    print(f"  Top-level keys: {list(parsed.keys())[:15]}")
                    # Print structure of first few keys
                    for k, v in list(parsed.items())[:3]:
                        print(f"    {k}: {type(v).__name__} {f'({len(v)})' if isinstance(v, (list, dict)) else ''}")
        except Exception as e:
            print(f"  Could not parse as JSON: {type(e).__name__}")

# Get full structure of one messageRequestContext
print("\n4. Detailed messageRequestContext Structure:")
print("-" * 80)
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 1")
row = cursor.fetchone()
if row:
    value = row['value']
    if isinstance(value, bytes):
        text = value.decode('utf-8')
        try:
            parsed = json.loads(text)
            print(f"Type: {type(parsed).__name__}")
            if isinstance(parsed, dict):
                print(f"\nAll keys ({len(parsed)} total):")
                for key in sorted(parsed.keys())[:30]:
                    val = parsed[key]
                    val_type = type(val).__name__
                    if isinstance(val, dict):
                        val_type += f" ({len(val)} keys)"
                    elif isinstance(val, list):
                        val_type += f" ({len(val)} items)"
                    print(f"  {key}: {val_type}")
                    if isinstance(val, dict) and val:
                        print(f"    Sub-keys: {list(val.keys())[:5]}")
        except Exception as e:
            print(f"Error parsing: {e}")

conn.close()

