# Development & Contribution Guide

1. **Branching Strategy**: Create feature branches from `main` (e.g. `feat/your-feature`).
2. **Local Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Running Gateway Locally**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. **Pre-Commit Verification**: Run pytest and ruff before submitting PRs:
   ```bash
   pytest
   ```
