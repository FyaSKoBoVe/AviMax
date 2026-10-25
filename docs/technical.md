# Technical Documentation

## Architecture Overview

CutFlow follows the Model-View-ViewModel (MVVM) architecture pattern with clear separation of concerns:

```
cutflow/
├── app/                    # Application entry point and dependency injection
│   ├── main.py            # Main entry point
│   ├── dependencies.py    # Dependency container
│   └── config.py          # Application configuration
├── domain/                # Business logic and domain models
│   ├── models/            # Domain models (Project, Clip, Filter, Segment, etc.)
│   ├── commands/          # Command pattern for undo/redo
│   └── services/          # Domain services interfaces
├── infrastructure/        # External dependencies implementation
│   ├── ffmpeg/            # FFmpeg/FFprobe services
│   ├── repositories/      # Data persistence
│   └── export_queue.py    # Export queue service
├── ui/                    # User interface
│   ├── views/             # Qt views (MainWindow, dialogs)
│   ├── widgets/           # Custom widgets (Player, Timeline)
│   ├── panels/            # UI panels (Metadata, Filter, Export)
│   └── styles/            # Theming (QSS stylesheets)
├── viewmodels/            # ViewModels connecting UI to domain
│   ├── project_viewmodel.py
│   ├── player_viewmodel.py
│   └── export_viewmodel.py
└── i18n/                  # Internationalization
    └── translator.py      # Translation loader
```

## Domain Models

### Project
Represents a video editing project with clips, filters, and metadata.

```python
@dataclass
class Project:
    name: str
    clips: list[Clip]
    filter_chain: FilterChain
    created_at: datetime
    modified_at: datetime
    file_path: Path | None
```

### Clip
Represents a video file with metadata.

```python
@dataclass
class Clip:
    id: str
    file_path: Path
    metadata: VideoMetadata
```

### Filter
Represents a video filter with parameters.

```python
@dataclass
class Filter:
    type: FilterType
    parameters: dict[str, float | str]
```

### Segment
Represents a time segment for cutting operations.

```python
@dataclass
class Segment:
    start_time: float
    end_time: float
    mode: SegmentMode  # STREAM_COPY or REENCODE
```

### ExportJob
Represents an export task in the queue.

```python
@dataclass
class ExportJob:
    id: str
    input_path: Path
    output_path: Path
    preset: ExportPreset
    status: ExportStatus
    progress: float
```

## Infrastructure Services

### FFmpegService
Handles video processing using FFmpeg.

**Methods:**
- `export_video()` - Export video with custom settings
- `cut_segment()` - Cut a segment from video
- `merge_clips()` - Concatenate multiple clips
- `get_version()` - Get FFmpeg version

### ProbeService
Extracts video metadata using FFprobe.

**Methods:**
- `probe()` - Extract metadata from video file
- Returns `VideoMetadata` object with duration, resolution, codec, etc.

### ExportQueue
Manages export jobs with progress tracking.

**Methods:**
- `add_job()` - Add export job to queue
- `start()` - Start processing queue
- `cancel_job()` - Cancel a specific job
- `clear_completed()` - Remove completed jobs

## ViewModels

### ProjectViewModel
Manages project state and clip operations.

**Signals:**
- `project_changed` - Emitted when project is modified
- `clip_added` - Emitted when clip is added
- `clip_removed` - Emitted when clip is removed

### PlayerViewModel
Manages video playback state.

**Signals:**
- `state_changed` - Emitted when player state changes
- `position_changed` - Emitted during playback
- `duration_changed` - Emitted when video duration changes

**States:**
- STOPPED, PLAYING, PAUSED

### ExportViewModel
Manages export operations and queue.

**Signals:**
- `job_added` - Emitted when export job is added
- `job_progress` - Emitted during export
- `job_completed` - Emitted when export finishes

## UI Components

### MainWindow
Main application window with menu bar, toolbar, and panels.

**Layout:**
- Left panel: Metadata, Filters, Export settings
- Right panel: Video player, Timeline

### PlayerWidget
Video player widget using QtMultimedia.

**Features:**
- Play/Pause/Stop controls
- Seek slider
- Time display

### TimelineWidget
Timeline with In/Out markers and zoom.

**Features:**
- Visual timeline representation
- In/Out marker placement
- Zoom control
- Position indicator

## Command Pattern

Undo/redo functionality using Command pattern.

**Available Commands:**
- `AddClipCommand` - Add clip to project
- `RemoveClipCommand` - Remove clip from project
- `AddFilterCommand` - Add filter to chain
- `RemoveFilterCommand` - Remove filter from chain

**Usage:**
```python
command = AddClipCommand(project, clip)
command_stack.execute(command)
command_stack.undo()
command_stack.redo()
```

## Export Presets

Pre-configured export settings for different platforms.

**Available Presets:**
- YouTube 1080p, 720p, 480p
- WhatsApp
- Instagram
- TikTok
- Custom

Each preset defines:
- Video codec
- Audio codec
- Resolution
- Bitrate
- CRF value
- FFmpeg preset

## Filters

### Basic Filters
- Brightness
- Contrast
- Saturation
- Hue
- Gamma

### Advanced Filters
- Crop (x, y, width, height)
- Resize (width, height)
- Rotate (degrees)
- Fade (in/out, duration)
- Volume (multiplier)

Filters are converted to FFmpeg filter strings automatically.

## Internationalization

Translation system using Qt Linguist (.ts/.qm files).

**Supported Languages:**
- English (en_US) - Source
- Italian (it_IT)

**Adding Translations:**
1. Use `self.tr()` or `QCoreApplication.translate()` in code
2. Run `pyside6-lupdate` to extract strings
3. Edit .ts files with Qt Linguist
4. Run `lrelease` to compile .qm files

## Configuration

Application configuration stored in user config directory.

**Config File:** `~/.config/cutflow/config.json`

**Settings:**
- FFmpeg path
- FFprobe path
- Theme preference
- Language preference

## Dependencies

**Required:**
- Python 3.11+
- PySide6 (Qt6 bindings)
- FFmpeg (external binary)
- FFprobe (external binary)

**Python Packages:**
- PySide6
- platformdirs
- pytest (for testing)

## Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Running Application
```bash
python -m cutflow.app.main
```

### Code Style
- Use ruff for linting
- Follow PEP 8
- Type hints required
- Docstrings for public APIs

## Performance Considerations

### Export Queue
- Exports run in background threads
- Progress updates via signals
- Multiple jobs can be queued

### Video Processing
- Stream copy mode for fast cuts (no re-encoding)
- Re-encode mode for quality control
- FFmpeg subprocess management

### Memory
- Video metadata cached in Clip objects
- Export jobs stored in memory queue
- Consider pagination for large projects

## Error Handling

### FFmpeg Errors
- Subprocess errors caught and reported
- FFmpeg detection on startup
- Fallback to system PATH

### File Operations
- Path validation before operations
- File existence checks
- Permission error handling

### Export Failures
- Job status updated to FAILED
- Error messages stored in job
- User can retry failed jobs

## Security

### File Access
- User must have read access to input files
- User must have write access to output directory
- No automatic file deletion

### Subprocess Execution
- FFmpeg/FFprobe paths validated
- No arbitrary command execution
- Input sanitization for FFmpeg args

## Future Enhancements

### Planned Features
- Audio waveform visualization
- Multi-track timeline
- Keyframe animation
- Project templates
- Batch processing
- Cloud storage integration

### Technical Debt
- Add integration tests
- Improve error messages
- Add logging system
- Optimize large file handling
- Add plugin system for filters
