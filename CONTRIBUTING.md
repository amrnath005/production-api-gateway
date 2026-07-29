# Contributing Guidelines

Thank you for your interest in contributing to the **Production FastAPI API Gateway**!

## How to Contribute

1. **Fork the Repository**: Create your feature branch off of `main`.
2. **Set Up Local Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Run Unit Tests**: Ensure all 29 tests pass before opening a PR:
   ```bash
   pytest
   ```
4. **Code Style & Formatting**: Follow PEP 8 guidelines, use explicit type hints on all public functions, and provide comprehensive docstrings.
5. **Open a Pull Request**: Submit a clear PR describing your changes and linking to relevant issue tickets.
