# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import commu_file as commu
import logging
import pandas as pd
import time 
from datetime import datetime,timedelta
from threading import Thread as th

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import *

class countTime(th): #count down timer

    def __init__(self):
        th.__init__(self)

        self.stoptime = False
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.bufferTimer = []
        self.status = "end"
        self.timer = ""
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    def setupdatefunction(self,update,listIP,type): #get init function & value
        self.conType = type  #connect type
        self.listIP = listIP #get all update ip
        #pass function
        self.updateDevice = update #update

    def settime(self): #set time form main class
        if(self.bufferTimer == []):
            self.hour =0
            self.min =0
            self.sec =0
            self.status = "not set"
        else:
            delta = self.bufferTimer.pop(0)
            #print("pop : ",delta)
            delta = str(delta).split(":")
            #print("split :",delta)
            self.hour = int(delta[0])
            self.min = int(delta[1])
            self.sec = int(delta[2])
            self.status = "alraedy set"

    def setbufferTimer(self,tdelta): # buffering click button more than 1 times
        self.bufferTimer.append(str(tdelta))
        self.status = "wait"
        #print("list timer : ",self.bufferTimer)
        
    def countdown(self): #main function timer
        
        self.status = "clock running"
        t = self.hour*60*60+self.min*60+self.sec
        while t:
        # Divmod takes only two arguments so
        # you'll need to do this for each time
        # unit you need to add
            if(self.stoptime == True):
                break
            mins, secs = divmod(t, 60)  #convert time unit
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)
            self.timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs) #set form
            print(self.timer, end="\r") 
            time.sleep(1) 
            t -= 1
        if(self.stoptime == True): #instant stop timer
            self.status = "cancle"
            logging.info("cancle")
        else:
            self.status = "done"
        self.stoptime = False

    def getTimer(self):
        return self.timer

    def getstatusTimer(self):
        return self.status

    def run(self): #runing in thread
        print("thread run")
        self.settime()
        print("settime")
        self.countdown()
        print("countdown")
        self.updateDevice(self.listIP,self.conType)    #updatedevice(self,updateip,type)
        print("update")
        self.bufferTimer =[]
        logging.info("timer done")

class TableModel(QAbstractTableModel): #model view prototype, this basic set Model for displaying data in QT form
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                #print("value ",str(value))
                return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

