"""Dependency injection container"""

from pathlib import Path

from cutflow.infrastructure.ffmpeg.ffmpeg_service import FFmpegService
from cutflow.infrastructure.ffmpeg.probe_service import ProbeService
from cutflow.infrastructure.repositories.config_repository import ConfigRepository
from cutflow.infrastructure.repositories.project_repository import ProjectRepository
from cutflow.app.config import ConfigManager, FFmpegDetector
from cutflow.viewmodels.project_viewmodel import ProjectViewModel
from cutflow.viewmodels.player_viewmodel import PlayerViewModel
from cutflow.viewmodels.export_viewmodel import ExportViewModel


class Dependencies:
    """Dependency injection container"""

    def __init__(self) -> None:
        """Initialize dependencies"""
        self._config_repository: ConfigRepository | None = None
        self._config_manager: ConfigManager | None = None
        self._ffmpeg_service: FFmpegService | None = None
        self._probe_service: ProbeService | None = None
        self._project_repository: ProjectRepository | None = None
        self._project_viewmodel: ProjectViewModel | None = None
        self._player_viewmodel: PlayerViewModel | None = None
        self._export_viewmodel: ExportViewModel | None = None

    @property
    def config_repository(self) -> ConfigRepository:
        """Get config repository"""
        if self._config_repository is None:
            self._config_repository = ConfigRepository()
        return self._config_repository

    @property
    def config_manager(self) -> ConfigManager:
        """Get config manager"""
        if self._config_manager is None:
            self._config_manager = ConfigManager(self.config_repository)
            self._config_manager.load()
        return self._config_manager

    @property
    def ffmpeg_service(self) -> FFmpegService:
        """Get FFmpeg service"""
        if self._ffmpeg_service is None:
            self._ffmpeg_service = FFmpegService(self.config_manager.ffmpeg_path)
        return self._ffmpeg_service

    @property
    def probe_service(self) -> ProbeService:
        """Get probe service"""
        if self._probe_service is None:
            self._probe_service = ProbeService(self.config_manager.ffprobe_path)
        return self._probe_service

    @property
    def project_repository(self) -> ProjectRepository:
        """Get project repository"""
        if self._project_repository is None:
            self._project_repository = ProjectRepository(Path.home() / "CutFlow" / "Projects")
            self._project_repository.base_dir.mkdir(parents=True, exist_ok=True)
        return self._project_repository

    @property
    def project_viewmodel(self) -> ProjectViewModel:
        """Get project viewmodel"""
        if self._project_viewmodel is None:
            self._project_viewmodel = ProjectViewModel(self.probe_service)
        return self._project_viewmodel

    @property
    def player_viewmodel(self) -> PlayerViewModel:
        """Get player viewmodel"""
        if self._player_viewmodel is None:
            self._player_viewmodel = PlayerViewModel()
        return self._player_viewmodel

    @property
    def export_viewmodel(self) -> ExportViewModel:
        """Get export viewmodel"""
        if self._export_viewmodel is None:
            self._export_viewmodel = ExportViewModel()
        return self._export_viewmodel
