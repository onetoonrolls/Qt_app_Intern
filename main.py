# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import commu_file as commu
import logging
import pandas as pd

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import *

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
        
        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
        self.commu = commu.commutnicate_app()
        self.commu.setDevice_name("EMU-B20MC")
        #self.commu.setFTP_connect()
        #self.commu.connection_FTP()
        #self.commu.disconnect_FTP()

        #create TabelModel section
        self.devicetopic =['ip','mac','id','mes','sdc','ntp','tcp','c_version']
        self.devicecData = pd.DataFrame(columns=self.devicetopic)
        self.statustopic=['ip','mac','date','error'] #****lack mac form update***
        self.statusData = pd.DataFrame(columns=self.statustopic)
        
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("status",self.list_obj)

        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)

        self.deviceTable = TableModel(self.devicecData)
        self.statusTable = TableModel(self.statusData)
        
    def tableSetData(self,table,data):
        for i in data:
            if(table == "device"):
                self.devicecData = self.devicecData.append(i,ignore_index=True)
            elif(table == "status"):
                self.statusData = self.statusData.append(i,ignore_index=True)
            else:
                logging.info("unmatch table")

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
        
    @Slot(str)
    def updateFirmware(self, type):
        if(type == ""):
            logging.info("type connection from QML is NULL")
            self.setContexNoti.emit("type connection from QML is NULL")
        else:
            logging.info("connect type : "+type)
            for ip in self.updateIP:
                updateMac = self.findMacUpdate(ip)
                data = [ip,updateMac,"no avalible","no avalible"]
                # self.commu.setModbus_connect(ip)
                # #logging.info(self.commu.getconnectIP())
                # statusConnect = self.commu.connnection_brige(type,ip) 
                # if(statusConnect == "connect"):
                #      #self.commu.command_update_firmware()
                #      #print("update IP: ",ip)
                #      #add print to log.ini 
                self.commu.setPrintData(data)
                self.commu.command_print_ini("log","INI_config/ini_storage/") 
                #      self.commu.disconnect_brige()
                #      self.setContexNoti.emit("Update Ip : "+ ip +" done")
                #      logging.info("Update Ip : "+ ip +" done")
                # elif(statusConnect == "unable_connect"):
                #      logging.info("unable connect")
                #      self.setContexNoti.emit("Ip : "+ ip +statusConnect)
            
            self.setContexNoti.emit("Update Ip : "+ ip +" done")
            self.commu.setClearMod_ip()

    @Slot(str)        
    def getUpdateIP(self, ip):
        if(ip == ""):
            logging.info("ip is NULL")
        else:
            self.updateIP.append(ip)
            logging.info("IP rev.")
    
    @Slot(bool)
    def refreshmentTable(self, isState): #refresh table
        #fetch newdata from device section
        # self.commu.setDevice_name("EMU-B20MC")
        # self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        # self.commu.setModbus_connect("init")
        #self.commu.commamd_complexDeviceINFO("Modbus",self.commu.getconnectIP())
        #read data from ini file section
        self.devicecData = self.devicecData.iloc[0:0] #clear old data
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        self.list_obj = self.commu.command_unpack_json(self.Table_data)
        self.tableSetData("device",self.list_obj)
        self.deviceTable._data = self.devicecData
        self.deviceTable.layoutChanged.emit()
        #change ip in List checkbox
        self.appendToListCheck(True)
        logging.info("device table changed")
        

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    #get context to page
    backEnd = Connect_page()
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
