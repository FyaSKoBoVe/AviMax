"""Configuration manager"""

import shutil
from pathlib import Path
from typing import Optional

from cutflow.infrastructure.repositories.config_repository import ConfigRepository
from cutflow.domain.exceptions.file_error import FileError


class FFmpegDetector:
    """Detect FFmpeg installation"""

    @staticmethod
    def find_ffmpeg() -> Optional[str]:
        """Find FFmpeg executable in system

        Returns:
            Path to FFmpeg executable or None if not found
        """
        # Check common locations
        candidates = ["ffmpeg", "/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]
        for candidate in candidates:
            if shutil.which(candidate):
                return candidate
        return None

    @staticmethod
    def find_ffprobe() -> Optional[str]:
        """Find FFprobe executable in system

        Returns:
            Path to FFprobe executable or None if not found
        """
        # Check common locations
        candidates = ["ffprobe", "/usr/bin/ffprobe", "/usr/local/bin/ffprobe"]
        for candidate in candidates:
            if shutil.which(candidate):
                return candidate
        return None


class ConfigManager:
    """Application configuration manager"""

    def __init__(self, config_repository: ConfigRepository) -> None:
        """Initialize config manager

        Args:
            config_repository: Config repository instance
        """
        self._config_repository = config_repository
        self._ffmpeg_path: Optional[str] = None
        self._ffprobe_path: Optional[str] = None
        self._auto_detect = True

    def load(self) -> None:
        """Load configuration"""
        self._ffmpeg_path = self._config_repository.get("ffmpeg_path")
        self._ffprobe_path = self._config_repository.get("ffprobe_path")
        self._auto_detect = self._config_repository.get("auto_detect", True)

        if self._auto_detect:
            self.detect_ffmpeg()

    def save(self) -> None:
        """Save configuration"""
        if self._ffmpeg_path:
            self._config_repository.set("ffmpeg_path", self._ffmpeg_path)
        if self._ffprobe_path:
            self._config_repository.set("ffprobe_path", self._ffprobe_path)
        self._config_repository.set("auto_detect", self._auto_detect)

    def detect_ffmpeg(self) -> None:
        """Auto-detect FFmpeg installation"""
        if not self._ffmpeg_path:
            self._ffmpeg_path = FFmpegDetector.find_ffmpeg()
        if not self._ffprobe_path:
            self._ffprobe_path = FFmpegDetector.find_ffprobe()

    @property
    def ffmpeg_path(self) -> str:
        """Get FFmpeg path"""
        if not self._ffmpeg_path:
            self.detect_ffmpeg()
        return self._ffmpeg_path or "ffmpeg"

    @ffmpeg_path.setter
    def ffmpeg_path(self, path: str) -> None:
        """Set FFmpeg path"""
        self._ffmpeg_path = path
        self._auto_detect = False

    @property
    def ffprobe_path(self) -> str:
        """Get FFprobe path"""
        if not self._ffprobe_path:
            self.detect_ffmpeg()
        return self._ffprobe_path or "ffprobe"

    @ffprobe_path.setter
    def ffprobe_path(self, path: str) -> None:
        """Set FFprobe path"""
        self._ffprobe_path = path
        self._auto_detect = False

    @property
    def auto_detect(self) -> bool:
        """Get auto-detect setting"""
        return self._auto_detect

    @auto_detect.setter
    def auto_detect(self, value: bool) -> None:
        """Set auto-detect setting"""
        self._auto_detect = value
