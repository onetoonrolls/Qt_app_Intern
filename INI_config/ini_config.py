import configparser
import os
import logging

class ini_config():
   
    def __init__(self):
        
        self.device_name = ""
        self.value1 = [] #ip,houst_ip,ip(log)
        self.value2 =[] #mac,username
        self.value3 = [] #id,password,date
        self.value4 =[] #mes,port,error
        self.value5= [] #sdc,ip(init)
        self.value6 = [] #ntp
        self.value7 = [] #tcp
        self.value8 = [] #c_version
        self.FTP_data ={} #unuse
        self.device_info = {}
        self.path_write = "INI_config/ini_storage/"
        self.path_read = "INI_config/ini_storage/example.ini"
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    def setDevice_name(self,device): #set deivce type
        self.device_name = device

    def setStatus(self,status_rev): #set status info device
        self.value4.append(status_rev[0])
        self.value5.append(status_rev[1])
        self.value6.append(status_rev[2])
        self.value7.append(status_rev[3])

    def setFTP_data(self,FTP): #set initConfig port
        self.FTP_data["port"]= FTP

    def setVersion(self,ver): #set device version
        self.value8.append(ver)

    def setDate(self,date): #set log date
        self.value3.append(date)

    def setError(self,error): #set log error
        self.value4.append(error)

    def setIP(self,ip): #set device ip
        self.value1.append(ip)

    def setMac(self,mac): #set deivce mac
        self.value2.append(mac)

    def setID(self,id): #set device id
        self.value3.append(id)

    def setTime(self,time): #set log time
        self.value4.append(time)

    def setLog(self,ip,mac,date,error): #pack of log command for update log 
        self.setIP(ip)
        self.setMac(mac)
        self.setDate(date)
        self.setError(error)

    def setInitconfig(self,ip):
        self.setIP(ip)

    def setLogFTP(self,mac,date,time,ver): #pack of log command for FTP
        #self.setIP(ip)
        self.setMac(mac)
        self.setDate(date)
        self.setTime(time)
        self.setVersion(ver)

    def setDevice_basicDetail(self,id,ip,mac): 
        self.setIP(ip)
        self.setMac(mac)
        self.setID(id)
    
    def setDevice_info(self,ip,mac,id,sta,C_ver): #pack of device info command 
        self.setDevice_basicDetail(id,ip,mac)
        self.setStatus(sta)
        self.setVersion(C_ver)

    def setClear(self): #clear value in ini_config
        self.value1 = [] 
        self.value2 =[] 
        self.value3 = [] 
        self.value4 =[] 
        self.value5= [] 
        self.value6 = [] 
        self.value7 = [] 
        self.value8 = []
        
    def clearAllsection(self,type): #clear all section in ini.file
        data =  configparser.ConfigParser()
        logging.info("current read file: "+self.path_read)
        data.read(os.path.abspath(self.path_read))
        for section in data.sections():
            logging.info("section :"+section)
            data.remove_section(section)
        
        logging.info("write path :"+self.path_write)
        if(type == "device"):
            file_name = self.path_write+'config_'+self.device_name+'.ini'
            logging.info("file name : "+file_name)
        elif(type == "log"):
            file_name = self.path_write+'log.ini'
            logging.info("file name : "+file_name)
        elif(type == "initConfig"):
            file_name = self.path_write+'initConfig.ini'
            logging.info("file name : "+file_name)
        elif(type == "logFTP"):
            file_name = self.path_write+'logFTP.ini'
        else:
            logging.info("type NULL ")
        with open(os.path.abspath(file_name), 'w') as configfile: #write file
            data.write(configfile)
            logging.info("clear complete")

    def setPath(self,read,write): #if string same = same path,if string NULL = no change path

        if(read =="same"):
            read = write
        elif(read =="NULL"):
            read = self.path_read
        elif(write =="same"):
            write = read
        elif(write =="NULL"):
            write = self.path_write
        self.path_read = read
        self.path_write = write

    def ini_print(self,type): #write INI file classify from type
        data =  configparser.ConfigParser() #inherit parser object
        logging.info("write path :"+self.path_write)
        if(type == "device"):
            file_name = self.path_write+'config_'+self.device_name+'.ini'
            logging.info("file name : "+file_name)
        elif(type == "log"):
            file_name = self.path_write+'log.ini'
            logging.info("file name : "+file_name)
        elif(type == "initConfig"):
            file_name = self.path_write+'initConfig.ini'
            logging.info("file name : "+file_name)
        elif(type == "logFTP"):
            file_name = self.path_write+'logFTP.ini'
        else:
            logging.info("type NULL ")
        self.setPath("same",file_name)
        data.read(os.path.abspath(self.path_read))
        if(type != "initConfig"):
            if(data.sections() !=[]): #check data not overwrite
                for section in data.sections(): #get old data
                    for key,value in data.items(section):
                        #self.key_obj.append(key)
                        if(key =="ip"or key =="houst_ip"): 
                            self.value1.append(value) #ip,houst_ip,ip(log)
                        elif(key =="mac" or key =="username" ):
                            self.value2.append(value) #mac,username
                        elif(key =="id" or key =="password" or key =="date"):
                            self.value3.append(value) #id,password,error,date
                        elif(key =="mes"or key =="port" or key =="error" or key == "time"):
                            self.value4.append(value) #mes,port,timeFTP
                        elif(key =="sdc"or key =="initip"):
                            self.value5.append(value) #sdc,ip(init)
                        elif(key =="ntp"):
                            self.value6.append(value) #ntp
                        elif(key =="tcp"):
                            self.value7.append(value) #tcp
                        elif(key =="c_version" or key == "version"):
                            self.value8.append(value) #c_version,verFTP
                            #print("value ver: ",value)
                        else:    
                            print("key not macth; key: ",key,value)

            for i in range(len(data.sections())+1): #create section topic in new file
                if(type == "device"):
                    data[self.device_name+"-"+str(i+1)]={
                        "ip" : self.value1[i],
                        "mac" : self.value2[i],
                        "id" : self.value3[i],
                        "MES" : self.value4[i],
                        "SDC" : self.value5[i],
                        "NTP" : self.value6[i],
                        "TCP" : self.value7[i],
                        "c_version" : self.value8[i]
                    }
                elif(type == "log"):
                    data["log-"+str(i+1)]={
                            "ip" : self.value1[i],
                            "mac": self.value2[i],
                            "date" : self.value3[i],
                            "error" : self.value4[i]
                        }
                elif(type == "logFTP"):
                    data["logFTP-"+str(i+1)]={
                            #"ip" : self.value1[i],
                            "mac": self.value2[i],
                            "date" : self.value3[i],
                            "time" : self.value4[i],
                            "version" : self.value8[i]
                        }
        elif(type == "initConfig"):
            sec_item = data.items(self.device_name+'-init')
            L_init = len(sec_item)
            data.set(self.device_name+'-init',"initip-"+str(L_init+1),self.value1[0])
        else:
            logging.info("worng type")
        with open(os.path.abspath(file_name), 'w') as configfile: #write file
            data.write(configfile)
            logging.info("ini file printed")
        self.setClear()
        logging.info("clear done")

    def read_INI_to_Json(self): #convert .ini file to dic form
        data =  configparser.ConfigParser() #inherit parser object
        key_obj = []
        logging.info("current read file: "+self.path_read)
        dic_con = {} #original convert data form
        
        data.read(os.path.abspath(self.path_read))
        
        #return all section in .ini file
        for section in data.sections():
            logging.info("section"+section)
            
            if(section.find("EMU") !=-1):
                key_obj = ["ip","mac","id","mes","sdc","ntp","TCP","c_ver"]
            elif(section.find("log-1") !=-1):
                key_obj = ["ip","mac","date","error"]
            elif(section.find("logFTP") !=-1):
                key_obj = ["ip","mac","date","time","ver"]
            else:
                logging.info("section invaild")
            dic_con[section] ={}
            for key,value in data.items(section):
                dic_con[section][key]=value
        return dic_con,key_obj

