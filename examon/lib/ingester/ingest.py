class Ingest:
    def __init__(self, records, driver):
        self.driver = driver
        self.records = records

    def run(self):
        self.driver.run()
