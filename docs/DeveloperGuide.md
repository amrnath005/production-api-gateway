# Developer Setup & Contribution Guide

## 1. Local Environment Setup

1. **Clone Repository & Set Up Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

3. **Database Migrations**:
   Run Alembic migrations to set up local schema:
   ```bash
   alembic upgrade head
   ```

4. **Running Gateway Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 2. Test Execution
Run the full pytest suite:
```bash
pytest
```

## 3. Code Standards & Formatting
- Follow PEP 8 style guidelines.
- Use explicit type hints on all function signatures.
- Ensure all public functions have docstrings.
