from datetime import time
from ftplib import FTP
import json
import logging

class FTP_client():

    def __init__(self):
        logging.basicConfig(filename="config_edit_log.txt", level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    def connect(self,ip,user,psw):
        self.client_FTP = FTP(ip,user,psw)

    def disconnect(self):
        self.client_FTP.quit()

    def list_all_file(self): #list file name return list or string
        return self.client_FTP.nlst()

    def check_file(self,check_word): #check name file return boolean
        for listword in self.list_all_file():
            if(listword.find(check_word) == -1):
                print("file not exist")
                return False
            else :
                print("file exist")
                return True

    def search_file(self,check_word): #check& find name file retrun list or string
        transferfile = []
        #if(self.check_file(check_word)):
        for FTPfilename in self.list_all_file(): 
            #print(FTPfilename)
            if(FTPfilename.find(check_word) > -1): #check name in list all file ->not macth =-1
                #print("return value: "+FTPfilename)
                transferfile.append(FTPfilename) 
        return transferfile

    def check_path(self): #check current path
        print(self.client_FTP.pwd())

    def change_type_object(self,type="utf-8"): #setting return form type
        self.encoding = type

    def path_folder_server(self,path_server): #move path  in server
        path = str(path_server).split('/')
        for i in path:
            if(i ==''):
                pass
            else:
                self.client_FTP.cwd(i)
        
        logging.info(self.client_FTP.pwd())
    
    def read_file(self,namefile): #read file in desktop path
        with open(self.Path_Download+namefile,'rb') as file:
            logging.info("open "+namefile)
            return file.read()

    def back_to_root(self): #move to root path server
        self.client_FTP.cwd("/")

    def download_file(self,filename,path): #download file from sever
        write_file = path+filename
        with open(write_file, "wb") as file:
            # use FTP's RETR command to download the file
            self.client_FTP.retrbinary(f"RETR {filename}", file.write)
        logging.info("download "+filename+" done")

    def check_firmware_ver_server(self): #check update firmware from detail.txt in server
        self.back_to_root() #reset path server
        self.Path_Download = "Test_server_client/transfer_file_log/"
        detail_name = "detail.txt"
        self.path_folder_server("/"+device_name+"/fw")
        if(self.check_file(detail_name)):
            self.download_file(detail_name,self.Path_Download)
            detail = self.read_file(detail_name)
            detail = json.loads(detail) #search info in detail.txt 
            least_version = detail["fw-ver"]
            return str(least_version)

    def check_log(self,device_name): #check log update firmware in server
        self.back_to_root()
        mac = []
        date = []
        #self.check_path()
        self.path_folder_server("/"+device_name+"/fw/log")
        #self.check_path()
        #use for check new version firmware 
        #if(self.check_file(self.check_firmware_ver_server())):
            #list_log = self.search_file("_v"+self.check_firmware_ver_server())
        list_log = self.search_file("v0124")
        #print("list log:",list_log)
        for i in range(len(list_log)):
            detail_log = list_log[i].split("_")
            mac.append(detail_log[0])
            date.append(detail_log[1])
       
        return mac,date,detail_log[2]
    
    def sort_detail(self,device_name): #use check log  to classify data to object form
        mac,date,ver = self.check_log(device_name)
        ojb_one =[]
        list_obj = []
        key_json = [{"mac","date","time","ver"}] #edit after change stackture ojb
        
        for i in range(len(date)):  
            date_T = date[i].split("T")
            #match data with topic in object form
            time = date_T[1][0:2]+":"+date_T[1][2:4]+":"+date_T[1][4:6]
            day = date_T[0][7:8]
            month = date_T[0][5:6]
            year = date_T[0][0:4]
            ver = ver[0:5]

            ojb_one.append(mac[i])
            ojb_one.append(day+"/"+month+"/"+year) 
            ojb_one.append(time)  
            ojb_one.append(ver)
            list_obj.append(ojb_one) #store info in list from
            ojb_one = []
        return list_obj,key_json
        
if __name__ == "__main__":

    #default setting
    ip = '128.199.174.101'
    user = 'ndrs-es'
    pws = 'XitoYjzR'
    device_name = "EMU-B20MC"
    Path_Download = "../transfer_file_log/"
    Path_server = "/"+device_name+"/fw/log"
    filename = "detail.txt" #test search
    
    #test class
    client_FTP = FTP_client()
    #client_FTP.setdefaultvalue()
    client_FTP.connect(ip,user,pws)
    # client_FTP.change_type_object()
    #firmware_ver = client_FTP.check_firmware_ver_server()
    #print(firmware_ver)
    #client_FTP.check_path()
    '''
    mac,date = client_FTP.check_log(device_name)
    for y in range(len(mac)):
        
        print("log mac "+ str(y+1) +": ",mac[y])
        print("log date "+ str(y+1) +": ",date[y])
        print("////////////////////////\n")
    
    client_FTP.check_path()
    '''
    lis,topic= client_FTP.sort_detail("EMU-B20MC")
    print(lis)
    lis,topic= client_FTP.sort_detail("EMU-B20SM")
    print(lis)
    client_FTP.disconnect()
    

    


