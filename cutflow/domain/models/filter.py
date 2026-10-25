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
    CROP = "crop"
    RESIZE = "resize"
    ROTATE = "rotate"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    VOLUME = "volume"


@dataclass
class Filter:
    """Video filter with parameters"""
    type: FilterType
    value: float | str  # -100 to 100 for most filters, string for complex filters
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
                if isinstance(f.value, float):
                    filter_parts.append(f"eq=brightness={f.value / 100}")
            elif f.type == FilterType.CONTRAST:
                if isinstance(f.value, float):
                    filter_parts.append(f"eq=contrast={1 + f.value / 100}")
            elif f.type == FilterType.SATURATION:
                if isinstance(f.value, float):
                    filter_parts.append(f"eq=saturation={1 + f.value / 100}")
            elif f.type == FilterType.HUE:
                if isinstance(f.value, float):
                    filter_parts.append(f"eq=hue={f.value / 100}")
            elif f.type == FilterType.GAMMA:
                if isinstance(f.value, float):
                    filter_parts.append(f"eq=gamma={1 + f.value / 100}")
            elif f.type == FilterType.CROP:
                # value format: "iw:ih:0:0" (width:height:x:y)
                if isinstance(f.value, str):
                    filter_parts.append(f"crop={f.value}")
            elif f.type == FilterType.RESIZE:
                # value format: "1280:720" (width:height)
                if isinstance(f.value, str):
                    filter_parts.append(f"scale={f.value}")
            elif f.type == FilterType.ROTATE:
                # value in degrees: "90" or "-90"
                if isinstance(f.value, (float, str)):
                    filter_parts.append(f"rotate={f.value}*PI/180")
            elif f.type == FilterType.FADE_IN:
                # value format: "t=0:d=1" (start:duration in seconds)
                if isinstance(f.value, str):
                    filter_parts.append(f"fade=in:{f.value}")
            elif f.type == FilterType.FADE_OUT:
                # value format: "t=9:d=1" (start:duration in seconds)
                if isinstance(f.value, str):
                    filter_parts.append(f"fade=out:{f.value}")
            elif f.type == FilterType.VOLUME:
                # value in dB: "3dB" or "-3dB"
                if isinstance(f.value, str):
                    filter_parts.append(f"volume={f.value}")

        return ",".join(filter_parts)
