from examon_core.examon_item_registry import ItemRegistryFilter

from ...protocols import ContentReader


class InMemoryReader(ContentReader):
    def __init__(self, models):
        self.models = models

    def load(self, examon_filter: ItemRegistryFilter = None):
        return self.models
