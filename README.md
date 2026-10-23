# CutFlow

Desktop video editor for cutting, merging, and converting videos.

## Features

- **Video Playback**: Play video files with controls (play/pause, seek, volume)
- **Timeline**: Visual timeline with In/Out markers for precise cutting
- **Zoom & Scrubbing**: Zoom timeline and scrub through video
- **Keyboard Shortcuts**: I/O keys for In/Out points
- **Export**: Export clips with FFmpeg (MP4, WebM)
- **Export Queue**: Manage multiple export jobs with progress tracking
- **Filters**: Adjust brightness, contrast, saturation, hue, gamma
- **Projects**: Save and load projects
- **Undo/Redo**: Full undo/redo support for actions
- **Modern UI**: Dark/light theme with clean interface

## Requirements

- Python 3.11+
- FFmpeg (must be installed on system)

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/avimax.git
cd avimax

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run linter
ruff check .

# Run type checker
mypy cutflow
```

## Running

```bash
# From virtual environment
python -m cutflow.app.main

# Or using the installed script
cutflow
```

## Building Executable

```bash
# Install packaging dependencies
pip install -e ".[packaging]"

# Build with PyInstaller
pyinstaller cutflow.spec --clean
```

The executable will be in `dist/CutFlow`.

**Note:** The built executable requires FFmpeg to be installed on the target system.

## Tech Stack

- **Python 3.11+**: Core language
- **PySide6**: Qt6 GUI framework
- **FFmpeg**: Video processing (subprocess)
- **Hatchling**: Build system
- **PyInstaller**: Packaging

## Project Structure

```
cutflow/
├── app/                    # Application entry point
│   ├── main.py            # Main entry point
│   └── config.py          # Configuration management
├── domain/                 # Domain models
│   ├── models/            # Business models (Clip, Project, ExportJob, Filter)
│   └── value_objects/     # Value objects (VideoMetadata)
├── services/              # Business logic
│   ├── probe_service.py   # FFprobe integration
│   ├── export_service.py  # FFmpeg export
│   └── undo_redo_service.py # Undo/redo management
├── ui/                    # User interface
│   ├── styles/            # Themes (dark/light)
│   ├── views/             # Main window
│   └── widgets/           # Custom widgets (Player, Timeline, Filters, ExportQueue)
└── __init__.py
```

## Keyboard Shortcuts

- **Ctrl+O**: Open file
- **Ctrl+E**: Export clip
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **I**: Set In point
- **O**: Set Out point
- **Space**: Play/Pause

## License

MIT License

