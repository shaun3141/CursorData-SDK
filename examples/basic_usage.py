"""Basic usage examples for the CursorData SDK."""

from datetime import datetime, timedelta

from cursordata import CursorDataClient

print("=" * 60)
print("CursorData SDK - Basic Usage Examples")
print("=" * 60)

with CursorDataClient() as client:
    # Get database info
    print("\n1. Database Information:")
    print("-" * 60)
    info = client.get_database_info()
    print(f"Database path: {info.path}")
    print(f"ItemTable entries: {info.item_table_count}")
    print(f"CursorDiskKV entries: {info.cursor_disk_kv_count}")
    if info.last_modified:
        print(f"Last modified: {info.last_modified}")

    # Get usage statistics
    print("\n2. Usage Statistics:")
    print("-" * 60)
    stats = client.get_usage_stats()
    print(f"Total tracking entries: {stats.total_tracking_entries}")
    print(f"Total scored commits: {stats.total_scored_commits}")
    print(f"Composer sessions: {stats.composer_sessions}")
    if stats.tracking_start_time:
        print(f"Tracking started: {stats.tracking_start_time}")

    # File extensions
    print("\n3. Most Used File Extensions:")
    print("-" * 60)
    extensions = sorted(
        stats.most_used_file_extensions.items(),
        key=lambda x: x[1],
        reverse=True,
    )
    for ext, count in extensions[:10]:
        print(f"  {ext}: {count} entries")

    # Get composer sessions (now returns a collection)
    print("\n4. Composer Sessions (first 5):")
    print("-" * 60)
    sessions = client.get_composer_sessions()
    for session in sessions.take(5):
        print(f"  Session {session.composer_id[:8]}...:")
        print(f"    Entries: {session.entries_count}")
        print(f"    Files: {len(session.files_modified)}")
        print(f"    Extensions: {', '.join(session.file_extensions[:5])}")

    # Get some tracking entries (now returns a collection)
    print("\n5. AI Code Tracking Entries (first 5):")
    print("-" * 60)
    entries = client.get_ai_code_tracking_entries()
    for entry in entries.take(5):
        print(f"  Hash: {entry.hash[:8]}...")
        if entry.file_name:
            print(f"    File: {entry.file_name}")
        if entry.file_extension:
            print(f"    Extension: {entry.file_extension}")
        if entry.source:
            print(f"    Source: {entry.source}")

    # Get bubble conversations using query builder
    print("\n6. Bubble Conversations (first 5):")
    print("-" * 60)
    bubbles = client.query().bubbles().limit(5).execute()
    for conv in bubbles:
        print(f"  Bubble ID: {conv.bubble_id[:8] if conv.bubble_id else 'N/A'}...")
        if conv.metadata.created_datetime:
            print(f"    Created: {conv.metadata.created_datetime}")
        if conv.metadata.model_name:
            print(f"    Model: {conv.metadata.model_name}")
        print(f"    Has code blocks: {conv.code.has_code_changes()}")
        print(f"    Has lint errors: {conv.linting.has_errors()}")

    # Demonstrate Query Builder
    print("\n7. Query Builder Examples:")
    print("-" * 60)
    
    # Query bubbles from last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_bubbles = (
        client.query()
        .bubbles()
        .where(created_after=week_ago)
        .limit(10)
        .execute()
    )
    print(f"  Recent bubbles (last 7 days): {len(recent_bubbles)}")
    
    # Query bubbles with code blocks
    bubbles_with_code = (
        client.query()
        .bubbles()
        .where(has_code_blocks=True)
        .limit(5)
        .execute()
    )
    print(f"  Bubbles with code blocks: {len(bubbles_with_code)}")
    
    # Query composer sessions by extension
    python_sessions = (
        client.query()
        .composer_sessions()
        .where(file_extension=".py")
        .limit(5)
        .execute()
    )
    print(f"  Python composer sessions: {len(python_sessions)}")

    # Demonstrate Collection Methods
    print("\n8. Collection Methods:")
    print("-" * 60)
    
    # Filter and group
    all_bubbles = client.query().bubbles().limit(100).execute()
    
    # Group by date
    by_date = all_bubbles.group_by_date()
    print(f"  Bubbles grouped by date: {len(by_date)} days")
    for date, date_bubbles in list(by_date.items())[:3]:
        print(f"    {date}: {len(date_bubbles)} bubbles")
    
    # Group by model
    by_model = all_bubbles.group_by_model()
    print(f"  Bubbles grouped by model: {len(by_model)} models")
    for model, model_bubbles in list(by_model.items())[:3]:
        print(f"    {model}: {len(model_bubbles)} bubbles")

    # Demonstrate Property Groups
    print("\n9. Property Groups Example:")
    print("-" * 60)
    sample_bubble = all_bubbles.first()
    if sample_bubble:
        print(f"  Sample bubble metadata:")
        print(f"    Created: {sample_bubble.metadata.created_datetime}")
        print(f"    Model: {sample_bubble.metadata.model_name}")
        print(f"    Tokens: {sample_bubble.metadata.input_tokens} in, {sample_bubble.metadata.output_tokens} out")
        print(f"    Is agentic: {sample_bubble.metadata.is_agentic}")
        
        print(f"  Code information:")
        print(f"    Has code changes: {sample_bubble.code.has_code_changes()}")
        print(f"    Suggested blocks: {len(sample_bubble.code.suggested_blocks)}")
        print(f"    Git diffs: {len(sample_bubble.code.git_diffs)}")
        
        print(f"  Linting information:")
        print(f"    Has errors: {sample_bubble.linting.has_errors()}")
        print(f"    Error count: {sample_bubble.linting.error_count()}")

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
