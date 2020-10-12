import configparser
from Utils import get_tracker
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

config = configparser.RawConfigParser()
config.read('config.ini')

influxdb_user = config['InfluxDB']['Username']
influxdb_pass = config['InfluxDB']['Password']

client = InfluxDBClient(url=config['InfluxDB']['URL'], token=f'{influxdb_user}:{influxdb_pass}', org='-')
write_api = client.write_api(write_options=SYNCHRONOUS)

for section in config.sections():
    if section.startswith('Tracker.'):
        if config[section].getboolean('Enabled'):
            trackerName = section.split('.')[1]
            tracker = get_tracker(trackerName, config[section])
            print(f"[{trackerName}] Fetching stats.")
            try:
                stats = tracker.get_stats()
            except Exception as e:
                print(f"[{trackerName}] An error occurred while retrieving stats for this tracker.")
                print(f"[{trackerName}] {str(e)}")

            print(f"[{trackerName}] Ratio: {stats.ratio} Downloaded: {stats.download} Uploaded: {stats.upload}")

            p = Point("ratio").tag("tracker", trackerName).field("ratio", stats.ratio).field("download", stats.download).field("upload", stats.upload)

            try:
                write_api.write(bucket=config['InfluxDB']['Database'], org='-' ,record=p)
            except Exception as e:
                print("[InfluxDB] An error occurred while writing to Influxdb.")
                print(f"[InfluxDB] {str(e)}")
            print("[InfluxDB] Successfully written to InfluxDB")