if __name__ == "__main__":
    #status = ["nor","nor","nor","nor"]
    #FTP = {"port":21,"server":"ndrs"}
    #a = ini_config()
    # d = "EMU-B20MC"
    # a = ["124.21.2.312"]
    # config = configparser.ConfigParser()
    # config.read('INI_config/ini_storage/initConfig.ini')
    # b = config.items(d+'-init')
    # l = len(b)
    # print(l)
    # config.set(d+'-init',"initip-"+str(l+1),a[0])
    # with open('INI_config/ini_storage/initConfig.ini', 'w') as configfile: #write file
    #         config.write(configfile)
    #config[d+'-init']["initip-"+str(l)]=a[0]
    # a.setPath("NULL","INI_config/ini_storage/")
    # a.setDevice_name("EMU-B20MC")
    # a.setDevice_info("127.0.0.1","0x14E52E02A","0x0008",status,"0x0123")
    # a.ini_print("device")

    # a.setPath("NULL","INI_config/ini_storage/")
    # a.setLog("127.0.10.1","03/25/2077","0x0000")
    # a.ini_print("log")
    
    # a.setPath("INI_config/ini_storage/config_EMU-B20MC.ini","NULL")
    # readINI,keyReadINI = a.read_INI_to_Json()
    # print("\nkey INI file : ",keyReadINI)
    # print("\nobj INI file : ",readINI)
    
    # a.setPath("INI_config/ini_storage/log.ini","NULL")
    # readINI,keyReadINI = a.read_INI_to_Json()
    # print("\nkey INI file : ",keyReadINI)
    # print("\nobj INI file : ",readINI)

    # a.setPath("INI_config/ini_storage/config_EMU-B20SM.ini","INI_config/ini_storage/")
    # a.setDevice_name("EMU-B20SM")
    # a.clearAllsection("device")
    pass

