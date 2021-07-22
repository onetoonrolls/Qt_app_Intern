# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import commu_file as commu

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
        #print("list obj : ",list_obj)
        for i in list_obj:
            self.setContextStatus.emit(i["ip"],i["date"],i["error"])

    @Slot(str)
    def updateFirmware(self, type):
        if(type == ""):
            print("type connection from QML is NULL")
            self.setContexNoti.emit("type connection from QML is NULL")
        else:
            print("connect type : ",type)
            for i in self.updateIP:
                data = [i,"02/05/9999","0x0000"]
                # self.commu.setModbus_connect(i)
                # statusConnect = self.commu.connnection_brige("Modbus") 
                #if(statusConnect == "connect"):
                    # self.commu.command_update_firmware()
                    #print("update IP: ",i)
                    #add print to log.ini 
                    #self.commu.setPrintData(data)
                    #self.commu.command_print_ini("log","INI_config/ini_storage/") 
                    # self.commu.disconnect()
                    #self.setContexNoti.emit("Update Ip : "+ i +" done")
                #elif(statusConnect == "unable_connect")
                    #self.setContexNoti.emit("Ip : "+ i +statusConnect)
                    
            self.setContexNoti.emit("Update Ip : "+ i +" done")

    @Slot(str)        
    def getUpdateIP(self, ip):
        if(ip == ""):
            print("ip is NULL")
        else:
                self.updateIP.append(ip)
                print("IP rev.")
    
    @Slot(bool)
    def refreshmentTable(self, isState): #refresh table
        self.setBoolDeviceClear.emit(isState)  #call in main.qml to toggle state device botton
        # self.commu.setDevice_name("EMU-B20MC")
        # self.commu.conmmand_clearINI("device","INI_config/ini_storage/config_EMU-B20MC.ini","INI_config/ini_storage/")
        # getIP = self.commu.getInitIP()
        # self.commu.commamd_complexDeviceINFO("device",getIP)
        self.Table_data,self.Table_head = self.commu.getINI_file("INI_config/ini_storage/config_EMU-B20MC.ini")
        list_obj = self.commu.command_unpack_json(self.Table_data)
        for i in list_obj:
            self.setContextTable.emit(i["ip"],i["mac"],i["id"],i["mes"],i["sdc"],i["ntp"],i["tcp"],i["c_version"]) #call in homepage.qml to change device data table
        if(isState == True):
            print("init table done")

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
    print(backEnd.updateIP)
    sys.exit(app.exec_())
