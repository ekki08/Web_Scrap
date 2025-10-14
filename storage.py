import csv
import json
import os
from datetime import datetime

class Storage:
    def __init__(self, base_dir="wb_storage"):
        """
        :param output_dir: Folder to save scraped data
        """
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
    
    def _timestamp_path(self, filename):
        data = datetime.now().strftime("%Y-%m-%d")
        folder = os.path.join(self.base_dir, data)
        os.makedirs(folder, exist_ok = True)
        return os.path.join(folder, filename)

    def save_to_json(self, filename, data):
        filepath = self._timestamped_path(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved JSON → {filepath}")

    def save_to_csv(self, filename, data):
        filepath = self._timestamped_path(filename)
        if not data: return
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ Saved CSV → {filepath}")
