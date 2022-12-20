# cpu_resource_monitor

### Overview

CPU resource monitor used system resource usage

### Installation
 
```
python3 -m venv env_resource
source env_resource/bin/activate
./install.sh
```

### Usage

Terminal session 1
```
./app.py
```

Terminal session 2
```
MQTT_HOST=localhost
MQTT_TOPIC=cpu_usage
SAMPLE_PERIOD=1
./monitor.py MQTT_HOST $MQTT_TOPIC $SAMPLE_PERIOD
```

Diagram (conceptual view): 

https://github.com/MyMelodyUwU/cpu_resource_monitor/blob/master/image.png
