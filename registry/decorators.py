# --------------------------
# Decorator for Admin Actions
# --------------------------

from functools import wraps

def action(desc, permissions=[]):
    """
    Decorator to attach metadata (description and permissions) to admin action methods.
    
    Args:
        desc (str): Short description used for labeling and UI display.
        permissions (list): Optional list of permission codenames required to run the action.
    
    Returns:
        function: The wrapped function with metadata attached.
    """
    def decorator(func):
        setattr(func, "_desc", desc)
        setattr(func, "_permissions", permissions)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrapper
    return decorator
