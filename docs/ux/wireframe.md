# Wireframe - CutFlow Main Interface

## Layout Overview

```
+---------------------------------------------------------------+
| Menu Bar: File Edit View Export Help                          |
+---------------------------------------------------------------+
| Toolbar: [Import] [Export] [Undo] [Redo] [Settings]           |
+---------------------------------------------------------------+
|                                                               |
|  +-------------------+  +-----------------------------------+  |
|  |                   |  |                                   |  |
|  |  Metadata Panel  |  |        Video Player                |  |
|  |                   |  |                                   |  |
|  |  - File Name     |  |   [Play/Pause] [Stop]              |  |
|  |  - Duration      |  |                                   |  |
|  |  - Resolution    |  |                                   |  |
|  |  - Codec         |  |                                   |  |
|  |  - Bitrate       |  |                                   |  |
|  |                   |  |                                   |  |
|  +-------------------+  +-----------------------------------+  |
|  |                   |  |                                   |  |
|  |  Filter Panel    |  |                                   |  |
|  |                   |  |                                   |  |
|  |  Brightness: [===|==] |                                   |  |
|  |  Contrast:   [===|==] |                                   |  |
|  |  Saturation: [===|==] |                                   |  |
|  |  [Add Filter]     |  |                                   |  |
|  |                   |  |                                   |  |
|  +-------------------+  +-----------------------------------+  |
|  |                   |  |  Timeline                          |  |
|  |  Export Panel    |  |  +----------------------------+  |  |
|  |                   |  |  | 00:00  00:30  01:00  01:30|  |  |
|  |  Preset: [▼]      |  |  +----------------------------+  |  |
|  |  Format: [▼]      |  |  | [Track]                       |  |  |
|  |  Mode:   [▼]      |  |  |   I_____________O             |  |  |
|  |  CRF:    [23]     |  |  |        |                      |  |  |
|  |  [Export]         |  |  +----------------------------+  |  |
|  |                   |  |  [Zoom: ===|===] [Set In] [Set Out]|  |
|  +-------------------+  +-----------------------------------+  |
|                                                               |
+---------------------------------------------------------------+
| Status Bar: Ready | Export: 0 jobs | Duration: 00:00 / 00:00 |
+---------------------------------------------------------------+
```

## Component Details

### Menu Bar
```
File
├── Import Video... (Ctrl+I)
├── Open Project... (Ctrl+O)
├── Save Project (Ctrl+S)
├── Save Project As... (Ctrl+Shift+S)
├── Export (Ctrl+E)
├── Export Queue
└── Quit (Ctrl+Q)

Edit
├── Undo (Ctrl+Z)
├── Redo (Ctrl+Y)
├── Clear Markers
└── Preferences...

View
├── Toggle Timeline (T)
├── Toggle Filters (F)
├── Toggle Metadata (M)
├── Zoom In (+)
├── Zoom Out (-)
└── Reset Zoom (R)

Export
├── Quick Export (Ctrl+E)
├── Export with Settings (Ctrl+Shift+E)
└── Export Queue

Help
├── Keyboard Shortcuts (F1)
├── Documentation
└── About
```

### Toolbar
```
[Import] [Export] [Undo] [Redo] [Export Queue] [Settings]
```

### Metadata Panel
```
+-------------------+
| Video Information |
+-------------------+
| File: video.mp4   |
| Duration: 02:30   |
| Resolution: 1920x1080 |
| Codec: H.264       |
| FPS: 60            |
| Bitrate: 8 Mbps    |
+-------------------+
```

### Filter Panel
```
+-------------------+
| Filters           |
+-------------------+
| Brightness: [====]|
| Contrast:   [====]|
| Saturation: [====]|
| Hue:        [====]|
| Gamma:      [====]|
+-------------------+
| [Add Advanced]    |
+-------------------+
```

### Export Panel
```
+-------------------+
| Export Settings   |
+-------------------+
| Preset: [▼]       |
|   YouTube 1080p   |
|   YouTube 720p    |
|   WhatsApp        |
|   Instagram       |
|   TikTok          |
|   Custom...        |
+-------------------+
| Mode: [▼]         |
|   Stream Copy     |
|   Reencode        |
+-------------------+
| CRF: [23]         |
| Preset: [▼]       |
|   Ultrafast       |
|   Superfast       |
|   Veryfast        |
|   Faster          |
|   Fast            |
|   Medium          |
|   Slow            |
|   Slower          |
|   Veryslow        |
+-------------------+
| [Export]          |
+-------------------+
```

### Timeline
```
+--------------------------------------------------+
| 00:00  00:15  00:30  00:45  01:00  01:15  01:30 |
+--------------------------------------------------+
| [Video Track]                                    |
|  I____________________________O                  |
|        |                                       |
+--------------------------------------------------+
| [Zoom: =====] [Set In (I)] [Set Out (O)] [Clear]|
+--------------------------------------------------+
```

### Export Queue Dialog
```
+-----------------------------------------------+
| Export Queue                        [X]        |
+-----------------------------------------------+
| Job 1: video.mp4 -> output.mp4                 |
| Status: Exporting... ████████░░ 80%            |
| Time remaining: 00:30                         |
| [Cancel]                                      |
+-----------------------------------------------+
| Job 2: video.mp4 -> tiktok.mp4                |
| Status: Pending                                |
| [Remove]                                      |
+-----------------------------------------------+
| Job 3: video.mp4 -> instagram.mp4             |
| Status: Completed ✓                            |
| [Open] [Remove]                               |
+-----------------------------------------------+
| [Export All] [Clear Completed]                 |
+-----------------------------------------------+
```

### Export Dialog (Advanced)
```
+-----------------------------------------------+
| Export Settings                    [X]        |
+-----------------------------------------------+
| Output: [Browse...] output.mp4                  |
+-----------------------------------------------+
| Video                                        |
| Codec: [libx264 ▼]                            |
| Bitrate: [8M]                                 |
| CRF: [23]                                     |
| Preset: [medium ▼]                            |
| Resolution: [1920x1080]                        |
+-----------------------------------------------+
| Audio                                        |
| Codec: [aac ▼]                               |
| Bitrate: [192k]                               |
| Sample Rate: [48000 ▼]                        |
+-----------------------------------------------+
| Filters                                      |
| [Apply Filter Chain]                          |
+-----------------------------------------------+
| [Export] [Cancel]                             |
+-----------------------------------------------+
```

## Design Tokens

### Colors (Dark Theme)
- Background: #1e1e1e
- Panel: #2e2e2e
- Border: #3e3e3e
- Text Primary: #e0e0e0
- Text Secondary: #a0a0a0
- Accent: #2196F3
- Success: #4CAF50
- Warning: #FF9800
- Error: #f44336
- In Marker: #4CAF50 (green)
- Out Marker: #f44336 (red)
- Position: #2196F3 (blue)

### Typography
- Font Family: Segoe UI, Roboto, Arial, sans-serif
- Font Size: 12px (base), 14px (labels), 16px (headers)
- Line Height: 1.5

### Spacing
- Padding: 8px (small), 16px (medium), 24px (large)
- Gap: 8px (small), 16px (medium)
- Border Radius: 4px (small), 8px (medium)

### Components
- Button Height: 32px
- Input Height: 32px
- Slider Height: 20px
- Timeline Height: 120px
- Player Minimum Height: 400px
