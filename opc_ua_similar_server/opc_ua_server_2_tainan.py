from opcua import Server
from random import randint
import time

server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server2/")
uri = "http://example.org"
idx = server.register_namespace(uri)

# 添加一個物件樹
temp_object = server.nodes.objects.add_object(idx, "Temperature")
temp_variable = temp_object.add_variable(idx, "TemperatureValue", 0)

# 可複寫變數
temp_variable.set_writable()

# 啟動 OPC UA 伺服器
server.start()

print("OPC UA Server 2 Tainan up and running at {}".format(server.endpoint))

try:
    while True:
        temperature = randint(26, 32)
        print("Temperature is: {}".format(temperature))
        temp_variable.set_value(temperature)
        time.sleep(2)
except Exception as e:
    print(e)
finally:
    # 關閉連線
    server.stop()
