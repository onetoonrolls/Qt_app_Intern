import sys,os
import paho.mqtt.client as mqtt #import the client1
sys.path.append(os.path.dirname(os.path.abspath("INI_config")))
from INI_config import ini_config as ini

import time
import json

client_configParser = ini.ini_config()
#broker_address="192.168.1.184" 
broker_name = "****"
port = 1883
username = "***"
password = "*****"
command_topic = "command" #sub
info_topic = "info/device-1" #pub
noti_topic = "noti/device-1" #pub
device_ip = "127.0.10.3"
msg = ""
msg_split = ["",""]
info = {"mac":"0x123AF2C001",
        "status":{
                "mes":" normal",
                "sdc":"normal",
                "ntp":"normal",
                "tcp ":"normal"        
        },
        "id":"0x201",
        "c_version":"0x9"
}
discon=0

def on_message(client, userdata, message):
    global msg,msg_split
    msg = message.payload.decode()
    #print(type(msg))
    print(f"Received `{msg}` from `{message.topic}` topic")
    msg_split = msg.split("@")
    if(msg_split[1] != ""):
        msg_split[1] = json.loads(msg_split[1])
    #print(msg_split)

def on_log(client,userdata, level, buf): #edit methos in mqtt handler
    print("log : ",buf)

def on_connect(client, userdata, flags, rc):
    if rc ==0:
        print("connected ok")
        client.subscribe(command_topic)
    else:
        print("bad connection code : ",rc)
    
def on_disconnect(client,userdata,flags,rc =0):
    print("Disconnect ",str(rc))

def getINI_file(readPath):
        client_configParser.setPath(readPath,"NULL")
        data,key =client_configParser.read_INI_to_Json()
        return data,key

def command_unpack_json(data): #in case send json not work 
            value =[]
            obj_pack_one = []
            for i in range(len(data)):
                if "FTP server" in data:
                    if(i == 0):
                        obj_pack_one = data["FTP server"]
                    elif(i == 1):
                        obj_pack_one = data["MQTT"]
                    elif(i == 2):
                        obj_pack_one = data["EMU-B20MC-init"]
                    elif(i == 3):
                        obj_pack_one = data["EMU-B20SM-init"]
                else:
                    pass
                    #logging.info("cant find topic in data")
                value.append(obj_pack_one)
            #print("return value: " ,value)
            return value

def setMQTT_connect():
    global broker_name,username,password,port
    Initread,key= getINI_file("INI_config/ini_storage/initConfig.ini")
    Initread = command_unpack_json(Initread)
    #print(Initread)
    broker_name = Initread[1]["server_ip"]
    username = Initread[1]["username"]
    password = Initread[1]["password"]
    port = Initread[1]["port"]

def connect_mqtt():
    #set client ID
    client = mqtt.Client("littleZoocafe1") #create new instance
    #client = client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    #client.on_log =  on_log
    client.connect(broker_name, port) #connect to broker
    #client.connect(broker_name,1883,60) 

    print("connect to broker ",broker_name)
    return client
    
def checkUpdate(ip):
    
    if(ip != ""):
        for key in ip:
            #print(ip[key])
            if ip[key] == device_ip:
                return True
        return False
    else:
        print("data is null")
        
def run():
    global msg,msg_split,discon
    setMQTT_connect()
    mq = connect_mqtt()
   
    mq.loop_start()
    while(True):
        time.sleep(5)
        if(discon == 1):
            time.sleep(15)
            mq.disconnect()
            break
        else:
            print(msg_split)
            if(msg_split[0] == "update"):
                if(checkUpdate(msg_split[1])):
                    mq.publish(noti_topic,"update "+device_ip)
                    print("send update")
                msg_split[0] = ''
                msg_split[1] = ''
            elif(msg_split[0] == "info"):
                mq.publish(info_topic,json.dumps(info))
                mq.publish(noti_topic,"info send")
                print("send info")
                msg_split[0] = ''
            elif(msg_split[0] == "discon"):
                mq.publish(noti_topic,"discon")
                discon = 1
                print("disconnect..")
            elif(msg_split[0] == ""):
                print("wait..")
                msg_split[0] = ''
                msg_split[1] = ''
            else:
                print("msg_split isnt not match")
            #print("running")

            # i=+1
    mq.loop_stop()

if __name__ == '__main__':
    run()