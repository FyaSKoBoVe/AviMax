"""Export presets for common platforms and formats"""

from dataclasses import dataclass
from enum import Enum


class PresetCategory(Enum):
    """Preset category"""
    PLATFORM = "platform"
    FORMAT = "format"
    CUSTOM = "custom"


@dataclass
class ExportPreset:
    """Export preset with predefined settings"""

    name: str
    category: PresetCategory
    video_codec: str
    audio_codec: str
    crf: int
    preset: str
    video_bitrate: str | None = None
    audio_bitrate: str | None = None
    resolution: str | None = None
    description: str = ""


# Common export presets
EXPORT_PRESETS: dict[str, ExportPreset] = {
    # Platform presets
    "youtube_1080p": ExportPreset(
        name="YouTube 1080p",
        category=PresetCategory.PLATFORM,
        video_codec="libx264",
        audio_codec="aac",
        crf=23,
        preset="medium",
        video_bitrate="8M",
        audio_bitrate="192k",
        resolution="1920x1080",
        description="YouTube recommended settings for 1080p",
    ),
    "youtube_720p": ExportPreset(
        name="YouTube 720p",
        category=PresetCategory.PLATFORM,
        video_codec="libx264",
        audio_codec="aac",
        crf=23,
        preset="medium",
        video_bitrate="5M",
        audio_bitrate="128k",
        resolution="1280x720",
        description="YouTube recommended settings for 720p",
    ),
    "whatsapp": ExportPreset(
        name="WhatsApp",
        category=PresetCategory.PLATFORM,
        video_codec="libx264",
        audio_codec="aac",
        crf=28,
        preset="medium",
        video_bitrate="2M",
        audio_bitrate="128k",
        resolution="720x1280",
        description="WhatsApp optimized for mobile sharing",
    ),
    "instagram": ExportPreset(
        name="Instagram",
        category=PresetCategory.PLATFORM,
        video_codec="libx264",
        audio_codec="aac",
        crf=23,
        preset="medium",
        video_bitrate="3.5M",
        audio_bitrate="128k",
        resolution="1080x1080",
        description="Instagram square format",
    ),
    "tiktok": ExportPreset(
        name="TikTok",
        category=PresetCategory.PLATFORM,
        video_codec="libx264",
        audio_codec="aac",
        crf=23,
        preset="medium",
        video_bitrate="4M",
        audio_bitrate="128k",
        resolution="1080x1920",
        description="TikTok vertical format",
    ),
    # Format presets
    "mp4_h264": ExportPreset(
        name="MP4 H.264",
        category=PresetCategory.FORMAT,
        video_codec="libx264",
        audio_codec="aac",
        crf=23,
        preset="medium",
        description="Standard MP4 with H.264 codec",
    ),
    "mp4_h265": ExportPreset(
        name="MP4 H.265",
        category=PresetCategory.FORMAT,
        video_codec="libx265",
        audio_codec="aac",
        crf=28,
        preset="medium",
        description="MP4 with H.265 (HEVC) for better compression",
    ),
    "webm": ExportPreset(
        name="WebM VP9",
        category=PresetCategory.FORMAT,
        video_codec="libvpx-vp9",
        audio_codec="libopus",
        crf=30,
        preset="medium",
        description="WebM with VP9 codec for web",
    ),
    "mp3_audio": ExportPreset(
        name="MP3 Audio",
        category=PresetCategory.FORMAT,
        video_codec="none",
        audio_codec="libmp3lame",
        crf=0,
        preset="medium",
        audio_bitrate="192k",
        description="Extract audio as MP3",
    ),
    "aac_audio": ExportPreset(
        name="AAC Audio",
        category=PresetCategory.FORMAT,
        video_codec="none",
        audio_codec="aac",
        crf=0,
        preset="medium",
        audio_bitrate="192k",
        description="Extract audio as AAC",
    ),
}


def get_preset(preset_id: str) -> ExportPreset | None:
    """Get preset by ID

    Args:
        preset_id: Preset identifier

    Returns:
        ExportPreset or None if not found
    """
    return EXPORT_PRESETS.get(preset_id)


def get_all_presets() -> list[ExportPreset]:
    """Get all presets

    Returns:
        List of all presets
    """
    return list(EXPORT_PRESETS.values())


def get_presets_by_category(category: PresetCategory) -> list[ExportPreset]:
    """Get presets by category

    Args:
        category: Preset category

    Returns:
        List of presets in the category
    """
    return [p for p in EXPORT_PRESETS.values() if p.category == category]
