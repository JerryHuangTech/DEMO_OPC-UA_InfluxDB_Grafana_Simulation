@echo off

cd "./dist"

start "" /wait "opc_ua_server_1_taipei.exe"
start "" /wait "opc_ua_server_2_tainan.exe"

start "" "iot_hub.exe"
