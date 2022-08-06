#!/usr/bin/python

# Is necessary to install python-lxml and curl packages

from lxml import etree
from influxdb import InfluxDBClient
import time

# InfluxDB server
influxdb_server = 'MyInfluxDB.com'

# InfluxDB port
influxdb_port = '8086'

# InfluxDB Database name
database = 'testdb'

# InfluxDB Auth
username = 'influx-user'
password = 'AtB73HeTqp'

client = InfluxDBClient(host = influxdb_server, port = influxdb_port, username = username, password = password, database = database)

# Tracker running information
opentracker_link_url = 'http://127.0.0.1:6969/stats?mode=everything'

# Tracker's torrent information
opentracker_torrent_info_url = 'http://127.0.0.1:6969/stats?mode=tpbs&format=txt'

# Data query interval in seconds:
wait = 30

while True:
    status = etree.parse(opentracker_url)
    stats = status.getroot()

    # Uptime
    uptime = stats[2].text

    # Torrents
    torrents = stats[3][0].text

    # Peers
    peers = stats[4][0].text

    # Seeds
    seeds = stats[5][0].text

    # Completed downloads
    completed = stats[6][0].text

    # leechers
    leechers = int(peers) - int(seeds)

    # Uncomment to debug
    #print("Uptime: " + uptime)
    #print("Torrents: " + torrents)
    #print("Peers: " + peers)
    #print("Seeds: " + seeds)
    #print("Leechers: " + str(leechers))
    #print("Completed: " + completed)

    # Write to InfluxDB
    link_data = [
        {
            "measurement": "link_data",
            "tags": {
                "tracker_id":tracker_id
            },
            "fields": {
                "uptime":uptime,
                "torrents":torrents,
                "peers":peers,
                "seeds":seeds,
                "completed":completed,
                "leechers":leechers
            }
        }
    ]

    client.write_points(link_data)

    # wait for 15 seconds
    time.sleep(wait)
