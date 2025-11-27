# utils.py
import os
import csv
from datetime import datetime


def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_timestamp():
    return datetime.now().isoformat()


def append_to_csv(csv_path, row, header=None):
    # Ensure its directory exists
    ensure_directory(os.path.dirname(csv_path))

    file_exists = os.path.isfile(csv_path)

    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)

        # Add header if file didn't exist or is empty
        if header and (not file_exists or os.path.getsize(csv_path) == 0):
            writer.writerow(header)

        writer.writerow(row)


def format_number(num, precision=3):
    try:
        return f"{float(num):.{precision}f}"
    except:
        return "0.0"