# Developer Guide

## Introduction
This guide is for extending the (English-only) Python Data Analytics Software.

## Project Structure
- `src/`: Main source code (core, ui, utils).
- `docs/`: Documentation (user_manual.md, this guide).
- `tests/`: Unit tests.
- `examples/`: Sample data and scripts.
- `main.py` (in `src/`): Application entry point.
- `requirements.txt`: Dependencies.

## Setting up Development Environment
1.  Generate repository.
2.  Navigate to project root.
3.  Create/activate virtual environment.
4.  `pip install -r requirements.txt`
5.  (Optional) `pip install pytest`

## Running the Application
From project root: `python src/main.py` or `python -m src.main`

## Extending the Codebase

### Adding a New Statistical Method
1.  **Core Logic**: Implement in `src/core/`. Handle NaNs/non-numeric data.
2.  **UI Integration**: Add UI element (button/menu) in `src/ui/main_window.py`. Connect to method calling core function. Display results/plot.
3.  **Unit Tests**: Add to `tests/`.
4.  **Documentation**: Update `docs/user_manual.md` and this guide.

## Key Modules
- `src/main.py`: Entry point.
- `src/ui/main_window.py`: Main UI class.
- `src/utils/settings_manager.py`: Manages `config.json` (no language settings now).
- `src/utils/data_handler.py`: Data loading.
- `src/utils/plotting.py`: Matplotlib helpers.
- `src/utils/report_generator.py`: PDF reports.

## Running Tests
- `pip install pytest` (if not done).
- From project root: `pytest`
