# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth, subprocess

def receiveMessages(targetBluetoothMacAddress):
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  print(server_sock)
  port = 1
  server_sock.bind((targetBluetoothMacAddress,port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  
  data = client_sock.recv(1024)
  print ("received [%s]" % data)
  
  client_sock.close()
  server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  print(sock)
  sock.connect((targetBluetoothMacAddress, port))
  print("Sending...")
  sock.send("hello!!")
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    name = bluetooth.lookup_name(bdaddr)
    print (name + " [" + str(bdaddr) + "]")
    if "Nick" in name:
      print "FOUND"
      receiveMessages(bdaddr)
    
    
lookUpNearbyBluetoothDevices()
