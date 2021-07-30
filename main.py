# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import commu_file as commu
import logging

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, QTimer, Signal, Slot, QTime

class Connect_page(QObject):
    
    #create signal
    setContextTable = Signal(str,str,str,str,str, str, str, str)
    setBoolDeviceClear = Signal(bool)
    setBoolStatClear = Signal(bool)
    setContextStatus = Signal(str,str,str)
    setContexNoti = Signal(str)
    
    def __init__(self):
        QObject.__init__(self)
        
        self.errorCode = "0x0000"
        self.date ="07/555/2077"
        self.updateIP =[]

        logging.basicConfig(filename="config_debug.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
        self.commu = commu.commutnicate_app()
        self.commu.setDevice_name("EMU-B20MC")
        #self.commu.setFTP_connect()
        #self.commu.connection_FTP()
        #self.commu.disconnect_FTP()
             
    @Slot(bool)
    def refreshmentStatus(self, isState):
        self.setBoolStatClear.emit(isState)
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/log.ini")
        list_obj = self.commu.command_unpack_json(self.Table_data)
        
        for i in list_obj:
            self.setContextStatus.emit(i["ip"],i["date"],i["error"])

    @Slot(str)
    def updateFirmware(self, type):
        if(type == ""):
            logging.info("type connection from QML is NULL")
            self.setContexNoti.emit("type connection from QML is NULL")
        else:
            logging.info("connect type : "+type)
            for ip in self.updateIP:
                data = [ip,"no avalible","no avalible"]
                # self.commu.setModbus_connect(ip)
                # #logging.info(self.commu.getconnectIP())
                # statusConnect = self.commu.connnection_brige(type,ip) 
                # if(statusConnect == "connect"):
                #      #self.commu.command_update_firmware()
                #      #print("update IP: ",ip)
                #      #add print to log.ini 
                #      self.commu.setPrintData(data)
                #      self.commu.command_print_ini("log","INI_config/ini_storage/") 
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
        self.setBoolDeviceClear.emit(isState)  #call in main.qml to toggle state device botton
        # self.commu.setDevice_name("EMU-B20MC")
        # self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        # self.commu.setModbus_connect("init")
        
        # self.commu.commamd_complexDeviceINFO("Modbus",self.commu.getconnectIP())
        # self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        # list_obj = self.commu.command_unpack_json(self.Table_data)
        # for i in list_obj:
        #     self.setContextTable.emit(i["ip"],i["mac"],i["id"],i["mes"],i["sdc"],i["ntp"],i["tcp"],i["c_version"]) #call in homepage.qml to change device data table
        # if(isState == True):
        logging.info("init table done")
        # self.commu.setClearMod_ip()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    #get context to page
    backEnd = Connect_page()
    engine.rootContext().setContextProperty("backend", backEnd)
    engine.rootContext().setContextProperty("homeBackend", backEnd)
    engine.rootContext().setContextProperty("UpdatbackEnd", backEnd)

    #load main file
    engine.load(os.fspath(Path(__file__).resolve().parent / "qml/main.qml"))
    if not engine.rootObjects():
        print("check root run error")
        sys.exit(-1)
    backEnd.refreshmentTable(True)
    #print(backEnd.updateIP)
    sys.exit(app.exec_())