class Connect_page(QObject):
    
    #create signal
    setContextListcheck = Signal(str)
    setClearListcheck = Signal(bool)
    setContexNoti = Signal(str)
    
    def __init__(self):
        QObject.__init__(self)

        self.errorCode = "0x0000"
        self.date ="07/555/2077"
        self.updateIP = []
        self.hour = []
        self.min = []
        self.listSetData("hour") #reset tumbler timer
        self.listSetData("min")  #reset tumbler timer
        self.dataHour = pd.DataFrame(self.hour,columns=["hour"]) #set data for tumbler
        self.dataMin = pd.DataFrame(self.min,columns=["min"]) #set data for tumbler
        self.timer = countTime() #inherite countdown class 
        #self.timer = countTime(self.testfunc)
          
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
        self.commu = commu.commutnicate_app()
        self.commu.setDevice_name("EMU-B20MC") 
        
        #create TabelModel section
        self.devicetopic =['ip','mac','id','mes','sdc','ntp','tcp','c_version'] #init table columns
        self.devicecData = pd.DataFrame(columns=self.devicetopic) #create table with columns
        self.statustopic=['ip','mac','date','error'] 
        self.statusData = pd.DataFrame(columns=self.statustopic)
        self.logtopic=['mac','date','version'] 
        self.logData = pd.DataFrame(columns=self.logtopic)
        #read old log from inifile
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini") #read INI file 
        self.list_obj = self.commu.command_unpack_json(self.Table_data) #convert data form
        self.tableSetData("status",self.list_obj) #push data in table

        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/logFTP.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("logFTP",self.list_obj)

        self.commu.setDevice_name("EMU-B20MC")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)
        self.commu.setDevice_name("EMU-B20SM")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20SM.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)

        self.deviceTable = TableModel(self.devicecData) #convert table to model form
        self.statusTable = TableModel(self.statusData)
        self.logTable = TableModel(self.logData)
    
    def checkFTPlog(self):
        #connectFTP
        self.commu.setFTP_connect()
        self.commu.connection_FTP()
        
    def listSetData(self,type): #set hour&min for tumbler timer
        num = ""
        if(type == "hour"):
            for i in range(12):
                self.hour.append(i+1)
        elif(type == "min"):
            for i in range(60):
                self.min.append(i)

    def settimer(self,h,m): #set basic timer info
        self.timer = countTime()
        #self.timer = countTime(self.testfunc)
        
        FMT = "%d-%m %H:%M" #date form 
        currentDateTime = datetime.now() #get current date
        #print(currentDateTime.strftime("%D:%H:%M"))
        now = currentDateTime.strftime(FMT) #init date form to current date
        #print(now)
        nowHour = currentDateTime.hour #get current hour
        if(h == "-1"): #in case none set timer
            tdelta = datetime.strptime(now,FMT)-datetime.strptime(now,FMT)
            print(tdelta)
        else:
            hour = int(h) 
            if(hour<nowHour):
                tomorrow = datetime.now() + timedelta(days=1)
                #print(tomorrow)
                nextDay =tomorrow.day
                Month =tomorrow.month
                date2 = str(nextDay)+"-"+str(Month)+" "+h+":"+m
            else:
                nowDay = currentDateTime.day
                nowMonth = currentDateTime.month
                date2 = str(nowDay)+"-"+str(nowMonth)+" "+h+":"+m
            tdelta = datetime.strptime(date2,FMT)-datetime.strptime(now,FMT) #find period
        self.timer.setbufferTimer(tdelta)

    @Slot(int,int,int)
    def setTimeupdate(self,hour,min,posfix): #init basic timer from UI 
        if(hour == -1):
            self.settimer(str(-1),str(-1))
        else:
            hour = self.dataHour.at[hour,"hour"]
            min = self.dataMin.at[min,"min"]
            if(hour <10):
                hour_str = "0"+str(hour)
            else:
                hour_str = str(hour)
            if(min <10):
                min_str = "0"+str(min)
            else:
                min_str = str(min)
            if(posfix == 0):
                #self.setTimeSignal.emit(hour_str+" : "+min_str+" AM")
                self.settimer(hour_str,min_str)
            elif(posfix == 1):
                #self.setTimeSignal.emit(hour_str+" : "+min_str+" PM")
                self.settimer(str(hour+12),min_str)
        
    @Slot(bool)
    def cancleTimer(self,stop): #clear timer setting
        self.timer.stoptime = stop
        self.timer.bufferTimer = []
        self.timer.hour = 0
        self.timer.min = 0
        self.timer.sec = 0

    def starCount(self): #start timer thread
        self.timer.start()

    def tableSetData(self,table,data): #insert data to table
        for i in data:
            if(table == "device"):
                self.devicecData = self.devicecData.append(i,ignore_index=True)
            elif(table == "status"):
                self.statusData = self.statusData.append(i,ignore_index=True)
            elif(table == "logFTP"):
                self.logData = self.logData.append(i,ignore_index=True)
            else:
                logging.info("unmatch table")

    def findIP(self,mac): #find ip form mac in table
        index = self.devicecData[self.devicecData['mac']== mac].index.values.astype(int)[0]
        ip = self.devicecData.iat[index,1]
        return ip

    def findMacUpdate(self,updateIP): #find mac from ip use in update device
        index = self.devicecData[self.devicecData['ip']== updateIP].index.values.astype(int)[0] #find index
        updateMac = self.devicecData.iat[index,1] #get device mac
        return updateMac
    
    def getALLdeviceIP(self): #get ip from table
        listIP = self.devicecData['ip'].tolist()
        return listIP
    
    def getALLLdeviceMAC(self): #get mac from table
        listMAC = self.devicecData['mac'].tolist()
        return listMAC
    
    def getALLDIP_MAC(self): # use for match ip&mac when fetch 
        listDevice = []
        listIP = self.getALLdeviceIP()
        listMac = self.getALLLdeviceMAC()
        for index in range(len(listIP)):
            listDevice.append(listIP[index],listMac[index])
        return listDevice 
    
    @Slot(bool)
    def appendToListCheck(self, isState): #get ip from table & push to select IP section
        self.setClearListcheck.emit(True)
        listIP = self.getALLdeviceIP()
        for ip in listIP:
            self.setContextListcheck.emit(ip)
        
    @Slot(bool)
    def refreshmentStatus(self, isState): #update status info
        self.statusData = self.statusData.iloc[0:0] #clear old data
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini")
        list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("status",list_obj)
        self.statusTable._data = self.statusData
        self.statusTable.layoutChanged.emit()
        logging.info("status table changed")
        self.setContexNoti.emit("refresh status done")
        
    def updatedevice(self,updateip,type):
        print("update device function")
        updatecontext = self.commu.command_complexUpdate(type,updateip)
        print(updatecontext)

    @Slot(str)
    def updateFirmware(self, type): #update device for Modbus
        if(type == ""):
            logging.info("type connection from QML is NULL")
            self.setContexNoti.emit("type connection from QML is NULL")
        else:
            
            self.timer.setupdatefunction(self.updatedevice,self.updateIP,type)
            for ip in self.updateIP:  #add print to log.ini 
                updateMac = self.findMacUpdate(ip)
                FMT = "%d-%m %H:%M"
                currentDateTime = datetime.now()
                now = currentDateTime.strftime(FMT)
                data = [ip,updateMac,now,"no avalible"]      
                self.commu.setPrintData(data)
                self.commu.command_print_ini("log","INI_config/ini_storage/") 
            self.starCount()
            self.setContexNoti.emit("update commit done")

    @Slot(str)        
    def getUpdateIP(self, ip): #check receive ip from update section
        if(ip == ""):
            logging.info("ip is NULL")
        else:
            self.updateIP.append(ip)
            logging.info("IP rev.")
    
    @Slot(bool)
    def refreshmentLog(self, isState): #update log table
        #fetch newdata from device section
        self.commu.conmmand_clearINI("logFTP","INI_config/ini_storage/logFTP.ini","INI_config/ini_storage/")
        self.commu.connection_FTP()
        self.commu.setDevice_name("EMU-B20MC")
        MC,topicMC =self.commu.getlogFTP() 
        self.commu.setDevice_name("EMU-B20SM")
        SM,topicSM =self.commu.getlogFTP()
        self.commu.disconnect_FTP()
        #write section
        if(topicMC =="not found" or topicSM =="not found"):
            self.setContexNoti.emit("not found log")
        if(topicMC !="not found"):
            for i in MC:
                self.commu.setPrintData(i)
                self.commu.command_print_ini("logFTP","INI_config/ini_storage/")
        elif(topicSM !="not found"):
            for i in SM:
                self.commu.setPrintData(i)
                self.commu.command_print_ini("logFTP","INI_config/ini_storage/")
            #read section
        if(topicMC !="not found" or topicSM !="not found"):
            self.logData = self.logData.iloc[0:0]
            self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/logFTP.ini")
            self.list_obj = self.commu.command_unpack_json(self.Table_data)
            self.tableSetData("logFTP",self.list_obj)
            self.logTable._data = self.logData
            self.logTable.layoutChanged.emit()
            self.setContexNoti.emit("update log FTP table")

    @Slot(bool)
    def refreshmentTable(self, isState): #update device info table for Modbus
        #fetch newdata from device section
        self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20SM.ini","INI_config/ini_storage/")
        self.commu.setDeviceIP_connect("MC")
        self.commu.commamd_complexDeviceINFO("Modbus",self.commu.getconnectIP())
        self.commu.setDeviceIP_connect("SM")
        self.commu.commamd_complexDeviceINFO("Modbus",self.commu.getconnectIP())

        #read data from ini file section
        self.devicecData = self.devicecData.iloc[0:0] #clear old data
        self.commu.setDevice_name("EMU-B20MC")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)
        self.commu.setDevice_name("EMU-B20SM")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20SM.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)

        self.deviceTable._data = self.devicecData
        self.deviceTable.layoutChanged.emit()
        #change ip in List checkbox
        self.appendToListCheck(True)
        self.setContexNoti.emit("refresh device table done")
    
    @Slot(bool)
    def refreshmentTableMQTT(self, isState): #update device table for MQTT
        #fetch newdata from device section
        self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20SM.ini","INI_config/ini_storage/")
        self.commu.setMatchIP_MAC(self.getALLDIP_MAC())
        self.commu.setDeviceIP_connect("MC")
        self.commu.setTypeMatchIP("MC")
        self.commu.setDeviceIP_connect("SM")
        self.commu.setTypeMatchIP("SM")
        self.commu.commamd_complexDeviceINFO("MQTT","")

        #read data from ini file section
        self.devicecData = self.devicecData.iloc[0:0] #clear old data
        self.commu.setDevice_name("EMU-B20MC")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)
        self.commu.setDevice_name("EMU-B20SM")
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20SM.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)

        self.deviceTable._data = self.devicecData
        self.deviceTable.layoutChanged.emit()
        #change ip in List checkbox
        self.appendToListCheck(True)
        self.setContexNoti.emit("refresh device table done")

    @Slot(str,str)
    def registDevice(self, ip,device): #add new deivce to iniconfig.ini
        self.commu.setPrintData([ip,device])
        self.commu.command_print_ini("initConfig","INI_config/ini_storage/")
        self.setContexNoti.emit("regist device done")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    #get context to page
    backEnd = Connect_page()
    #blinding model & backEnd to QML
    engine.rootContext().setContextProperty('LogFTPModel', backEnd.logTable) 
    engine.rootContext().setContextProperty('StatusModel', backEnd.statusTable)
    engine.rootContext().setContextProperty('DeviceModel', backEnd.deviceTable)
    engine.rootContext().setContextProperty("backend", backEnd)
    engine.rootContext().setContextProperty("homeBackend", backEnd)
    engine.rootContext().setContextProperty("UpdatbackEnd", backEnd)

    #load main file
    engine.load(os.fspath(Path(__file__).resolve().parent / "qml/main.qml"))
    if not engine.rootObjects():
        print("check root run error")
        sys.exit(-1)
    sys.exit(app.exec_())
