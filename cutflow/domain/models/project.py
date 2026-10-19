"""Project model for CutFlow"""

from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import json

from cutflow.domain.models.clip import Clip
from cutflow.domain.models.filter import FilterChain


@dataclass
class Project:
    """CutFlow project"""

    name: str
    clips: list[Clip] = field(default_factory=list)
    filter_chain: FilterChain = field(default_factory=FilterChain)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    file_path: Path | None = None

    def add_clip(self, clip: Clip) -> None:
        """Add clip to project"""
        self.clips.append(clip)
        self.modified_at = datetime.now()

    def remove_clip(self, clip_id: str) -> None:
        """Remove clip from project"""
        self.clips = [c for c in self.clips if c.id != clip_id]
        self.modified_at = datetime.now()

    def save(self, path: Path) -> None:
        """Save project to file"""
        self.file_path = path
        self.modified_at = datetime.now()

        data = {
            "name": self.name,
            "clips": [
                {
                    "id": clip.id,
                    "file_path": str(clip.file_path) if clip.file_path else None,
                    "metadata": {
                        "video_codec": clip.metadata.video_codec if clip.metadata else "unknown",
                        "audio_codec": clip.metadata.audio_codec if clip.metadata else "unknown",
                        "resolution": clip.metadata.resolution if clip.metadata else "1920x1080",
                        "duration": clip.metadata.duration if clip.metadata else 0,
                        "fps": clip.metadata.video_fps if clip.metadata else 30,
                    },
                }
                for clip in self.clips
            ],
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "Project":
        """Load project from file"""
        with open(path) as f:
            data = json.load(f)

        from cutflow.domain.value_objects.video_metadata import VideoMetadata

        clips = []
        for clip_data in data.get("clips", []):
            metadata = VideoMetadata(
                format_name="unknown",
                duration=clip_data["metadata"]["duration"],
                size=0,
                video_codec=clip_data["metadata"]["video_codec"],
                video_width=1920,
                video_height=1080,
                video_fps=clip_data["metadata"]["fps"],
                audio_codec=clip_data["metadata"]["audio_codec"],
            )
            clip = Clip(
                id=clip_data["id"],
                file_path=Path(clip_data["file_path"]) if clip_data["file_path"] else None,
                metadata=metadata,
            )
            clips.append(clip)

        return cls(
            name=data["name"],
            clips=clips,
            created_at=datetime.fromisoformat(data["created_at"]),
            modified_at=datetime.fromisoformat(data["modified_at"]),
            file_path=path,
        )
