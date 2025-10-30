CursorData SDK Documentation
==============================

.. admonition:: Important Disclaimer
   :class: danger

   **This is an unofficial project** not connected with or endorsed by AnySphere (Cursor). 
   This SDK is developed independently and provided as-is. Use at your own risk. 
   The Cursor editor and its database structure are property of AnySphere.

Welcome to the CursorData SDK documentation! This SDK provides a Python interface
for accessing and analyzing Cursor editor's local SQLite usage data database.

Documentation Sections
======================

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   installation
   quickstart
   api
   cursordiskkv
   contributing

Class Overview
==============

This section provides a high-level overview of the main classes in the SDK. For detailed API documentation, see :doc:`api`.

Core Classes
------------

:class:`cursordata.client.CursorDataClient`
   The main client class for interacting with the Cursor database. Provides methods to query usage data, 
   composer sessions, bubble conversations, and more. Automatically detects database location on macOS, 
   Windows, and Linux.

:class:`cursordata.query.QueryBuilder`
   A fluent query builder interface for constructing complex queries across bubbles, composer sessions, 
   and AI code tracking entries with filtering, sorting, and limiting capabilities.

Data Models - ItemTable
------------------------

These models represent data from the ItemTable:

:class:`cursordata.models.AICodeTrackingEntry`
   Individual AI-assisted code change entries with metadata about source, file, and composer session.

:class:`cursordata.models.UsageStats`
   Aggregated statistics including total entries, scored commits, and file extension usage.

:class:`cursordata.models.ComposerSession`
   Groups related code changes from multi-file editing sessions with associated files and metadata.

:class:`cursordata.models.DatabaseInfo`
   Information about the database file including location, entry counts, and last modified time.

Data Models - cursorDiskKV
---------------------------

These models represent structured conversation and code data from cursorDiskKV. For detailed 
documentation, see :doc:`cursordiskkv`.

:class:`cursordata.cursordiskkv_models.BubbleConversation`
   Conversation data stored in bubbles with structured message and context information.

:class:`cursordata.cursordiskkv_models.ComposerData`
   Multi-file editing session data including code blocks, diffs, and metadata.

:class:`cursordata.cursordiskkv_models.MessageRequestContext`
   Context information associated with message requests including files, code, and metadata.

:class:`cursordata.cursordiskkv_models.CodeBlockDiff`
   Represents code block changes and diffs within conversations.

:class:`cursordata.cursordiskkv_models.Checkpoint`
   Checkpoint data representing saved states in conversations.

:class:`cursordata.cursordiskkv_models.InlineDiffs`
   Inline code diff information showing changes within code blocks.

Collections
-----------

Collection classes that provide type-safe, iterable access to groups of related data models:

:class:`cursordata.collections.BubbleCollection`
   Type-safe collection of :class:`cursordata.cursordiskkv_models.BubbleConversation` objects with 
   filtering and querying capabilities.

:class:`cursordata.collections.ComposerSessionCollection`
   Type-safe collection of :class:`cursordata.models.ComposerSession` objects with 
   filtering and querying capabilities.

:class:`cursordata.collections.AICodeTrackingCollection`
   Type-safe collection of :class:`cursordata.models.AICodeTrackingEntry` objects with 
   filtering and querying capabilities.

Enums
-----

:class:`cursordata.models.DatabaseLocation`
   Enum for platform-specific database paths (macOS, Windows, Linux).

:class:`cursordata.models.ItemTableKey`
   Enum of known keys in the ItemTable for direct database access.

Getting Started
===============

For installation instructions, see :doc:`installation`.

For examples and common use cases, see :doc:`quickstart`.

For complete API documentation, see :doc:`api`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

