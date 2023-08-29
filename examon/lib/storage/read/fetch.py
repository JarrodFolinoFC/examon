class Fetch:
    def __init__(self, record_driver, blob_driver):
        self.record_driver = record_driver
        self.blob_driver = blob_driver

    def load(self, examon_filter=None):
        models = self.record_driver.load(examon_filter)
        self.blob_driver.load(models)
        return models
