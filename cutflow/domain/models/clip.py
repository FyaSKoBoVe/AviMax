"""Clip model"""

from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from cutflow.domain.value_objects.video_metadata import VideoMetadata


@dataclass
class Clip:
    """Video clip in project"""

    id: str = field(default_factory=lambda: str(uuid4()))
    file_path: Path | None = None
    metadata: VideoMetadata | None = None
