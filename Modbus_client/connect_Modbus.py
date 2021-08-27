from os import path
from pymodbus import client
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
from pymodbus.file_message import WriteFileRecordRequest
import logging

class Modbus_connect():
    
    def __init__(self) :
        self.hex_mac = ""

    #test display list from module
    def print_outputFrom_register(result):
        for i in range(result) :
            print("round"+str(i)+": "+hex(result[i]))

     #connect Modbus TCP client
    def connect_client(self,ip_add):
        self.Client_Modbus = ModbusTcpClient(ip_add)
        #print("status modbus connect:",self.Client_Modbus)
        if(self.Client_Modbus.connect()): #check connection
            return "connect"
        else:
            return "unable_connect"

    def disconect(self):
        self.Client_Modbus.close()
        
    #convert to mac(HEX) to string
    def mac_convertTOstring(self,mac):
        #print("mac :",mac)
        for i in mac:
            #print("type i ",type(i))
            try:
                one_mac = hex(i)
                self.hex_mac += one_mac
            except:
                pass
        #print(self.hex_mac)
        self.hex_mac = "0x"+self.uppercase_string(self.hex_mac.replace("0x",""))
        return self.hex_mac

    #convert status to string
    def status_convert(self,stu):
        if(stu == hex(0)):
            return "normal"
        elif(stu == hex(99)):
            return "abnormal"
        else:
            return "None"

    def uppercase_string(self,word):
        NWord =""
        for i in word:
            switcher = {
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "e": "E",
                "f": "F"   
            }
            NWord += switcher.get(i,i)
        return NWord
                
    #write single&multi register values
    #bit_address = device bit-address 
    #bit_value = payload 
    #num_regist = in case multi-writ **default =1**
    def write_bit_register(self,bit_value=1,bit_address=0,num_regist=1):
        self.Client_Modbus.write_registers(bit_address,[bit_value]*num_regist)

    def mac_read(self):
        mac_addr = 0x0000
        mac_read = self.mac_convertTOstring(self.Client_Modbus.read_holding_registers(mac_addr,3).registers)
        return mac_read

    def firmware_read(self):
        version_addr =0x0001
        firmVersion_read = self.Client_Modbus.read_input_registers(version_addr,1).registers
        return hex(firmVersion_read[0])

    def device_id_read(self):
        deID_addr = 0x0000
        deID = self.Client_Modbus.read_input_registers(deID_addr,1).registers
        return  hex(deID[0])

    def status_read(self):
        status_addr = 0x038A
        status = self.Client_Modbus.read_input_registers(status_addr,4).registers
        
        MES_sta = self.status_convert(hex(status[0]))
        SDC_sta = self.status_convert(hex(status[1]))
        NTP_sta = self.status_convert(hex(status[2]))
        TCP_sta = self.status_convert(hex(status[3]))
        status_con =[MES_sta,SDC_sta,NTP_sta,TCP_sta]
        
        return status_con

    def update_firmware(self):
        OTA_update_addr = 0x010F
        self.write_bit_register(0x1,OTA_update_addr,1)

    def get_info_device(self):
        mac = self.mac_read()
        ver = self.firmware_read()
        id = self.device_id_read()
        status = self.status_read()
        return mac,ver,status,id



if __name__ == "__main__":
    
    path = '/ini/EMU-B20MC'
    #connect client
    
    
    M = Modbus_connect()
    print(M.connect_client("1*"))
    M.update_firmware()
    #print(M.get_info_device())
    #print(M.connect_client("172.16.5.65"))
    # print(M.connect_client(ip)) #test status connect
    # #test read
    # #mac = M.mac_read()
    # #print("\nmac: ",mac)
    # M.disconect()
    # print(M.connect_client(ip))
    # M.disconect()
    '''
    device_ID = device_id_read()
    print("\ndevice ID: "+str(device_ID))
    firmVersion = fireware_read()
    print("\nver.device: "+str(firmVersion))
    MES,SDC,NTP,TCP = status_read()
    print("MES status: "+MES)
    print("\nSDC status: "+SDC)
    print("\nNTP status: "+NTP)
    print("\nTCP status: "+TCP)

    #test write

    #///////////////////////////////////////////////////////////////////////////////////////////////////////

    FTP_data={"ip address":ip,"mac address":mac}
    status = {"MES status":MES,"SDC status":SDC,"NTP status":NTP,"TCP status":TCP}
    ini_print("EMU-B20MC",status,FTP_data,firmVersion,device_ID)
    test_dic_convert = read_INI_to_dict(path)
    print(test_dic_convert)

    #close connection
    client.close()
    '''