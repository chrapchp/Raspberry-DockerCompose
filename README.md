##  Docker Compose 
#### Node-RED, MQTT, InfluxDB, Grafana, Telegraf

|File|Description|
-:|-
.env|could  be secrets or general config parameters for docker-compose.yml
.dev-influxdb.env | influxdb 2 config/secrets
docker-compose.yml -|docker compose file
/volume/mosquitto/config/mosqitto.conf  | generic configuration file
/volume/nodered/data/settings.js  | generic configuration file
/volume/nodered/data/key.pem | generate private key here
/volume/nodered/data/cert.pem | generate self-signed cert here
/volume/telegraf/telegraf.conf | generated by influxdb2 telegraf output configuration




