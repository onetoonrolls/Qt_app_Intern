# description
  this program generate application for communication bewteen Modbus TCP & MQTT & FTP server and organize device(EMU B20MC&B20SM)
# Init setting before run program

  -add INI file in INI_config/ini_storage; file name initConfig.ini
  
  -add context in iniConfig.ini **section,key must be same example below
  
  /////Example ///// 
  
  [FTP server] <- FTP sitting
  
    host_ip = 127.0.0.1
    
    username = xxxxx
    
    password = xxxxx
    
    port = xxx

  [EMU-B20MC-init] <-device ip
  
    initip-1 = 127.0.0.1
    
  # Requirement
    -python 3.9.6 lib
    
    -pymodbus
    
    -configparser
    
    **you can download module script in requirement.txt
    
    
