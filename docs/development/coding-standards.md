# Coding Standards & Best Practices

1. **PEP 8 Compliance**: Follow standard Python naming conventions (`snake_case` for variables/functions, `PascalCase` for classes).
2. **Explicit Type Annotations**: All function signatures must include Python type hints.
3. **Docstrings**: Public functions and classes must include concise docstrings explaining inputs and outputs.
4. **SQLAlchemy 2.x Styles**: Use `select()` and `async_sessionmaker`. Avoid 1.x legacy ORM session queries.
5. **Exception Handling**: Raise domain exceptions defined in `app/core/exceptions.py` rather than generic `RuntimeError`.
