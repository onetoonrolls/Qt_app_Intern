import paho.mqtt.client as mqtt #import the client1
import json
import time

#broker_address="192.168.1.184" 
# broker_name = "139.59.227.111"
# port = 1883
# username = "ndrs-sv"
# password = "mqtt@/2019"
info_topic = "info/#" #sub
update_topic = "update" #pub
noti_topic = "noti/#" #sub
msg = ""
info = [{},{},{}]
noti = ["","",""]
discon=0

def on_message(client, userdata, message):
    global msg,info,noti,discon
    msg = message.payload.decode()
    topic = message.topic
    #print(f"Received `{msg}` from `{topic}` topic")

    if msg == "discon":
        discon =1
        print("disconnect&terminate")

    topic_split = topic.split("/")
    if topic_split[0] == "info":
        msg_dic = json.loads(msg)
        if topic_split[1] == "device-1":
            info[0] = msg_dic
        elif topic_split[1] == "device-2":
            info[1] = msg_dic
        elif topic_split[1] == "device-3":
            info[2] = msg_dic
    elif topic_split[0] == "noti":
        if topic_split[1] == "device-1":
            noti[0] = msg
        elif topic_split[1] == "device-2":
            noti[1] = msg
        elif topic_split[1] == "device-3":
            noti[2] = msg
        

def on_log(client,userdata, level, buf): #edit methos in mqtt handler
    print("log : ",buf)

def on_connect(client, userdata, flags, rc):
    if rc ==0:
        print("connected ok")
        client.subscribe(info_topic)
        client.subscribe(noti_topic)
    else:
        print("bad connection code : ",rc)
    
def on_disconnect(client,userdata,flags,rc =0):
    print("Disconnect ",str(rc))

class MQTT_connect():
    def __init__(self):
        #broker_address="192.168.1.184" 
        self.broker_name = ""
        self.port = 1234
        self.username = ""
        self.password = ""
        self.id = "littlezoocafe"
        self.info_topic = "info/#" #sub
        self.update_topic = "update" #pub
        self.noti_topic = "noti/#" #sub
        # self.msg = ""
        # self.info = [{},{},{}]
        # self.noti = ["","",""]
        
        self.client = mqtt.Client(self.id)

    def setIDconnect(self,id):
        self.id = id

    def setConnect(self,broker,port,user,psw):
        self.broker_name = broker
        self.port = port
        self.username = user
        self.password = psw

    
    def connect_mqtt(self):
        #global on_connect,on_log,on_disconnect,on_message
        #set client ID
        #self.client = mqtt.Client("littleZoocafe") #create new instance
        #client = client = mqtt_client.Client(client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        #client.on_log =  self.on_log
        self.client.connect(self.broker_name, self.port) #connect to broker
        #client.connect(broker_name,1883,60) 

        print("connect to broker ",self.broker_name)
        #return client

    def shutdownDeviceAndDisconnect(self):
        self.client.publish("command","discon"+"@"+"") #test get info
#       print("send command disconnect")

    def disconnenct(self):
        self.client.disconnect()

    def convert_listTOJson(self,type,data):
        dic = {}
        count = 1
        if(type == "update_ip"):
            for d in data:
                dic["ip-"+str(count)] = d
                count +=1
        return json.dumps(dic)

    def get_info(self):
        global info
        self.client.publish("command","info"+"@"+"") #test get info
        print("send command get info")
        time.sleep(18)
        #print(noti)
        #print(info)
        return info
    
    def update_device(self,update_ip): #update_ip = list form
        self.client.publish("command","update"+"@"+self.convert_listTOJson("update_ip",update_ip))
        print("send command update device")
        time.sleep(10)
        print(noti)
     
if __name__ == '__main__':
    broker_name = "139.59.227.111"
    port = 1883
    username = "ndrs-sv"
    password = "mqtt@/2019"
    
    id = "littleZoocafe"
    test_update_ip = ["127.0.10.1","127.0.10.2","127.0.10.3"]
    mq = MQTT_connect()
    mq.setIDconnect(id)
    mq.setConnect(broker_name,port,username,password)
    mq.connect_mqtt()
    mq.client.loop_start()
    info = mq.get_info()
    print(info)
    mq.update_device(test_update_ip)
    mq.client.loop_stop()
    #mq.update_device(test_update_ip)