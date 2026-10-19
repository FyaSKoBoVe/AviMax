"""Video filter model"""

from dataclasses import dataclass, field
from enum import Enum


class FilterType(Enum):
    """Filter type"""
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    SATURATION = "saturation"
    HUE = "hue"
    GAMMA = "gamma"


@dataclass
class Filter:
    """Video filter with parameters"""
    type: FilterType
    value: float  # -100 to 100 for most filters
    enabled: bool = True


@dataclass
class FilterChain:
    """Chain of video filters"""
    filters: list[Filter] = field(default_factory=list)

    def add_filter(self, filter: Filter) -> None:
        """Add filter to chain"""
        self.filters.append(filter)

    def remove_filter(self, filter_type: FilterType) -> None:
        """Remove filter from chain"""
        self.filters = [f for f in self.filters if f.type != filter_type]

    def get_filter(self, filter_type: FilterType) -> Filter | None:
        """Get filter by type"""
        for f in self.filters:
            if f.type == filter_type:
                return f
        return None

    def to_ffmpeg_filter(self) -> str:
        """Convert to FFmpeg filter string"""
        if not self.filters:
            return ""

        filter_parts = []
        for f in self.filters:
            if not f.enabled:
                continue

            if f.type == FilterType.BRIGHTNESS:
                # eq=brightness=<value>
                filter_parts.append(f"eq=brightness={f.value / 100}")
            elif f.type == FilterType.CONTRAST:
                # eq=contrast=<value>
                filter_parts.append(f"eq=contrast={1 + f.value / 100}")
            elif f.type == FilterType.SATURATION:
                # eq=saturation=<value>
                filter_parts.append(f"eq=saturation={1 + f.value / 100}")
            elif f.type == FilterType.HUE:
                # eq=hue=<value>
                filter_parts.append(f"eq=hue={f.value / 100}")
            elif f.type == FilterType.GAMMA:
                # eq=gamma=<value>
                filter_parts.append(f"eq=gamma={1 + f.value / 100}")

        return ",".join(filter_parts)
