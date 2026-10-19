"""Main entry point for CutFlow application"""

import sys
from PySide6.QtWidgets import QApplication

from cutflow.app.dependencies import Dependencies
from cutflow.ui.views.main_window import MainWindow
from cutflow.ui.styles.theme_manager import ThemeManager
from cutflow.i18n.translator import Translator


def main() -> int:
    """Main entry point

    Returns:
        Exit code
    """
    app = QApplication(sys.argv)
    app.setApplicationName("CutFlow")
    app.setOrganizationName("CutFlow")

    # Setup translator
    translator = Translator()
    translator.load_translations(app)

    # Setup theme manager
    theme_manager = ThemeManager()
    stylesheet = theme_manager.load_theme("dark")
    app.setStyleSheet(stylesheet)

    # Setup dependencies
    deps = Dependencies()

    # Create main window
    main_window = MainWindow(
        project_vm=deps.project_viewmodel,
        player_vm=deps.player_viewmodel,
        export_vm=deps.export_viewmodel,
        theme_manager=theme_manager,
    )
    main_window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
