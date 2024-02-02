# DEMO_OPC-UA_InfluxDB_Grafana_Simulation

模擬製作一個桌面Dashboard應用程式，能觀看工廠邊緣裝置定期回寫環境溫度資料，並可同時查看天氣影響資訊。採用 Electron 、grafana、 Vue.js、Flask、OPC UA Server(Python) 與 InfluxDB 整合。

## 使用方式

1. 至 `./docker-IoT/` 閱讀所提供的 `Docker.md` 建立docker
2. 至 `./opc_ua_similar_server` 閱讀所提供的 `Readme.md` 建立基礎程式，使用模擬程式讓服務啟動，自動寫入假資料
3. 按照`Docker.md` 操作，便能快速建立Dashboard

## 展示可用項目


### 模擬 Docker 使用

本專案會透過 docker-compose 模擬 Docker 建立 Grafana 與 InfluxDB 
![](.\docker-IoT\doc\1setup.png)


### 模擬 OPC UA Server 與 IoT Hub 通訊

本專案設置兩個 OPC UA Server ，並基於OPC UA統一與IoT Hub通訊
![](.\opc_ua_similar_server\Doc\0.png)

本專案會模擬寫入時序資料庫 InfluxDB
![](.\opc_ua_similar_server\Doc\1.png)


### 模擬 Grafana 應用

![](.\docker-IoT\doc\4-1.png)