import configparser
import humanfriendly
from Utils import get_tracker
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
from datetime import timezone
from datetime import datetime
logging.basicConfig(format='%(asctime)s [%(levelname)8s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)

config = configparser.RawConfigParser()
config.read('config.ini')

influxdb_user = config['InfluxDB']['Username']
influxdb_pass = config['InfluxDB']['Password']

client = InfluxDBClient(url=config['InfluxDB']['URL'], token=f'{influxdb_user}:{influxdb_pass}', org='-')
write_api = client.write_api(write_options=SYNCHRONOUS)

time_now = datetime.now(tz=timezone.utc)
dt_string = time_now.strftime("%d/%m/%Y %H:%M:%S")
logging.info("The current date and time is " + dt_string)

for section in config.sections():
    if section.startswith('Tracker.'):
        if config[section].getboolean('Enabled'):
            trackerName = section.split('.')[1]
            tracker = get_tracker(trackerName, config[section])
            logging.info("Fetching stats for " + trackerName)
            try:
                stats = tracker.get_stats()
            except Exception as e:
                logging.error("An error occurred whilst retrieving stats for " + trackerName)
                logging.error(e)

            logging.info(f"({trackerName}) Ratio: {stats.ratio} Downloaded: {stats.download} ({humanfriendly.format_size(stats.download, binary=True)}) Uploaded: {stats.upload} ({humanfriendly.format_size(stats.upload, binary=True)})")

            p = Point("ratio").time(time_now).time(time_now).tag("tracker", trackerName).field("ratio", stats.ratio).field("download", stats.download).field("upload", stats.upload)

            try:
                write_api.write(bucket=config['InfluxDB']['Database'], org='-' ,record=p)
            except Exception as e:
                logging.error("An error occurred while writing to Influxdb.")
                logging.error(e)
            logging.info("Successfully written to InfluxDB")


