from influxdb import InfluxDBClient
import datetime
import time
from opcua import Client

# 初始化 InfluxDB Client
client = InfluxDBClient('influxdb', 8086, 'admin',
                        'supersecret', 'IoT-edge-template')
client.create_database('IoT-edge-template')
client.switch_database('IoT-edge-template')


def write_data_to_influxdb(server_id, temperature):
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "server_id": server_id
            },
            "time": datetime.utcnow().isoformat(),
            "fields": {
                "value": temperature
            }
        }
    ]
    client.write_points(json_body)


def get_temperature_from_server(server_url):
    client = Client(server_url)
    try:
        # OPC UA Server 模擬連線
        client.connect()

        # 連上server
        temperature_node_id = "ns=2;i=2"
        temperature_node = client.get_node(temperature_node_id)

        # 讀取測量資料
        temperature = temperature_node.get_value()
        return temperature
    finally:
        # 中斷連線
        client.disconnect()


# 模擬接收 OPC UA server 資料
while True:
    # 這裡假設直接調用
    temperature_server1 = get_temperature_from_server(
        "opc.tcp://localhost:4840/freeopcua/server1/")
    temperature_server2 = get_temperature_from_server(
        "opc.tcp://localhost:4840/freeopcua/server2/")

    # 寫入 InfluxDB
    write_data_to_influxdb("server1_taipei", temperature_server1)
    write_data_to_influxdb("server2_tainan", temperature_server2)

    time.sleep(2)  # 每隔 2 秒模拟接收一次数据
