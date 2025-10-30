Quick Start Guide
=================

This guide introduces the CursorData SDK through common use cases. Each section shows how to solve a specific problem you might encounter when analyzing your Cursor usage data.

The SDK automatically finds your Cursor database on macOS, Windows, and Linux—just initialize the client and start exploring:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Your code here
       pass

.. note::
   All code examples in this guide assume you have Cursor installed and have used it at least once. The database must exist at the default location for your platform.

Use Case 1: Getting an Overview of Your Usage
---------------------------------------------

**When to use this**: You want a quick snapshot of how you've been using Cursor—how many AI-assisted code changes you've made, what file types you work with most, and when tracking started.

The `get_usage_stats()` method gives you a comprehensive overview:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       stats = client.get_usage_stats()
       
       print(f"You've made {stats.total_tracking_entries} AI-assisted code changes")
       print(f"Across {stats.composer_sessions} composer sessions")
       print(f"Including {stats.total_scored_commits} scored commits")
       
       if stats.tracking_start_time:
           print(f"Tracking started: {stats.tracking_start_time.strftime('%Y-%m-%d')}")
       
       # See what file types you work with most
       print("\nMost worked-on file types:")
       top_extensions = sorted(
           stats.most_used_file_extensions.items(),
           key=lambda x: x[1],
           reverse=True
       )[:5]
       
       for ext, count in top_extensions:
           print(f"  {ext or '(no extension)'}: {count} changes")

This gives you a high-level understanding of your coding patterns and helps identify what you're working on most frequently.

Use Case 2: Analyzing Your Work Patterns
-----------------------------------------

**When to use this**: You want to understand which files and projects you've been modifying, or analyze your workflow patterns over time.

Get all unique files that have been modified with AI assistance:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       entries = client.get_ai_code_tracking_entries()
       
       # Collect unique files
       unique_files = set()
       file_extensions = {}
       
       for entry in entries:
           if entry.file_name:
               unique_files.add(entry.file_name)
           if entry.file_extension:
               file_extensions[entry.file_extension] = \
                   file_extensions.get(entry.file_extension, 0) + 1
       
       print(f"Total unique files modified: {len(unique_files)}")
       print("\nTop 10 most active files:")
       for file_path in sorted(unique_files)[:10]:
           print(f"  {file_path}")

Or analyze extension patterns to understand your tech stack usage:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       stats = client.get_usage_stats()
       
       # Find what percentage of work is in each file type
       total = sum(stats.most_used_file_extensions.values())
       print("Distribution of work by file type:")
       for ext, count in sorted(
           stats.most_used_file_extensions.items(),
           key=lambda x: x[1],
           reverse=True
       ):
           percentage = (count / total) * 100
           print(f"  {ext or '(no extension)'}: {count} ({percentage:.1f}%)")

Use Case 3: Exploring AI Code Tracking Entries
-----------------------------------------------

**When to use this**: You need to examine individual AI-generated code changes, find entries by source (Composer, Chat, etc.), or track code generation patterns.

Each entry represents a single AI-assisted code change with metadata:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       entries = client.get_ai_code_tracking_entries()
       
       print(f"Found {len(entries)} total code tracking entries\n")
       
       # Filter by source
       composer_entries = [e for e in entries if e.source == "composer"]
       chat_entries = [e for e in entries if e.source == "chat"]
       
       print(f"Composer entries: {len(composer_entries)}")
       print(f"Chat entries: {len(chat_entries)}")
       
       # Examine recent entries
       print("\nMost recent entries:")
       for entry in entries[:5]:
           print(f"\n  Hash: {entry.hash[:12]}...")
           if entry.file_name:
               print(f"  File: {entry.file_name}")
           if entry.file_extension:
               print(f"  Type: {entry.file_extension}")
           if entry.source:
               print(f"  Source: {entry.source}")
           if entry.composer_id:
               print(f"  Composer Session: {entry.composer_id[:12]}...")

You can use this to audit AI-generated code, track what tools (Composer vs Chat) you use most, or build custom analytics.

Use Case 4: Understanding Composer Sessions
--------------------------------------------

