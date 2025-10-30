Contributing Guide
==================

Thank you for your interest in contributing to the CursorData SDK! This guide will help you get started with contributing to the project.

Setting Up Development Environment
----------------------------------

First, clone the repository and set up your development environment:

.. code-block:: bash

   git clone https://github.com/shaun3141/CursorData-SDK.git
   cd CursorData-SDK
   uv pip install -e ".[dev,docs]"

Development Dependencies
------------------------

The project uses the following tools for development:

- **pytest**: Testing framework
- **black**: Code formatter
- **ruff**: Linter
- **mypy**: Type checker
- **sphinx**: Documentation generator

Running Tests
-------------

Run the test suite using pytest:

.. code-block:: bash

   pytest

To run with coverage:

.. code-block:: bash

   pytest --cov=src/cursordata --cov-report=html

Code Quality
------------

Before submitting a pull request, ensure your code follows the project's style guidelines:

Format your code with black:

.. code-block:: bash

   black src/

Lint your code with ruff:

.. code-block:: bash

   ruff check src/
   ruff check --fix src/  # Auto-fix issues when possible

Type check with mypy:

.. code-block:: bash

   mypy src/

Documentation
-------------

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

- Use Google-style docstrings for all classes, methods, and functions
- Include type hints for all parameters and return values
- Provide clear descriptions of what functions do
- Include examples in docstrings when helpful
- Document any exceptions that may be raised

Building Documentation Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The documentation will be generated in ``docs/_build/html/``. Open ``index.html`` in your browser to view it.

Adding New Documentation Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a new ``.rst`` file in the ``docs/`` directory
2. Add it to the table of contents in ``docs/index.rst`` under the ``.. toctree::`` directive
3. Rebuild the documentation to verify it appears correctly

Testing Documentation
~~~~~~~~~~~~~~~~~~~~~~

The documentation includes doctest examples that are automatically tested. To run doctests:

.. code-block:: bash

   cd docs
   make doctest

Adding Executable Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

When adding code examples to documentation, you can make them executable by using the ``.. doctest::`` directive:

.. code-block:: rst

   .. doctest::

      >>> from cursordata import CursorDataClient
      >>> client = CursorDataClient()
      >>> stats = client.get_usage_stats()
      >>> stats.total_tracking_entries >= 0
      True
      >>> client.close()

Note: Be careful with doctest examples that require database access, as they may not work in all environments.

API Documentation
~~~~~~~~~~~~~~~~~~

API documentation is automatically generated from docstrings using Sphinx autodoc. Make sure your docstrings follow the Google style:

.. code-block:: python

   def example_function(param1: str, param2: int = 10) -> bool:
       """Brief description of the function.
       
       Longer description explaining what the function does,
       when to use it, and any important details.
       
       Args:
           param1: Description of the first parameter.
           param2: Description of the second parameter. Defaults to 10.
       
       Returns:
           Description of the return value.
       
       Raises:
           ValueError: When invalid input is provided.
       
       Example:
           >>> result = example_function("test", 20)
           >>> result
           True
       """
       # Implementation here
       pass

Submitting Changes
------------------

1. Create a new branch for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and ensure all tests pass:

   .. code-block:: bash

      pytest
      black src/
      ruff check src/
      mypy src/

3. Commit your changes with a clear, descriptive commit message:

   .. code-block:: bash

      git commit -m "Add feature: description of changes"

4. Push your branch and create a pull request on GitHub

5. Ensure your pull request includes:
   - A clear description of the changes
   - Tests for new functionality (if applicable)
   - Updated documentation (if applicable)
   - Passing CI checks

Pull Request Checklist
----------------------

Before submitting a pull request, make sure:

- [ ] All tests pass locally
- [ ] Code is formatted with black
- [ ] No linting errors (ruff)
- [ ] Type checking passes (mypy)
- [ ] Documentation is updated if needed
- [ ] New features have appropriate tests
- [ ] Commit messages are clear and descriptive

Code Style Guidelines
----------------------

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Keep functions focused and single-purpose
- Write docstrings for all public functions, classes, and methods
- Use meaningful variable and function names
- Keep line length to 100 characters (as configured in black/ruff)

Type Hints
~~~~~~~~~~

Always include type hints:

.. code-block:: python

   def process_data(
       entries: List[AICodeTrackingEntry],
       filter_by_source: Optional[str] = None,
   ) -> Dict[str, int]:
       """Process tracking entries and return statistics."""
       # Implementation
       pass

Testing Guidelines
------------------

- Write tests for new functionality
- Aim for good test coverage
- Use descriptive test names
- Group related tests using pytest fixtures when appropriate
- Test edge cases and error conditions

Example test structure:

.. code-block:: python

   import pytest
   from cursordata import CursorDataClient

   def test_get_usage_stats():
       """Test that usage stats are returned correctly."""
       with CursorDataClient() as client:
           stats = client.get_usage_stats()
           assert isinstance(stats.total_tracking_entries, int)
           assert stats.total_tracking_entries >= 0

Questions?
----------

If you have questions about contributing, please:

1. Check the existing documentation
2. Review open and closed issues on GitHub
3. Open a new issue with your question

Thank you for contributing to the CursorData SDK!

