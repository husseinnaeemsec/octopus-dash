from django.core.exceptions import ImproperlyConfigured



class OctopusDashException(ImproperlyConfigured):
    """Base exception for all OctopusDash-related errors."""
    pass



class InvalidFieldException(OctopusDashException):
    """Raised when a specified field does not exist on the given model."""
    pass


class InvalidModelReference(OctopusDashException):
    """Raised when the `model` attribute is not a Django model class."""
    def __init__(self, model):
        msg = f"`model` must be a Django model class, not an instance: got {repr(model)}"
        super().__init__(msg)


class AbstractModelNotAllowed(OctopusDashException):
    """Raised when an abstract model is passed to ModelAdmin."""
    def __init__(self, model):
        super().__init__(f"Model '{model.__name__}' is abstract and cannot be used in ModelAdmin.")


class ModelRegistrationConflict(OctopusDashException):
    """Raised when both `model` and `model_admin` are provided simultaneously."""
    def __init__(self):
        super().__init__("Provide either `model` or `model_admin`, not both.")


# App-related exceptions
class AppNotFound(OctopusDashException):
    """Raised when a specified Django app is not found."""
    def __init__(self, app_label):
        super().__init__(f"App with the label '{app_label}' was not found.")

class DuplicateApp(OctopusDashException):
    """Raised when trying to register an app that is already registered."""
    def __init__(self, app_label):
        super().__init__(f"App '{app_label}' is already registered.")

# ModelAdmin-related exceptions
class ReadonlyFieldEditableException(OctopusDashException):
    """Raised when a readonly field is also listed in editable form fields."""
    def __init__(self, field):
        super().__init__(f"Readonly field '{field}' is also listed in 'form_fields'. This is not allowed.")

class HiddenFieldInFormException(OctopusDashException):
    """Raised when a hidden field is included in form_fields."""
    def __init__(self, field):
        super().__init__(f"Hidden field '{field}' cannot be included in 'form_fields'.")

class HiddenFieldInListDisplayException(OctopusDashException):
    """Raised when a hidden field is shown in list_display."""
    def __init__(self, field):
        super().__init__(f"Hidden field '{field}' cannot be included in 'list_display'.")

class InvalidActionException(OctopusDashException):
    """Raised when an action is not defined or not callable."""
    def __init__(self, action_name):
        
        super().__init__(f"Action '{action_name}' is missing. Define it or remove it from `actions`.")

class MissingModelException:
    """Raised when a ModelAdmin subclass doesn't define a model."""
    def __init__(self,name):
        raise OctopusDashException(f"You must define a `model` attribute in your {name} subclass.")

class InvalidModelReference(OctopusDashException):
    """Raised when the model provided is not a class."""
    def __init__(self, model):
        super().__init__(f"`model` must be a Django model class, not an instance: got {repr(model)}")

class AbstractModelNotAllowed(OctopusDashException):
    """Raised when an abstract model is passed to a ModelAdmin."""
    def __init__(self, model):
        super().__init__(f"Model '{model.__name__}' is abstract and cannot be used in ModelAdmin.")

class ModelRegistrationConflict(OctopusDashException):
    def __init__(self):
        super().__init__("Provide either `model` or `model_admin`, not both.")