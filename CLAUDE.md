# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Shodan Eye is a Python CLI tool that queries the Shodan API to collect information about internet-connected devices matching user-specified keywords. It displays IP, port, organization, location, transport layer, domains, hostnames, and banner data for each result.

## Running

```bash
pip3 install -r requirements.txt   # sole dependency: shodan
python3 shodan-eye.py
```

The tool is interactive — it prompts for: whether to save output to a file, and a search keyword. There are no command-line arguments.

## API Key Handling

Resolution order:
1. `SHODAN_API_KEY` environment variable (preferred)
2. `./api.txt` file (if it exists and is non-empty)
3. Interactive prompt via `getpass.getpass()` (key is then saved to `./api.txt`)

The `api.txt` file is gitignored. If authentication fails, the user is prompted to replace the key via `getpass` (input hidden cross-platform). The retry logic is a `while True` loop in `run()` — on failure, the user can enter a new key or decline to exit.

## Architecture

Single-file application (`shodan-eye.py`, ~220 lines). No module structure, no tests, no linting configuration.

Key functions:
- `run()` — main entry point, handles user interaction, search loop, and logging
- `get_api_key()` — resolves API key from env var, file, or user prompt

Key flow:
1. Display a random ASCII banner
2. Ask user about file output (with filename validation: alphanumeric, underscores, hyphens only)
3. Resolve API key via `get_api_key()`
4. Validate the key with a test query (`api.search("b00m")`)
5. Use `api.search_cursor()` to iterate results up to a hardcoded limit of 888
6. Print results to console and optionally write to a log file (opened once, closed in `finally`)

## Style Conventions

- ANSI color codes used throughout for terminal styling (red: `\033[1;31m`, blue: `\033[34m`)
- f-strings for all string formatting
- `with` statements for API key file I/O; log file uses `open()`/`close()` with `finally`
- `getpass.getpass()` for hidden input

## Files

- `shodan-eye.py` — the entire application
- `requirements.txt` — single dependency (`shodan`)
- `Shodan_Dorks_The_Internet_of_Sh*t.txt` — collection of example Shodan search queries/dorks
- `.gitignore` — excludes `api.txt`, `*.pyc`, `__pycache__/`
- `LICENSE` — GPL v3
- `README.md` — install/usage instructions and project links
- `img/` — screenshot assets for the README
- `api.txt` — created at runtime to store the Shodan API key (not in repo)
