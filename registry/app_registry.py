


import logging 

logger = logging.getLogger(__name__)
from .admin import AppAdmin
from ._exceptions import DuplicateApp




# --------------------------
# Global Registry of AppAdmins
# --------------------------

class Registry:
    """
    Global singleton registry to manage registered AppAdmins by app label.
    """

    _registry = {}

    @classmethod
    def register_app(cls, app: AppAdmin) -> None:
        """
        Register an AppAdmin instance globally.

        Args:
            app (AppAdmin): The app to register.

        Raises:
            DuplicateApp: If the app label is already registered.
        """
        if not cls._registry.get(app.app_label):
            cls._registry[app.app_label] = app
            return
        raise DuplicateApp(f"App {app.app_label} is already registred.")

    @classmethod
    def get_app(cls, app_label: str) -> AppAdmin | None:
        """Get a registered AppAdmin by app label."""
        return cls._registry.get(app_label, None)

    @classmethod
    def get_apps(cls) -> dict:
        """Return all registered apps."""
        return cls._registry


registry = Registry()
