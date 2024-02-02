python -m venv venv || exit /b
venv\Scripts\activate || exit /b
pip install opcua influxdb_client pyinstaller || exit /b
