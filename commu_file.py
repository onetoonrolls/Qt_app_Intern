from os import stat
from FTP_client import connect_FTP as FTP
from Modbus_client import connect_Modbus as Mod
from INI_config import ini_config as ini
from MQTT_test import MQTT_config as MQTT
import logging

class commutnicate_app():
    def __init__(self):
        self.FTP_ip = "127.0.0.1"
        self.FTP_port = 21
        self.FTP_user = "****"
        self.FTP_psw = "****"
        self.MQTT_ip = "127.0.0.1"
        self.MQTT_port = 1883
        self.MQTT_user = "******"
        self.MQTT_psw = "*******"
        self.dataToINI = []
        self.device_name ="EMU-B20MC" #EMU-B20MC,EMU-B20SM
        self.MOd_ip =[] #get ip from read iniConfig & set ip update for Modbus
        self.MQ_MC = [] #check Match IP for MC device & device type to identify ip before collect from MQTT
        self.MQ_SM = [] #check Match IP for SM device & device type to identify ip before collect from MQTT
        self.MatchIPMAC = [] #check Match IP & MAC to identify ip before collect from MQTT
        self.type_connection = "Modbus"
        self.client_configParser = ini.ini_config()
        self.setFTP_connect()
        self.setMQTT_connect()
        #write info -> ini file when start class
        self.setDevice_name("EMU-B20MC")
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
        
    def setPrintData(self,data): #set data in list form to data
        self.dataToINI = data

    def setFTP_connect(self):
        Initread,key= self.getINI_file("INI_config/ini_storage/initConfig.ini")
        Initread = self.command_unpack_json(Initread)
        
        self.FTP_ip = Initread[0]["host_ip"]
        self.FTP_user = Initread[0]["username"]
        self.FTP_psw = Initread[0]["password"]
        self.FTP_port = Initread[0]["port"]

    def setDeviceIP_connect(self,ip): #set ip to connect modbus device from app
        
        if(ip == "MC"):
            Initread,key= self.getINI_file("INI_config/ini_storage/initConfig.ini")
            Initread = self.command_unpack_json(Initread)
            data = Initread[2]
            for key in data:
                #read ip EMUB20MC
                self.MOd_ip.append(data[key])
            self.setDevice_name("EMU-B20MC")
        elif(ip == "SM"):
            Initread,key= self.getINI_file("INI_config/ini_storage/initConfig.ini")
            Initread = self.command_unpack_json(Initread)
            data = Initread[3]
            for key in data:
                #read ip EMUB20SC
                self.MOd_ip.append(data[key])
            self.setDevice_name("EMU-B20SM")
        elif(type(ip)== int):
            logging.info("ip is int not string")
        else:
            self.MOd_ip.append(ip)
        
    def setMQTT_connect(self):
        Initread,key= self.getINI_file("INI_config/ini_storage/initConfig.ini")
        Initread = self.command_unpack_json(Initread)
        
        self.MQTT_ip = Initread[1]["server_ip"]
        self.MQTT_user = Initread[1]["username"]
        self.MQTT_psw = Initread[1]["password"]
        self.MQTT_port = int(Initread[1]["port"])

    def setDevice_name(self,device_name):
        self.device_name = device_name

    def setPath_ini(self,read,write):
        self.client_configParser.setPath(read,write)

    def setClearMod_ip(self):
        self.MOd_ip = []
        logging.info("clear Modbus ip done")

    def setMatchIP_MAC(self,IPMAC):
        self.MatchIPMAC = IPMAC
        print(IPMAC)
        
    def setTypeMatchIP(self,type):
        if(type == "MC"):
            self.MQ_MC = self.MOd_ip  
              
        elif(type == "SM"):
            self.MQ_SM = self.MOd_ip

    def connection_FTP(self):
        self.client_connectFTP = FTP.FTP_client()
        self.client_connectFTP.connect(self.FTP_ip,self.FTP_user,self.FTP_psw)

    def connnection_brige(self,con_type,ip): #connect client type connection
        #con_type = Modbus,MQTT
        self.type_connection = con_type
        if(self.type_connection == "Modbus"): 
            self.client_connect1 = Mod.Modbus_connect()
            return self.client_connect1.connect_client(ip)
        elif(self.type_connection =="MQTT"): #dev in pocessing MQTT
            self.client_connect2 = MQTT.MQTT_connect()
            self.client_connect2.setConnect(self.MQTT_ip,self.MQTT_port,self.MQTT_user,self.MQTT_psw)
            return self.client_connect2.connect_mqtt()
        else :
            logging.info("unknow type\n")
    
    def disconnect_FTP(self):
        self.client_connectFTP.disconnect()

    def disconnect_brige(self):
        if(self.type_connection == "Modbus"):
            self.client_connect1.disconect()
        elif(self.type_connection =="MQTT"):
            self.client_connect2.disconnenct()
        logging.info("disconnect done")

    def get_least_firmwareVer(self): #check FTP detail 
        version = self.client_connectFTP.check_firmware_ver_server()
        logging.info("avaliable firmware version: "+version)
        return version
    
    def get_allDevice_least_update(self): #check FTP log return dic form
        log_update,log_key = self.client_connectFTP.sort_detail(self.device_name)
        logging.info("rev. date log_update: "+log_update)
        return log_update,log_key
    
    def getInfo_device(self): #call info from another files
        if(self.type_connection) == "Modbus":
            return self.client_connect1.get_info_device()
        elif(self.type_connection == "MQTT"):
            return self.client_connect2.get_info()
        else:
            logging.info("type not map, try again!")
        
    def getINI_file(self,readPath): #get info from INI file
        self.client_configParser.setPath(readPath,"NULL")
        data,key =self.client_configParser.read_INI_to_Json()
        return data,key
    
    def getMQTTnoti(self):
        return self.client_connect2.get_noti()

    def getconnectIP(self): #check ip from main.py
        return self.MOd_ip

    def getlogFTP(self):
        return self.client_connectFTP.sort_detail(self.device_name)

    def conmmand_clearINI(self,type,readPath,writePath): #clear all data in one INI file
        if(type == "device"):
            self.client_configParser.setDevice_name(self.device_name)
            self.client_configParser.setPath(readPath,writePath)
            self.client_configParser.clearAllsection(type)
        else:
            self.client_configParser.setPath(readPath,writePath)
            self.client_configParser.clearAllsection(type)

    def command_unpack_json(self,data): #sort data from topic use in initConfig.ini to list form
            value =[]
            obj_pack_one = []
            for i in range(len(data)):
                
                if "EMU-B20MC-1" in data:
                    obj_pack_one = data[self.device_name+"-"+str(i+1)]
                elif "EMU-B20SM-1" in data:
                    obj_pack_one = data[self.device_name+"-"+str(i+1)]
                elif "log-1" in data:
                    obj_pack_one = data["log-"+str(i+1)]
                elif "logFTP-1" in data:
                    obj_pack_one = data["logFTP-"+str(i+1)]
                elif "FTP server" in data:
                    if(i == 0):
                        obj_pack_one = data["FTP server"]
                    elif(i == 1):
                        obj_pack_one = data["MQTT"]
                    elif(i == 2):
                        obj_pack_one = data["EMU-B20MC-init"]
                    elif(i == 3):
                        obj_pack_one = data["EMU-B20SM-init"]
                else:
                    logging.info("cant find topic in data")
                value.append(obj_pack_one)
            #print("return value: " ,value)
            return value
    
    def command_print_ini(self,typeSelect,writePath): #write data to INI file
        self.client_configParser.setPath("NULL",writePath)
        #print(self.dataToINI)
        if(typeSelect == "device"):
            self.client_configParser.setDevice_name(self.device_name)
            self.client_configParser.setDevice_info(self.dataToINI[0],self.dataToINI[1],self.dataToINI[2],[self.dataToINI[3],self.dataToINI[4],self.dataToINI[5],self.dataToINI[6]],self.dataToINI[7])
        elif(typeSelect == "log"):
            self.client_configParser.setLog(self.dataToINI[0],self.dataToINI[1],self.dataToINI[2],self.dataToINI[3])
        elif(typeSelect == "initConfig"):
            self.client_configParser.setInitconfig(self.dataToINI[0])
            self.client_configParser.setDevice_name(self.dataToINI[1])
            pass
        elif(typeSelect == "logFTP"):
            self.client_configParser.setLogFTP(self.dataToINI[0],self.dataToINI[1],self.dataToINI[2],self.dataToINI[3])
        self.client_configParser.ini_print(typeSelect)
    
    def command_update_firmware(self): 
        if(self.type_connection == "Modbus"):
            self.client_connect1.update_firmware()
            logging.info("current updating ....")
        elif (self.type_connection == "MQTT"):
            self.client_connect2.update_device(self.MOd_ip)
        else:
            logging.info("type not map, try again!")

    def command_complexUpdate(self,type,allIP): #pack of update command use in Modbus 
        statuscontext = []
        for ip in allIP:
            statusconnect = self.connnection_brige(type,ip)
            #print(statusconnect)
            if(statusconnect == "connect"):
                self.command_update_firmware()
                self.disconnect_brige()
                statuscontext.append("update "+ip+" done") 
            else:
                statuscontext.append("unable connect ip "+ip)
        return statuscontext

    def commamd_complexDeviceINFO(self,type,allIP): #pack of info command from type
        if type == "Modbus":
            for ip in allIP:
                statusconnect = self.connnection_brige(type,ip) #connect device
                #print(statusconnect)
                if(statusconnect == "connect"):
                    mac,id,st,ver= self.getInfo_device() #get info
                
                    self.setPrintData([ip,mac,id,st[0],st[1],st[2],st[3],ver]) #compack info
                    self.command_print_ini("device","INI_config/ini_storage/") #write ini
                    self.disconnect_brige()
                else:
                    print(statusconnect)
        elif type == "MQTT":
            statusconnect = self.connnection_brige(type,"")
            
            info = commu.getInfo_device()
            
            print(info)
            for x in info:
                ip = ""
                for y in self.MatchIPMAC:
                    if x["mac"] == y[1]:
                        print(x["ip"])
                        ip = y[0]
                        print(ip)
                        break
                # self.setPrintData([ip,mac,id,st["mes"],st["sdc"],st["ntp"],st["tcp"],ver])#compack info
                # self.command_print_ini("device","INI_config/ini_storage/") #write ini
            # self.disconnect_brige()

        self.setClearMod_ip()
        
            
