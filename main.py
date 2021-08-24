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

class countTime(th):

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

    def setupdatefunction(self,update,type,listIP,connect,setcon,discon,clear):
        self.conType = type  #connect type
        self.listIP = listIP #get all update ip
        #pass function
        self.updateDevice = update #update
        self.connect = connect #connect device
        self.setcon = setcon #set ip to commu
        self.discon = discon #disconnect device
        self.clearUp = clear #clear list ip update

    def settime(self):
        delta = self.bufferTimer.pop(0)
        #print("pop : ",delta)
        delta = str(delta).split(":")
        #print("split :",delta)
        self.hour = int(delta[0])
        self.min = int(delta[1])
        self.sec = int(delta[2])
        self.status = "alraedy set"

    def setbufferTimer(self,tdelta):
        self.bufferTimer.append(str(tdelta))
        self.status = "wait"
        #print("list timer : ",self.bufferTimer)
        
    def countdown(self):
        
        self.status = "clock running"
        t = self.hour*60*60+self.min*60+self.sec
        while t:
        # Divmod takes only two arguments so
        # you'll need to do this for each time
        # unit you need to add
            if(self.stoptime == True):
                break
            mins, secs = divmod(t, 60) 
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)
            self.timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs) 
            print(self.timer, end="\r") 
            time.sleep(1) 
            t -= 1
        if(self.stoptime == True):
            self.status = "cancle"
            logging.info("cancle")
        else:
            self.status = "done"
        self.stoptime = False

    def getTimer(self):
        return self.timer

    def getstatusTimer(self):
        return self.status

    def run(self):
        self.settime()
        self.countdown()
        for ip in self.listIP:
            self.connect(ip) #self.commu.setModbus_connect(ip)
            statusConnect = self.connect(self.conType,ip) #self.commu.connnection_brige(type,ip) 
            if(statusConnect == "connect"): #check connect device
                self.updateDevice()    
                self.discon()
        self.clearUp()
        self.bufferTimer =[]
        logging.info("timer done")

