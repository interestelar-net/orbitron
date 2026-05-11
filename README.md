# Orbitron

Orbitron is a minimal Discord bot written with `discord.py`. It loads the bot token from a `.env` file and starts from `src/main.py`.

**Status:** Initial base — simple structure with extension support in `src/extensions`.

**Summary:**
- Language: Python
- Main library: `discord.py`
- ORM/DB layer: `SQLAlchemy` (async)

**Requirements**
- Python 3.11 or newer
- Dependencies listed in `requirements.txt`

## Installation and usage
1. Create and activate a virtual environment (recommended):

PowerShell (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Command Prompt (Windows):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Linux / macOS (bash/zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env` and add the `DISCORD_TOKEN` value for your bot.

4. Run the bot:

```bash
python src/main.py
```

## Project structure (relevant files)
- `src/main.py` — entry point
- `src/extensions/` — folder for bot extensions/handlers
- `src/services/database/database.py` — async SQLAlchemy engine/session/base service
- `.env.example` — example environment variables

## Contributing
- Open an issue or submit a pull request describing the proposed changes.

## License
- See the `LICENSE` file in the repository.
