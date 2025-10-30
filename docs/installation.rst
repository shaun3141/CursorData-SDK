Installation
============

The CursorData SDK can be installed using pip or uv.

Using pip
---------

.. code-block:: bash

   pip install cursordata-sdk

Using uv
--------

.. code-block:: bash

   uv pip install cursordata-sdk

Development Installation
------------------------

To install in development mode with all dependencies:

.. code-block:: bash

   git clone https://github.com/shaun3141/CursorData-SDK.git
   cd CursorData-SDK
   uv pip install -e ".[dev,docs]"

Requirements
------------

- Python 3.8 or higher
- SQLite3 (usually included with Python)

Platform Support
----------------

The SDK automatically detects the Cursor database location on:

- **macOS**: ``~/Library/Application Support/Cursor/User/globalStorage/state.vscdb``
- **Windows**: ``%APPDATA%\\Cursor\\User\\globalStorage\\state.vscdb``
- **Linux**: ``~/.config/Cursor/User/globalStorage/state.vscdb``

You can also specify a custom database path when initializing the client:

.. code-block:: python

   from cursordata import CursorDataClient

   client = CursorDataClient(db_path="/custom/path/to/state.vscdb")

