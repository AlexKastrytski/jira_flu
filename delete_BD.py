# #import influxdb_client, os, time # type: ignore
# from influxdb_client import InfluxDBClient, Point, WritePrecision # type: ignore
# from influxdb_client.client.write_api import SYNCHRONOUS # type: ignore
# token = 'FKNAyFerai9zrEuwq2VsOFxWSNfidmzJDWiEBTU-iy0Qsrh0fIaXLbJLRga53Whw-rU0n1io1Yk-h2biQPpwIw=='
# org = "A1_IKT"
# url = "http://192.168.16.15:8086"
# write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
# db_list = write_client.get_list_database()
# for db in db_list:
#     write_client.drop_database(db['name'])

from influxdb import InfluxDBClient
import os

influx_host = os.getenv('INFLUX_HOST', 'localhost')
db_client = InfluxDBClient(host=influx_host)

db_list = db_client.get_list_database()

for db in db_list:
    db_client.drop_database(db['name'])