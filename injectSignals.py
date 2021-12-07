from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plot

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "makeMeComplicated"
org = "theOrg"
bucket = "theBucket"
serverIP = "localhost"
#serverIP = "192.168.2.86"


def generateSine( amplitude, freq, samplingRate):
    deltaT = 1./samplingRate
    t = np.arange(0, 1, deltaT)
    sinusoid =  amplitude * np.sin(2*np.pi*freq*t)
    return (t, sinusoid)

# generate AM modulated wave
sampingRate=400 

ac = 1   # carrier amplitude
fc = 10  # carrier frequence 

(t,carrier) = generateSine( ac, fc, sampingRate)
plot.plot(t, carrier)


am = 10
fm = 1
(t,message) = generateSine( am, fm, sampingRate)
plot.plot(t, message)

mi =am/ac
modulatedAM = ((ac + mi*message) * carrier) 

plot.plot(t, modulatedAM)



# go back samplingRate seconds as we are going to push samples at 1 samples per s
timestamp = int(datetime.now().timestamp()) - sampingRate 
points = []
with InfluxDBClient(url="http://" + serverIP + ":8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)

    #for sample in len(modulatedAM):
    for sample in range(len(modulatedAM)):

        point = Point("sampleSignals") 
        point.tag("tag", "carrier") 
        point.field("value", carrier[sample]) 
        point.time(timestamp,WritePrecision.S )
        points.append( point)
        
        point = Point("sampleSignals") 
        point.tag("tag", "message") 
        point.field("value", message[sample]) 
        point.time(timestamp,WritePrecision.S )
        points.append( point)
        
        point = Point("sampleSignals") 
        point.tag("tag", "modulatedAM") 
        point.field("value", modulatedAM[sample]) 
        point.time(timestamp,WritePrecision.S )
        points.append( point)
        


        write_api.write(bucket, org, points,time_precision="s")
        #write_api.write(bucket, org, point2,time_precision="s")

        timestamp = timestamp + 1
#         write_api.write(bucket, org, data,time_precision="ns")
client.close()


plot.show()