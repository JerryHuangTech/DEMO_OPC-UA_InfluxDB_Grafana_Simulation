from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime
from opcua import Client
import os
import random

# 設定參數
token = os.getenv('INFLUXDB_TOKEN',
                  "BLCddmNWRQqlNwuHDj2X4eEZQNWKoS3zqoKOkRGL3bqU_lMBZVUPAnw2L0VHziRm4Mvamvy76QeUev1jGOMwPg==")
org = os.getenv('INFLUXDB_ORG', "IoT")
bucket = os.getenv('INFLUXDB_BUCKET', "TemplateData")
db_url = os.getenv('INFLUXDB_URL', 'http://localhost:8086')

# 初始化 InfluxDB Client
client = InfluxDBClient(url=db_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


# 寫入資料庫
def write_data_to_influxdb(server_id, temperature):
    print(f"write temperature {temperature} to tag server_id {server_id}")
    try:
        point = Point("temperature") \
            .tag("server_id", server_id) \
            .field("value", temperature) \
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket=bucket, org=org, record=point)

        print("Data written to InfluxDB successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# 取得 OPC UA SERVER 的資料
def get_temperature_from_server(server_url):
    print(f"opcua url: {server_url}")
    opcua_client = Client(server_url)
    try:
        opcua_client.connect()
        temperature_node_id = "ns=2;i=2"
        temperature_node = opcua_client.get_node(temperature_node_id)
        temperature = temperature_node.get_value()
        print(f"get temperature: {temperature}")
        return temperature
    except Exception as e:
        print(f"Error connecting to {server_url}: {e}")
        return None
    finally:
        opcua_client.disconnect()


# 溫度動態
def generate_temperature(initial_temperature, min_temperature, max_temperature, rate_of_change):
    temperature = initial_temperature
    while True:
        temperature_change = random.uniform(-rate_of_change, rate_of_change)
        temperature += temperature_change
        if temperature < min_temperature:
            temperature = min_temperature
        elif temperature > max_temperature:
            temperature = max_temperature
        yield round(temperature, 3)


# 使用示例
initial_temp = 20.0  # 初始溫度（整數）
min_temp = 15.0  # 最小溫度（整數）
max_temp = 28.0  # 最大溫度（整數）
change_rate = 0.1  # 每次溫度變化的最大值（整數）

temperature_generator = generate_temperature(
    initial_temp, min_temp, max_temp, change_rate)


# 主程式持續執行
while True:
    try:
        print("執行 OPC UA ----------------")
        temperature_server0 = next(temperature_generator)
        print("loaclhost room temperature")
        print(f"get temperature: {temperature_server0}")
        temperature_server1 = get_temperature_from_server(
            "opc.tcp://localhost:4840/freeopcua/server1/")
        temperature_server2 = get_temperature_from_server(
            "opc.tcp://localhost:4841/freeopcua/server2/")

        if temperature_server0 is not None:
            write_data_to_influxdb("server_0_test", temperature_server0)
        if temperature_server1 is not None:
            write_data_to_influxdb("server_1_taipei", temperature_server1)
        if temperature_server2 is not None:
            write_data_to_influxdb("server_2_tainan", temperature_server2)
    except KeyboardInterrupt:
        print("程式手段中斷")
        client.close()
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(
                f"{datetime.now().isoformat()} - Error: {str(e)}\n")
    time.sleep(5)

client.close()
