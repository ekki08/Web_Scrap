# Web Scraping Project

A small Python web-scraping framework with lightweight spiders, a simple scheduler, storage, and logging utilities.

## Features

- Base spider (`BaseSpider`) and example spider (`KeywordSpider`) that search pages for keywords.
- Centralized logger in `core/Logger_manager.py`.
- Simple local storage under `wb_storage/` for JSON/CSV outputs.
- Minimal scheduler and request utilities in `core/`.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (requests, beautifulsoup4):

```powershell
pip install -r requirements.txt
```

If you don't have `requirements.txt`, install manually:

```powershell
pip install requests beautifulsoup4
```

3. Run the example spider (from project root):

```powershell
# Run as a module (recommended)
python -m spiders.example_spiders

# Or run the top-level example script
python example_spiders.py
```

Note: `spiders/example_spiders.py` performs a sys.path fix so imports still work when running the file directly, but running as a module is cleaner for package-style imports.

## Project layout

- `core/` - core modules like `Logger_manager.py`, `scheduler.py`, `request_manager.py`, `storage.py`.
- `spiders/` - spider implementations (e.g., `example_spiders.py`).
- `wb_storage/` - local output (ignored by git by default).
- `logs/` - runtime logs (ignored by git by default).
- `test_scheduler.py` - quick test for the scheduler.

## Notes and troubleshooting

- If you see `ModuleNotFoundError: No module named 'Logger_manager'`, run spiders as a module from the project root (see commands above) or ensure Python's `sys.path` includes the project root. The code already tries to handle both cases.
- If a spider's `parse()` returns `None` or a single dict, the framework normalizes results so `BaseSpider` collects them consistently.
- Consider renaming `Logger_manager.py` to `logger_manager.py` to follow PEP8 module naming.


