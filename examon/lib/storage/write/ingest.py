class Ingest:
    def __init__(self, record_driver, blob_driver):
        self.record_driver = record_driver
        self.blob_driver = blob_driver

    def run(self):
        try:
            self.record_driver.create_all()
            self.blob_driver.create_files()
        except Exception:
            self.record_driver.delete_all()
            self.blob_driver.delete_files()
            raise
