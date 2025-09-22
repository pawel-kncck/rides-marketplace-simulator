# simulator/utils/csv_logger.py
import csv

class CsvLogger:
    def __init__(self, filename="simulation_log.csv"):
        self.filename = filename
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["timestamp", "event_type", "rider_id", "driver_id", "details"])

    def log(self, timestamp, event_type, rider_id=None, driver_id=None, details=""):
        self.writer.writerow([timestamp, event_type, rider_id, driver_id, details])

    def close(self):
        self.file.close()
