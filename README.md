# Description

  this program generate application for communication bewteen Modbus TCP & MQTT & FTP server and organize device(EMU B20MC&B20SM)

# Instruction 
  
  	Step 1 file set up

  		-create INI file name "iniConfig.ini" in format:
  ![1](https://user-images.githubusercontent.com/73213619/133962537-9f39a2e7-a44e-4f96-9a8c-0d2007fc6c54.PNG)
  		host_ip,server_ip,initip <-ip address type *application can edit initip 
		port <-int type FTP port defult is 21
		username,password <-string type upon user setting to server
  		-move "iniConfig.ini" to .../INI_config/ini_storage
  ![2](https://user-images.githubusercontent.com/73213619/133970769-e2b7c8bc-9a83-4f9d-acc7-4a8dea36e0ec.PNG)

  	Step 2 module set up 

  		-install requirement.txt with command "pip install -r requirements.txt" or install with single module with command "pip install module_name"
  
  	Step 3 application introduction
  
  		-basic tools
  ![5](https://user-images.githubusercontent.com/73213619/133968804-268a4e30-e338-48bc-a3e3-731125ade818.png)

  		-home page tools
  ![6](https://user-images.githubusercontent.com/73213619/133968871-21c7f629-edaf-4aeb-aec0-9d2cd1331df5.png)
  
  		-update page tools
  ![7](https://user-images.githubusercontent.com/73213619/133968945-42f3df0a-412a-47dc-92fa-49acb3d24cf3.png)

# Function description

  	->universal tools bar : refresh table in each page

  	->update tools : select device ip and protocol then submit in update page controller *note time counting is avaliable* 
			 when comfirm update to devices data will record in log.ini
  
  	->notification system : automatic display text when user pocess something in application
  
  	->register devices system : receive IP & type of device to add data in initConfig.ini
  
  	->Registed-devicecs system : display table from config_EMU-B20MC.ini&config_EMU-B20SM.ini when user click on refresh button

  	->Update log system(home page) : display table from logFTP.ini when user click on refresh button

  	->Update log system(update page) : display table from log.ini when user click on refresh button
 
# Requirement

    -python 3.9.6 lib
    
    -pymodbus
    
    -configparser

    -paho-MQTT
    
    **this script avaliable in requirement.txt
    
    
