from ._exceptions import *
from django.db import models
from rest_framework.serializers import BaseSerializer

import logging 

logger = logging.getLogger(__name__)



# --------------------------
# Metaclass for ModelAdmin
# --------------------------

class ModelAdminMetaClass(type):
    """
    Metaclass for ModelAdmin that performs early validation of configuration at class creation.
    
    Validations include:
    - Presence and correctness of `model` attribute.
    - Correct data types for configuration lists.
    - Existence and callability of declared actions.
    - Fields' existence on the model for display, edit, readonly, hidden, filter fields.
    - Validation of serializer_class type.
    - Logging useful hints for better UX.
    """
    def __new__(cls, name, bases, namespace):
        model = namespace.get("model", None)

        # Validate model presence and validity if class is not base ModelAdmin
        if name != 'ModelAdmin':
            if model is None:
                raise MissingModelException(name)
            if not isinstance(model, type) or not issubclass(model, models.Model):
                raise InvalidModelReference(model)
            if getattr(model._meta, 'abstract', False):
                raise AbstractModelNotAllowed(model)

        # 1. Validate that specified attributes are lists or tuples
        list_attrs = [
            'list_display', 'list_editable', 'filter_fields',
            'readonly_fields', 'hidden_fields', 'actions'
        ]
        for attr in list_attrs:
            value = namespace.get(attr)
            if value is not None and not isinstance(value, (list, tuple)):
                raise TypeError(
                    f"`{attr}` in '{name}' must be a list or tuple, got {type(value).__name__}"
                )

        # 2. Validate actions: no duplicates, exist, callable, optionally decorated
        actions = namespace.get("actions", [])
        if len(actions) != len(set(actions)):
            raise InvalidActionException("Duplicate entries found in `actions` list.")
        
        for action in actions:
            func = namespace.get(action, None)
            # Check base classes as fallback (inherited actions)
            if func is None:
                for base in bases:
                    func = getattr(base, action, None)
                    if func:
                        break
            if not callable(func):
                raise InvalidActionException(action)

            if not hasattr(func, "_desc"):
                logger.warning(
                    f"Action method '{action}' is not decorated with @action in '{name}'. "
                    "Consider adding metadata with the @action decorator."
                )

        # 3. Validate fields against the declared model
        if model is not None and isinstance(model, type) and issubclass(model, models.Model) and name != 'ModelAdmin':
            model_fields = {f.name for f in model._meta.get_fields()}

            # Validate lookup_field existence
            lookup_field = namespace.get('lookup_field', 'id')
            if lookup_field not in model_fields:
                raise InvalidFieldException(f"lookup_field '{lookup_field}' not found on model '{model.__name__}'")
            
            # Validate each config attribute fields are present on the model
            for config_attr in ['list_display', 'list_editable', 'readonly_fields', 'hidden_fields', 'filter_fields']:
                for field in namespace.get(config_attr, []):
                    if field not in model_fields:
                        raise InvalidFieldException(f"Field '{field}' in '{config_attr}' is not defined on model '{model.__name__}'")

            # Validate form_fields if specified as list/tuple
            form_fields = namespace.get('form_fields', '__all__')
            if isinstance(form_fields, (list, tuple)):
                for field in form_fields:
                    if field not in model_fields:
                        raise InvalidFieldException(f"Field '{field}' in `form_fields` does not exist on model '{model.__name__}'")

            # Check for conflicts with specific exceptions for readonly, hidden, list_display fields
            def check_field_conflicts(field_list, target, exception_cls):
                for field in field_list:
                    if field not in model_fields:
                        raise exception_cls(f"Field '{field}' in '{target}' is not a field on model '{model.__name__}'")

            check_field_conflicts(namespace.get('readonly_fields', []), 'readonly_fields', ReadonlyFieldEditableException)
            check_field_conflicts(namespace.get('hidden_fields', []), 'hidden_fields', HiddenFieldInFormException)
            check_field_conflicts(namespace.get('list_display', []), 'list_display', HiddenFieldInListDisplayException)

        else:
            # Raise error if model is not set for subclasses of ModelAdmin
            if name != 'ModelAdmin':
                raise MissingModelException(name)

        # 4. Validate serializer_class type if set
        serializer_class = namespace.get("serializer_class", None)
        if serializer_class and not issubclass(serializer_class, BaseSerializer):
            raise TypeError(f"`serializer_class` must inherit from `rest_framework.serializers.BaseSerializer`")

        # 5. Log hint for better UI/UX if list_display is missing
        if not namespace.get('list_display') and name != 'ModelAdmin':
            logger.info(f"Consider defining 'list_display' in {name} for better model visualization.")

        return super().__new__(cls, name, bases, namespace)