if __name__ == "__main__":
    ip = '*****'
    user = '*****'
    pws = '*****'
    device_name = "EMU-B20MC"
    Path_Download = "../transfer_file_log/"
    Path_server = "/"+device_name+"/fw/log"
    filename = "detail.txt" #test search
    data = ["127.0.11.0","11/11/2077","0x0000"]
    update = ["172.16.5.148","172.16.5.65"]
    c = commutnicate_app()
    #c.setDevice_name("EMU-B20MC")
    
    commu = commutnicate_app()
    #commu.setDevice_name("EMU-B20MC")
    #commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
    #commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20SM.ini","INI_config/ini_storage/")
    #commu.setDeviceIP_connect("MC")
    #print(commu.MOd_ip)
    # commu.commamd_complexDeviceINFO("Modbus",commu.getconnectIP())
    # commu.setDeviceIP_connect("SM")
    # print(commu.MOd_ip)
    # commu.commamd_complexDeviceINFO("Modbus",commu.getconnectIP())
    #connect = commu.command_complexUpdate("Modbus",update)
    #print(connect)
    
    # Initread,key= commu.getINI_file("INI_config/ini_storage/initConfig.ini")
    # Initread = commu.command_unpack_json(Initread)
    # print("v output : ",Initread)

    # commu.setMQTT_connect()
    # print(commu.MQTT_ip)
    # print(commu.MQTT_user)
    # print(commu.MQTT_psw)
    # print(commu.MQTT_port)

    #readINI,keyReadINI = c.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
    #print("\nkey INI file : ",keyReadINI)
    #print("\nobj INI file : ",readINI)
    #
    #print(V)
    # c.command_print_ini("log","INI_config/ini_storage/")
    
    # c.setDevice_name("EMU-B20MC")
    # readINI,keyReadINI = c.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
    # V = c.command_unpack_json(readINI)
    # print("v output : ",V)

    # readINI,keyReadINI = c.getINI_file("INI_config/ini_storage/log.ini")
    # V = c.command_unpack_json(readINI)
    # print("v output : ",V)

    # c.setFTP_connect()
    # print(c.FTP_ip,c.FTP_user,c.FTP_psw,c.FTP_port)

    # c.setDeviceIP_connect()
    # print(c.MOd_ip)

    # t = [
    #     ['001122334477', '6/8/2021', '17:01:08', 'v0124'],
    #     ['4E445211103E', '6/8/2021', '16:45:05', 'v0124'],
    #     ['4E445211103E', '6/8/2021', '16:50:14', 'v0124']
    #]
    #for i in t:
    #     # print(i[0])
    #     # print(i[1])
    #     # print(i[2])
    #     # print(i[3])
        # c.setPrintData(i)
        # c.command_print_ini("logFTP","INI_config/ini_storage/")
    
    # Table_data,Table_head = c.getINI_file("INI_config/ini_storage/logFTP.ini")
    # list_obj= c.command_unpack_json(Table_data)
    # print(list_obj)
    print(commu.MQTT_ip)
    print(commu.MQTT_user)
    print(commu.MQTT_psw)
    print(commu.MQTT_port)
    commu.commamd_complexDeviceINFO("MQTT","")
    noti = commu.getMQTTnoti()
    print(noti)
    # commu.connnection_brige("MQTT","")
    # commu.setDeviceIP_connect("127.0.10.1")
    # commu.command_update_firmware()
    # commu.disconnect_brige()
