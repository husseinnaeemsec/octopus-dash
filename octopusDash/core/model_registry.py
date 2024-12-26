from django.apps import apps

class ModelRegistry:
    def __init__(self):
        # Initialize an empty dictionary to store models grouped by app name
        self.registry = {}

    def register_model(self, model,**kwargs):
        """
        Register a single model to the registry. 
        The model will be grouped by its app name.
        """
        app_name = model._meta.app_label 
        if app_name not in self.registry:
            self.registry[app_name] = []
        self.registry[app_name].append(model)

    def register_models(self, models):
        """
        Register multiple models at once. 
        This will group them by their app name.
        """
        for model in models:
            self.register_model(model)

    def get_models_by_app(self):
        """Return the registry of models grouped by app name."""
        return self.registry

    def get_models(self):
        """Return a flattened list of all registered models."""
        all_models = []
        for models in self.registry.values():
            all_models.extend(models)
        return all_models


octopus_registry = ModelRegistry()



