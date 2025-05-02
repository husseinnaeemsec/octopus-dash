from django.conf import settings
from .admin import dashboard
from .conf import settings as octopusdash_settings

registry = dashboard.get_registry()



def get_model_admin(app_config,model):
    
    
    try:
        models = registry[app_config]['models']

        return models[model]['admin']

    
    except KeyError:
        return None

def get_app_models(app_config):
    
    try:
        return registry[app_config]['models']
    
    except KeyError:
        return None



def get_image_creation_model(field, path=None):
    from django.apps import apps

    """
    Retrieves the image creation model based on the configuration and model meta information.

    Args:
    - field: The field to retrieve the help text and other field properties.
    - path (optional): The dictionary that stores model paths (default: None, falls back to settings).

    Returns:
    - dict: A dictionary containing the image creation model details.
    
    Raises:
    - LookupError: If the image creation model is not found.
    """
    # Fallback to settings if path is not provided
    if path is None:
        config = octopusdash_settings.get("RICH_TEXT_EDITOR_IMAGE_CONFIG", {})
        path = config.get("IMAGE_MODEL_PATHS", {})

    # Get model information
    module, model_name = field.model.__module__, field.model._meta.object_name
    full_path = f"{module}.{model_name}"

    # Check if the full model path exists in the config and if ALLOW is set
    config = octopusdash_settings.get("RICH_TEXT_EDITOR_IMAGE_CONFIG", {})
    if full_path in path and config.get("ALLOW", False):
        image_creation_path = path.get(full_path)

        if image_creation_path:
            # Split path to get app_label and model name
            path_parts = image_creation_path.split(".")

            if len(path_parts) == 3:
                try:
                    # Get the model dynamically using app_label and model_name
                    app_label, model_name = path_parts[0], path_parts[2]
                    image_creation_model = apps.get_model(app_label, model_name)

                    # Return the details in a structured dictionary
                    return {
                        "model": {
                            "name": image_creation_model._meta.model_name,
                            "app_label": image_creation_model._meta.app_label,
                        }
                    }

                except LookupError:
                    raise LookupError(f"The image creation model '{image_creation_path}' is not found.")
    return None


