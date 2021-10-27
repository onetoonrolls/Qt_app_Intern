import paho.mqtt.client as mqtt #import the client1
import json
import time
from datetime import datetime,timedelta

info_topic = "info/#" #sub
update_topic = "update" #pub
noti_topic = "noti/#" #sub
msg = ""
info = [{".."},{".."},{".."}]
noti = ["","","",""]
discon=0

def on_message(client, userdata, message): #get msg from devices, this method is work in interrupt
    global msg,info,noti,discon
    msg = message.payload.decode()
    topic = message.topic
    #print(f"Received `{msg}` from `{topic}` topic")
    #print(topic)
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
        # self.info_topic = "info/#" #sub
        # self.update_topic = "update" #pub
        # self.noti_topic = "noti/#" #sub
        self.client = mqtt.Client(self.id)

    def setIDconnect(self,id): #change cliend id to connect MQTT
        self.id = id

    def setConnect(self,broker,port,user,psw): #set basic connect MQTT
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

    def shutdownDeviceAndDisconnect(self): #send msg to shut down device & when get msg shut down myself 
        self.client.publish("command","discon"+"@"+"") #test get info
#       print("send command disconnect")

    def disconnenct(self):
        self.client.disconnect()

    def convert_listTOJson(self,type,data): #change string Json to dic form
        dic = {}
        count = 1
        if(type == "update_ip"):
            for d in data:
                dic["ip-"+str(count)] = d
                count +=1
        return json.dumps(dic)

    def checkALLinfo(self): #check change noti&info slot
        time.sleep(1)
        global noti
        # if(noti[0] != ""): #check send 1 device
        #     return True
        # return False
        for x in noti: #check all device send info
            if x == "":
                return False
        return True

    def get_noti(self): 
        global noti
        return noti
 
    def get_info(self): 
        global info,noti
        FMT = "%M.%S"
        tdelta = ""
        miss = []
        output = []
        self.client.publish("command","info"+"@"+"") #test get info
        print("send command get info")
        self.client.loop_start()
        
        later = datetime.now() + timedelta(minutes=0.167) #set timeout get info
        later = later.strftime(FMT)
        while(str(tdelta) != "0:00:00" and str(tdelta) != "-1 day, 23:59:59"):
            print("wait info")
            currentDateTime = datetime.now()
            now = currentDateTime.strftime(FMT)
            if(self.checkALLinfo()): #interrupt end receive info 
                break
            tdelta = datetime.strptime(later,FMT)-datetime.strptime(now,FMT)
            print(tdelta)
        for x in info:
            output.append(x)
        info = [{".."},{".."},{".."}] #reset info
        if str(tdelta) == "0:00:00" :
            noti[-1] = "get info time out, deivce "
            for x in range(len(noti)-1):
                if(noti[x] == ""):
                    noti[-1] = noti[-1] + str(x+1) + " "
            noti[-1] = noti[-1] + "didnt sent info"
        #print(noti[-1])
        self.client.loop_stop()
        return output
    
    def update_device(self,update_ip): #update_ip = list form
        self.client.publish("command","update"+"@"+self.convert_listTOJson("update_ip",update_ip))
        print("send command update device")
        self.client.loop_start()
        time.sleep(3)
        print(noti)
        self.client.loop_stop()
     
if __name__ == '__main__':
    broker_name = ""
    port = 1234
    username = ""
    password = ""
    
    id = "littleZoocafe"
    test_update_ip = ["127.0.10.1","127.0.10.2","127.0.10.3"]
    mq = MQTT_connect()
    mq.setIDconnect(id)
    mq.setConnect(broker_name,port,username,password)
    mq.connect_mqtt()
    #mq.client.loop_start()
    getValue = mq.get_info()
    print(getValue)
    #mq.update_device(test_update_ip)
    #mq.client.loop_stop()
    #mq.update_device(test_update_ip)