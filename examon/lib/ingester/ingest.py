class Ingest:
    def __init__(self, records, driver):
        self.driver = driver
        self.records = records

    def run(self):
        for record in self.records:
            self.driver.insert(record)
            # unique id
            # internal id
            # language
            # repo
            # filename
            # ->1 src        (Mandatory)
            # ->1 metrics    (Optional)
            # ->M choices    (Optional)
            # ->M print logs (Mandatory)
            #

            pass
