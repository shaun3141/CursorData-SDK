cursorDiskKV Table Models
=========================

The ``cursorDiskKV`` table contains various types of structured data stored as key-value pairs.
This module provides strongly-typed models for all known entry types.

Entry Types
-----------

The cursorDiskKV table contains several types of entries:

- **bubbleId** entries (17,000+): Individual chat conversations with detailed context
- **messageRequestContext** entries (800+): Context information for message requests
- **checkpointId** entries (3,000+): Saved file states at checkpoints
- **codeBlockDiff** entries (2,000+): Code block differences between versions
- **composerData** entries (180+): Composer session data
- **inlineDiffs** entries: Workspace-specific inline diff data

BubbleConversation
------------------

The most common entry type, representing individual chat conversations within Cursor.

**Key format:** ``bubbleId:<bubble_id>:<conversation_id>``

**Properties:**

Core Fields
~~~~~~~~~~~

.. py:class:: BubbleConversation

   .. py:attribute:: _v
      :type: Optional[int]
      
      Version number of the bubble format

   .. py:attribute:: type
      :type: Optional[int]
      
      Type of bubble (internal integer code)

   .. py:attribute:: bubble_id
      :type: Optional[str]
      
      Unique identifier for this bubble

   .. py:attribute:: request_id
      :type: Optional[str]
      
      Unique request identifier for this conversation

   .. py:attribute:: checkpoint_id
      :type: Optional[str]
      
      Associated checkpoint identifier

   .. py:attribute:: text
      :type: Optional[str]
      
      Plain text content of the conversation

   .. py:attribute:: rich_text
      :type: Optional[str]
      
      Rich text/HTML content of the conversation

   .. py:attribute:: created_at
      :type: Optional[str]
      
      Timestamp when the bubble was created (ISO format string)

Context and Attached Items
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. py:attribute:: context
      :type: Optional[Dict[str, Any]]
      
      Context object containing selections, files, folders, etc. Includes:
      
      - ``notepads``: Associated notepads
      - ``composers``: Related composers
      - ``quotes``: Quoted content
      - ``selectedCommits``: Selected git commits
      - ``selectedPullRequests``: Selected pull requests
      - ``selectedImages``: Selected images
      - ``folderSelections``: Selected folders
      - ``fileSelections``: Selected files
      - ``terminalFiles``: Terminal-related files
      - ``selections``: General selections

   .. py:attribute:: attached_code_chunks
      :type: List[Any]
      
      List of code chunks attached to this conversation

   .. py:attribute:: attached_file_code_chunks_metadata_only
      :type: List[Any]
      
      Metadata-only list of attached files

   .. py:attribute:: attached_folders
      :type: List[Any]
      
      List of attached folders (old format)

   .. py:attribute:: attached_folders_new
      :type: List[Any]
      
      List of attached folders (new format)

   .. py:attribute:: attached_folders_list_dir_results
      :type: List[Any]
      
      Results from listing directory contents

   .. py:attribute:: attached_human_changes
      :type: bool
      
      Whether human changes were attached

   .. py:attribute:: human_changes
      :type: List[Any]
      
      List of human-made changes

   .. py:attribute:: cursor_rules
      :type: List[Any]
      
      List of cursor rules applied

   .. py:attribute:: knowledge_items
      :type: List[Any]
      
      List of knowledge items referenced

   .. py:attribute:: docs_references
      :type: List[Any]
      
      Documentation references

   .. py:attribute:: web_references
      :type: List[Any]
      
      Web page references

   .. py:attribute:: ai_web_search_results
      :type: List[Any]
      
      Results from AI web searches

   .. py:attribute:: external_links
      :type: List[Any]
      
      External links included in context

Code and Diffs
~~~~~~~~~~~~~~

   .. py:attribute:: suggested_code_blocks
      :type: List[Any]
      
      Code blocks suggested by the AI

   .. py:attribute:: user_responses_to_suggested_code_blocks
      :type: List[Any]
      
      User interactions with suggested blocks

   .. py:attribute:: assistant_suggested_diffs
      :type: List[Any]
      
      Diffs suggested by the assistant

   .. py:attribute:: diffs_since_last_apply
      :type: List[Any]
      
      File diffs that occurred since last apply

   .. py:attribute:: git_diffs
      :type: List[Any]
      
      Git diff information

   .. py:attribute:: file_diff_trajectories
      :type: List[Any]
      
      History of file diff changes

   .. py:attribute:: diff_histories
      :type: List[Any]
      
      Complete history of diffs

   .. py:attribute:: diffs_for_compressing_files
      :type: List[Any]
      
      Diffs used for file compression

   .. py:attribute:: codebase_context_chunks
      :type: List[Any]
      
      Chunks of codebase used as context