class TableModel(QAbstractTableModel): #model view prototype
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
        self.listSetData("hour")
        self.listSetData("min")
        self.dataHour = pd.DataFrame(self.hour,columns=["hour"])
        self.dataMin = pd.DataFrame(self.min,columns=["min"])
        self.timer = countTime()
        #self.timer = countTime(self.testfunc)
          
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
        self.commu = commu.commutnicate_app()
        self.commu.setDevice_name("EMU-B20MC")
        
        #create TabelModel section
        self.devicetopic =['ip','mac','id','mes','sdc','ntp','tcp','c_version']
        self.devicecData = pd.DataFrame(columns=self.devicetopic)
        self.statustopic=['ip','mac','date','error'] 
        self.statusData = pd.DataFrame(columns=self.statustopic)
        self.logtopic=['mac','date','version'] 
        self.logData = pd.DataFrame(columns=self.logtopic)
        
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("status",self.list_obj)

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

        self.deviceTable = TableModel(self.devicecData)
        self.statusTable = TableModel(self.statusData)
        self.logTable = TableModel(self.logData)
    
    def checkFTPlog(self):
        #connectFTP
        self.commu.setFTP_connect()
        self.commu.connection_FTP()
        

    def listSetData(self,type):
        num = ""
        if(type == "hour"):
            for i in range(12):
                self.hour.append(i+1)
        elif(type == "min"):
            for i in range(60):
                self.min.append(i)

    def settimer(self,h,m):
        self.timer = countTime(self.commu.command_update_firmware)
        #self.timer = countTime(self.testfunc)
        
        FMT = "%d-%m %H:%M"
        currentDateTime = datetime.now()
        #print(currentDateTime.strftime("%D:%H:%M"))
        now = currentDateTime.strftime(FMT)
        #print(now)
        nowHour = currentDateTime.hour
        if(h == "-1"):
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
            tdelta = datetime.strptime(date2,FMT)-datetime.strptime(now,FMT)
        self.timer.setbufferTimer(tdelta)

    @Slot(int,int,int)
    def setTimeupdate(self,hour,min,posfix):
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
    def cancleTimer(self,stop):
        self.timer.stoptime = stop
        self.timer.bufferTimer = []
        self.timer.hour = 0
        self.timer.min = 0
        self.timer.sec = 0

    def starCount(self):
        self.timer.start()

    def tableSetData(self,table,data):
        for i in data:
            if(table == "device"):
                self.devicecData = self.devicecData.append(i,ignore_index=True)
            elif(table == "status"):
                self.statusData = self.statusData.append(i,ignore_index=True)
            elif(table == "logFTP"):
                self.logData = self.logData.append(i,ignore_index=True)
            else:
                logging.info("unmatch table")

    def findIP(self,mac):
        index = self.devicecData[self.devicecData['mac']== mac].index.values.astype(int)[0]
        ip = self.devicecData.iat[index,1]
        return ip

    def findMacUpdate(self,updateIP):
        index = self.devicecData[self.devicecData['ip']== updateIP].index.values.astype(int)[0] #find index
        updateMac = self.devicecData.iat[index,1] #get device mac
        return updateMac
    
    def getALLdeviceIP(self):
        listIP = self.devicecData['ip'].tolist()
        return listIP
    
    @Slot(bool)
    def appendToListCheck(self, isState):
        self.setClearListcheck.emit(True)
        listIP = self.getALLdeviceIP()
        for ip in listIP:
            self.setContextListcheck.emit(ip)
        
    @Slot(bool)
    def refreshmentStatus(self, isState):
        self.statusData = self.statusData.iloc[0:0] #clear old data
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini")
        list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("status",list_obj)
        self.statusTable._data = self.statusData
        self.statusTable.layoutChanged.emit()
        logging.info("status table changed")
        self.setContexNoti.emit("refresh status done")
        
    @Slot(str)
    def updateFirmware(self, type):
        if(type == ""):
            logging.info("type connection from QML is NULL")
            self.setContexNoti.emit("type connection from QML is NULL")
        else:
            #self.timer.setupdatefunction(self.commu.command_update_firmware,type,self.updateIP,self.commu.connnection_brige,self.commu.setClearMod_ip,self.commu.disconnect_brige,self.commu.setClearMod_ip)
            for ip in self.updateIP:  #add print to log.ini 
                updateMac = self.findMacUpdate(ip)
                data = [ip,updateMac,"no avalible","no avalible"]      
                self.commu.setPrintData(data)
                self.commu.command_print_ini("log","INI_config/ini_storage/") 
            self.starCount()
            self.setContexNoti.emit("update commit done")

    @Slot(str)        
    def getUpdateIP(self, ip):
        if(ip == ""):
            logging.info("ip is NULL")
        else:
            self.updateIP.append(ip)
            logging.info("IP rev.")
    
    @Slot(bool)
    def refreshmentLog(self, isState):
        #fetch newdata from device section
        self.commu.conmmand_clearINI("logFTP","INI_config/ini_storage/logFTP.ini","INI_config/ini_storage/")
        self.commu.connection_FTP()
        self.commu.setDevice_name("EMU-B20MC")
        MC,topic =self.commu.getlogFTP() 
        self.commu.setDevice_name("EMU-B20SM")
        SM,topic =self.commu.getlogFTP()
        self.commu.disconnect_FTP()
        #write section
        for i in MC:
            self.commu.setPrintData(i)
            self.commu.command_print_ini("logFTP","INI_config/ini_storage/")
        for i in SM:
            self.commu.setPrintData(i)
            self.commu.command_print_ini("logFTP","INI_config/ini_storage/")
        #read section
        self.logData = self.logData.iloc[0:0]
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/logFTP.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("logFTP",self.list_obj)
        self.logTable._data = self.logData
        self.logTable.layoutChanged.emit()
        self.setContexNoti.emit("update log FTP table")

    @Slot(bool)
    def refreshmentTable(self, isState): #refresh table
        #fetch newdata from device section
        # self.commu.setDevice_name("EMU-B20MC")
        # self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        # self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20SM.ini","INI_config/ini_storage/")
        # self.commu.setModbus_connect("init")
        #self.commu.commamd_complexDeviceINFO("Modbus",self.commu.getconnectIP())

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
    def registDevice(self, ip,device):
        self.commu.setPrintData([ip,device])
        self.commu.command_print_ini("initConfig","INI_config/ini_storage/")
        self.setContexNoti.emit("regist device done")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    #get context to page
    backEnd = Connect_page()
    
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
