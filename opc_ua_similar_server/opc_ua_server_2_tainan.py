from opcua import Server
import random
import time

server = Server()
server.set_endpoint("opc.tcp://localhost:4841/freeopcua/server2/")
uri = "http://example.org/server2"
idx = server.register_namespace(uri)

# 添加一個物件樹
temp_object = server.nodes.objects.add_object(idx, "Temperature")
temp_variable = temp_object.add_variable(idx, "TemperatureValue", 0)

# 可複寫變數
temp_variable.set_writable()


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
initial_temp = 18.0  # 初始溫度
min_temp = 15.0  # 最小溫度
max_temp = 30.0  # 最大溫度
change_rate = 0.2  # 每次溫度變化的最大值

temperature_generator = generate_temperature(
    initial_temp, min_temp, max_temp, change_rate)


# 啟動 OPC UA 伺服器
server.start()

print("OPC UA Server 2 Tainan up and running at {}".format(server.endpoint))

try:
    while True:
        temperature = next(temperature_generator)
        print("Temperature is: {}".format(temperature))
        temp_variable.set_value(temperature)
        time.sleep(2)
except Exception as e:
    print(e)
finally:
    # 關閉連線
    server.stop()