Linting and Errors
~~~~~~~~~~~~~~~~~~

   .. py:attribute:: lints
      :type: List[Any]
      
      List of linting errors/warnings

   .. py:attribute:: approximate_lint_errors
      :type: List[Any]
      
      Approximate count of lint errors

   .. py:attribute:: multi_file_linter_errors
      :type: List[Any]
      
      Linter errors across multiple files

Terminal and Tools
~~~~~~~~~~~~~~~~~~

   .. py:attribute:: terminal_files
      :type: List[Any]
      
      Files related to terminal commands

   .. py:attribute:: existed_previous_terminal_command
      :type: bool
      
      Whether there was a previous terminal command

   .. py:attribute:: existed_subsequent_terminal_command
      :type: bool
      
      Whether there was a subsequent terminal command

   .. py:attribute:: interpreter_results
      :type: List[Any]
      
      Results from code interpreter

   .. py:attribute:: tool_results
      :type: List[Any]
      
      Results from various tools

   .. py:attribute:: supported_tools
      :type: List[Any]
      
      List of tools that are supported

Version Control
~~~~~~~~~~~~~~~

   .. py:attribute:: commits
      :type: List[Any]
      
      List of git commits referenced

   .. py:attribute:: pull_requests
      :type: List[Any]
      
      List of pull requests referenced

UI and Capabilities
~~~~~~~~~~~~~~~~~~~

   .. py:attribute:: capabilities
      :type: List[Any]
      
      List of available capabilities

   .. py:attribute:: capability_statuses
      :type: Dict[str, Any]
      
      Dictionary of capability statuses. Common keys include:
      
      - ``mutate-request``
      - ``start-submit-chat``
      - ``before-submit-chat``
      - ``chat-stream-finished``
      - ``before-apply``
      - ``after-apply``
      - ``accept-all-edits``
      - ``composer-done``
      - ``process-stream``
      - ``add-pending-action``

   .. py:attribute:: capability_contexts
      :type: List[Any]
      
      Context for capabilities

   .. py:attribute:: ui_element_picked
      :type: List[Any]
      
      UI elements that were picked/selected

   .. py:attribute:: notepads
      :type: List[Any]
      
      Notepads associated with this bubble

   .. py:attribute:: recent_locations_history
      :type: List[Any]
      
      History of recent file locations

   .. py:attribute:: recently_viewed_files
      :type: List[Any]
      
      List of recently viewed files

Project and Layout
~~~~~~~~~~~~~~~~~~

   .. py:attribute:: project_layouts
      :type: List[Any]
      
      Layout information for the project

   .. py:attribute:: relevant_files
      :type: List[Any]
      
      Files relevant to this conversation

Composer Integration
~~~~~~~~~~~~~~~~~~~~

   .. py:attribute:: summarized_composers
      :type: List[Any]
      
      Composers that have been summarized

   .. py:attribute:: edit_trail_contexts
      :type: List[Any]
      
      Context from edit trails

   .. py:attribute:: all_thinking_blocks
      :type: List[Any]
      
      All thinking/reasoning blocks

   .. py:attribute:: context_pieces
      :type: List[Any]
      
      Additional context pieces

Metadata
~~~~~~~~

   .. py:attribute:: is_agentic
      :type: bool
      
      Whether this is an agentic conversation

   .. py:attribute:: is_refunded
      :type: bool
      
      Whether this conversation was refunded

   .. py:attribute:: is_nudge
      :type: bool
      
      Whether this is a nudge message

   .. py:attribute:: is_quick_search_query
      :type: bool
      
      Whether this is a quick search

   .. py:attribute:: is_plan_execution
      :type: bool
      
      Whether this is part of plan execution

   .. py:attribute:: use_web
      :type: bool
      
      Whether web search was enabled

   .. py:attribute:: unified_mode
      :type: Optional[int]
      
      Unified mode setting (integer)

   .. py:attribute:: edit_tool_supports_search_and_replace
      :type: bool
      
      Whether edit tool supports search/replace

   .. py:attribute:: skip_rendering
      :type: bool
      
      Whether to skip rendering this bubble

   .. py:attribute:: token_count
      :type: Dict[str, int]
      
      Dictionary with token counts. Contains:
      
      - ``inputTokens``: Number of input tokens
      - ``outputTokens``: Number of output tokens

   .. py:attribute:: model_info
      :type: Optional[Dict[str, Any]]
      
      Information about the AI model used. Contains:
      
      - ``modelName``: Name of the model

   .. py:attribute:: console_logs
      :type: List[Any]
      
      Console log entries

   .. py:attribute:: todos
      :type: List[Any]
      
      List of todos/action items

   .. py:attribute:: deleted_files
      :type: List[Any]
      
      List of files that were deleted

   .. py:attribute:: images
      :type: List[Any]
      
      List of images attached

   .. py:attribute:: documentation_selections
      :type: List[Any]
      
      Documentation selections