**When to use this**: You want to analyze multi-file editing sessions, see which files were changed together, or understand the scope of your Composer workflows.

Composer sessions group together related code changes that happened in a single multi-file editing session:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       sessions = client.get_composer_sessions()
       
       print(f"You've had {len(sessions)} composer sessions\n")
       
       # Analyze session sizes
       for session in sessions[:5]:
           print(f"Session {session.composer_id[:12]}...:")
           print(f"  Code changes: {session.entries_count}")
           print(f"  Files modified: {len(session.files_modified)}")
           print(f"  File types: {', '.join(session.file_extensions[:5])}")
           if len(session.files_modified) > 0:
               print(f"  Sample files:")
               for file_path in list(session.files_modified)[:3]:
                   print(f"    - {file_path}")
           print()

This helps you understand how you're using Composer's multi-file editing capabilities and identify patterns in your workflow.

Use Case 5: Accessing Bubble Conversations
-------------------------------------------

**When to use this**: You need to retrieve conversation data stored in the database, access chat history, or analyze conversation patterns.

Bubble conversations contain the structured data from your Cursor conversations:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Get recent conversations
       conversations = client.get_bubble_conversations(limit=10)
       
       print(f"Found {len(conversations)} conversations\n")
       
       for conv in conversations:
           print(f"Bubble: {conv.bubble_id[:12]}...")
           print(f"  Conversation: {conv.conversation_id[:12]}...")
           if conv.data:
               # The data field contains the full conversation structure
               print(f"  Has conversation data: Yes")
           print()

You can also filter by a specific bubble ID:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Get all conversations for a specific bubble
       bubble_id = "your-bubble-id-here"
       conversations = client.get_bubble_conversations(bubble_id=bubble_id)
       
       for conv in conversations:
           # Process conversation data
           pass

Use Case 6: Direct Database Access (Advanced)
----------------------------------------------

**When to use this**: You need to access specific keys, search for patterns, or work with raw database values that aren't covered by the high-level methods.

The SDK provides methods for direct database access when you need more control:

.. code-block:: python

   from cursordata import CursorDataClient, ItemTableKey

   with CursorDataClient() as client:
       # Get database metadata
       info = client.get_database_info()
       print(f"Database location: {info.path}")
       print(f"ItemTable entries: {info.item_table_count}")
       print(f"CursorDiskKV entries: {info.cursor_disk_kv_count}")
       
       # Search for keys matching a pattern
       composer_keys = client.search_keys("composer%", table="ItemTable")
       print(f"\nFound {len(composer_keys)} keys matching 'composer%'")
       
       # Get specific known values
       start_time = client.get_ai_code_tracking_start_time()
       commits = client.get_ai_scored_commits()
       
       # Access raw or JSON-parsed values
       raw_value = client.get_value(ItemTableKey.AI_CODE_TRACKING_START_TIME)
       json_value = client.get_json_value(ItemTableKey.AI_CODE_TRACKING_SCORED_COMMITS)

This gives you full control when building custom tools or accessing data that the high-level methods don't expose.

Putting It All Together
-----------------------

Here's a complete example that demonstrates several use cases:

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Overview
       stats = client.get_usage_stats()
       print(f"=== Usage Overview ===")
       print(f"Total entries: {stats.total_tracking_entries}")
       print(f"Sessions: {stats.composer_sessions}")
       
       # Work patterns
       print(f"\n=== Work Patterns ===")
       top_ext = sorted(
           stats.most_used_file_extensions.items(),
           key=lambda x: x[1],
           reverse=True
       )[0]
       print(f"Most active file type: {top_ext[0]} ({top_ext[1]} changes)")
       
       # Recent sessions
       print(f"\n=== Recent Composer Sessions ===")
       sessions = client.get_composer_sessions()
       for session in sessions[:3]:
           print(f"Session modified {len(session.files_modified)} files")
           print(f"  Types: {', '.join(session.file_extensions[:3])}")

This approach lets you build comprehensive analytics, dashboards, or tools that help you understand and optimize your development workflow.
