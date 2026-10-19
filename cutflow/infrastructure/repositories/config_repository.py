"""Config repository implementation"""

import json
from pathlib import Path
from platformdirs import user_config_dir
from typing import Any, Optional


class ConfigRepository:
    """Repository for application configuration"""

    def __init__(self, app_name: str = "CutFlow") -> None:
        """Initialize config repository

        Args:
            app_name: Application name
        """
        self.config_dir = Path(user_config_dir(app_name))
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        """Load configuration from file

        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            return {}

        with open(self.config_file) as f:
            return json.load(f)

    def save(self, config: dict[str, Any]) -> None:
        """Save configuration to file

        Args:
            config: Configuration dictionary
        """
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        config = self.load()
        return config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value

        Args:
            key: Configuration key
            value: Value to set
        """
        config = self.load()
        config[key] = value
        self.save(config)
