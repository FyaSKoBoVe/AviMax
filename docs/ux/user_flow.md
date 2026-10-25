# User Flow for CutFlow

## Primary User Flow: Quick Video Cut

### Scenario: Marco wants to cut a gameplay highlight

**Step 1: Launch Application**
- User opens CutFlow
- Application detects FFmpeg automatically
- Onboarding overlay shows basic controls (first time only)

**Step 2: Import Video**
- User drags video file to main window
- OR clicks "Import" button and selects file
- FFprobe extracts metadata (duration, codec, resolution)
- Video loads in player
- Timeline shows full duration

**Step 3: Preview and Mark Segments**
- User plays video in player
- Uses keyboard shortcuts:
  - Space: Play/Pause
  - I: Set In point
  - O: Set Out point
  - Arrow keys: Frame-by-frame
- Timeline shows In (green) and Out (red) markers
- User can adjust markers by dragging on timeline

**Step 4: Apply Filters (Optional)**
- User opens Filter Panel
- Adjusts brightness/contrast if needed
- Adds fade in/out transitions

**Step 5: Export**
- User opens Export Panel
- Selects preset: "YouTube 1080p"
- Chooses mode: "Stream Copy" (fast) or "Reencode" (accurate)
- Clicks "Export" button
- Export job added to queue
- Progress bar shows completion
- Status bar shows "Exporting... 45%"

**Step 6: Complete**
- Export completes
- Status bar shows "Export complete"
- User can open output folder
- OR add another export job with different preset

## Secondary User Flow: Merge Multiple Clips

### Scenario: Alessandro wants to merge interview segments

**Step 1: Import Multiple Videos**
- User imports first video
- Video appears in project list
- User imports second video
- Video appears in project list

**Step 2: Arrange Order**
- User selects clips in desired order
- Drag-and-drop to reorder (future feature)

**Step 3: Export Merge**
- User selects "Merge Clips" option
- Chooses output format
- Clicks "Export"
- FFmpeg concatenates clips
- Progress shows combined duration

## Tertiary User Flow: Platform-Specific Export

### Scenario: Sofia wants to repurpose for multiple platforms

**Step 1: Load Video**
- User imports horizontal video

**Step 2: Cut Segment**
- User marks In/Out points for main content

**Step 3: Export for YouTube**
- Selects "YouTube 1080p" preset
- Exports horizontal version

**Step 4: Export for TikTok**
- Applies crop filter to vertical format
- Selects "TikTok" preset
- Exports vertical version

**Step 5: Export for Instagram**
- Applies crop filter to square format
- Selects "Instagram" preset
- Exports square version

## Error Recovery Flows

### FFmpeg Not Found
- Application shows error dialog
- "FFmpeg not detected. Please install FFmpeg or specify path."
- User can:
  - Browse to FFmpeg executable
  - Download FFmpeg (link provided)
  - Cancel

### Export Failed
- Export job shows "Failed" status
- Error message displayed in queue
- User can:
  - Retry export
  - Check output path permissions
  - Try different codec settings

### File Import Error
- Dialog shows "Unsupported format or corrupted file"
- User can:
  - Try another file
  - Check file integrity
  - View FFprobe error details

## Keyboard Shortcuts Flow

**Navigation**
- Space: Play/Pause
- Home: Go to start
- End: Go to end
- Left/Right: Seek ±5 seconds
- Shift+Left/Right: Seek ±1 second
- Up/Down: Volume ±10%

**Editing**
- I: Set In point
- O: Set Out point
- Ctrl+Z: Undo
- Ctrl+Y: Redo
- Delete: Remove selected clip

**Export**
- Ctrl+E: Export
- Ctrl+Shift+E: Export with settings
- Ctrl+Q: Quit

## Onboarding Flow (First Launch)

1. Welcome screen appears
2. "Get Started" button
3. Quick tour overlay:
   - "Drag video here to import"
   - "Use I and O keys to mark segments"
   - "Select preset and click Export"
4. "Skip tour" option
5. Tour completes, user can start using app
