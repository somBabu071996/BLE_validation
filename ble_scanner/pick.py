import asyncio
from bleak import BleakScanner
from datetime import datetime
import csv
import os

# Track startup time once
start_time = datetime.now()
timestamp_str = start_time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"ble_log_{timestamp_str}.csv"

# MACs to track
TARGET_MACS = {"E6:95:56:F7:A1:62", "E6:95:56:F7:A1:61", "CB:B6:B5:81:23:47", "CB:B6:B5:81:23:48","F6:A4:0F:01:83:90"}


# Write CSV headers
with open(LOG_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "MAC", "RSSI", "Name"])

def detection_callback(device, advertisement_data):
    mac = device.address.upper()
    if mac in TARGET_MACS:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rssi = advertisement_data.rssi
        name = device.name or "Unknown"

        # Print to console
        print(f"[{timestamp}] Device: {mac}, RSSI: {rssi}, Name: {name}")

        # Append to CSV
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, mac, rssi, name])
            f.flush()

async def main():
    scanner = BleakScanner(detection_callback)
    print(f"🔍 Live BLE scan (saving to {LOG_FILE})... Press Ctrl+C to stop.")
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\n⛔ Scan stopped by user.")
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(main())