Properties
~~~~~~~~~~

   .. py:method:: input_tokens() -> Optional[int]
      
      Get the number of input tokens.

   .. py:method:: output_tokens() -> Optional[int]
      
      Get the number of output tokens.

   .. py:method:: model_name() -> Optional[str]
      
      Get the model name used for this conversation.

MessageRequestContext
---------------------

Context information for message requests.

**Key format:** ``messageRequestContext:<bubble_id>:<message_id>``

.. autoclass:: cursordata.cursordiskkv_models.MessageRequestContext
   :members:
   :undoc-members:
   :show-inheritance:

Checkpoint
----------

Saved states of files at a particular point in time.

**Key format:** ``checkpointId:<bubble_id>:<checkpoint_id>``

.. autoclass:: cursordata.cursordiskkv_models.Checkpoint
   :members:
   :undoc-members:
   :show-inheritance:

CodeBlockDiff
-------------

Code block differences between versions.

**Key format:** ``codeBlockDiff:<bubble_id>:<diff_id>``

.. autoclass:: cursordata.cursordiskkv_models.CodeBlockDiff
   :members:
   :undoc-members:
   :show-inheritance:

ComposerData
------------

Composer session data.

**Key format:** ``composerData:<composer_id>``

.. autoclass:: cursordata.cursordiskkv_models.ComposerData
   :members:
   :undoc-members:
   :show-inheritance:

InlineDiffs
------------

Inline diff data for workspaces.

**Key format:** ``inlineDiffs-<workspace_id>``

.. autoclass:: cursordata.cursordiskkv_models.InlineDiffs
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Getting Bubble Conversations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Get all bubble conversations
       bubbles = client.get_bubble_conversations(limit=10)
       
       for bubble in bubbles:
           print(f"Bubble: {bubble.bubble_id}")
           print(f"  Text: {bubble.text}")
           print(f"  Created: {bubble.created_at}")
           print(f"  Model: {bubble.model_name}")
           print(f"  Input tokens: {bubble.input_tokens}")
           print(f"  Output tokens: {bubble.output_tokens}")
           print(f"  Is agentic: {bubble.is_agentic}")
           print(f"  Code blocks: {len(bubble.suggested_code_blocks)}")
           print(f"  Diffs: {len(bubble.diffs_since_last_apply)}")
       
       # Get conversations for a specific bubble
       bubble_id = "461c2e93-144c-4289-b946-be34bab5b6e1"
       bubbles = client.get_bubble_conversations(bubble_id=bubble_id)

Getting Message Request Contexts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       contexts = client.get_message_request_contexts(limit=10)
       
       for ctx in contexts:
           print(f"Linter errors: {len(ctx.multi_file_linter_errors)}")
           print(f"Deleted files: {len(ctx.deleted_files)}")
           print(f"Diffs: {len(ctx.diffs_since_last_apply)}")

Getting Checkpoints
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       checkpoints = client.get_checkpoints(limit=10)
       
       for checkpoint in checkpoints:
           print(f"Files: {len(checkpoint.files)}")
           print(f"Non-existent files: {len(checkpoint.non_existent_files)}")
           print(f"New folders: {len(checkpoint.newly_created_folders)}")

Getting Composer Data
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       composer_data = client.get_composer_data(limit=10)
       
       for cd in composer_data:
           print(f"Composer ID: {cd.composer_id}")
           print(f"Text: {cd.text[:100]}")
           print(f"Status: {cd.status}")
           print(f"Newly created files: {len(cd.newly_created_files)}")

Getting a Specific Entry
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cursordata import CursorDataClient

   with CursorDataClient() as client:
       # Get a specific entry by key
       entry = client.get_cursordiskkv_entry(
           "bubbleId:461c2e93-144c-4289-b946-be34bab5b6e1:abc123"
       )
       
       if isinstance(entry, BubbleConversation):
           print(f"Bubble: {entry.bubble_id}")
           print(f"Text: {entry.text}")

