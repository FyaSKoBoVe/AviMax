"""Translator for internationalization"""

import locale
from pathlib import Path
from PySide6.QtCore import QTranslator, QLocale


class Translator:
    """Translator for application strings"""

    def __init__(self) -> None:
        """Initialize translator"""
        self._translator = QTranslator()
        self._current_locale = self._detect_locale()

    def _detect_locale(self) -> str:
        """Detect system locale

        Returns:
            Locale string (e.g., "en", "it")
        """
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                return system_locale[:2]  # Get language code only
        except Exception:
            pass
        return "en"  # Default to English

    def load_translations(self, app) -> None:
        """Load translations for application

        Args:
            app: QApplication instance
        """
        translations_dir = Path(__file__).parent
        translation_file = translations_dir / f"cutflow_{self._current_locale}.qm"

        if translation_file.exists():
            self._translator.load(str(translation_file))
            app.installTranslator(self._translator)

    def tr(self, text: str) -> str:
        """Translate text

        Args:
            text: Text to translate

        Returns:
            Translated text
        """
        # In a real implementation, this would use QCoreApplication.translate
        # For now, return the text as-is
        return text

    @property
    def current_locale(self) -> str:
        """Get current locale"""
        return self._current_locale

    def set_locale(self, locale_code: str) -> None:
        """Set locale

        Args:
            locale_code: Locale code (e.g., "en", "it")
        """
        self._current_locale = locale_code
