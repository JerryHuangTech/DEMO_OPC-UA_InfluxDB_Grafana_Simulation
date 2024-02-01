# DEMO_Room_Temperature_Dashboard
模擬製作一個桌面Dashboard應用程式，能觀看工廠邊緣裝置定期回寫環境溫度資料，並可同時查看天氣影響資訊。採用 Electron 、grafana、 Vue.js、Flask、OPC UA Server(Python) 與 InfluxDB 整合。

## 使用方式

1. 先使用 `Install.bat` 自動完成 `venv` 建置，並完成 `pip` 安裝 
2. 至 `./docker-IoT/` 閱讀所提供的 `Readme.md` 建立docker
3. 至 `./opc_ua_similar_server` 使用模擬程式讓服務啟動，自動寫入假資料
4. 至 `./main_console` 執行 `npm i` 完成安裝，接著執行 `npm run dev` ，就能啟動監控的應用程式