import pymongo
import RPi.GPIO as GPIO 
import MFRC522 
import signal 
import time
import json
from datetime import date 
import datetime

GPIO.setwarnings(False);
continue_reading = True
myclient = pymongo.MongoClient("mongodb://mongo:27017/")

mydb = myclient["dbSHome"]
mylog = mydb["log"]
myuser = mydb["user"]

# dblist = myclient.list_database_names()
# if "RFID" in dblist:
#   print("The database exists.")


GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(7)


# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Looking for cards")
print("Press Ctrl-C to stop.")

# This loop checks for chips. If one is near it will get the UID
try:
  
  while True:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

      # Print UID
        myquery = { "uid": str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]) }
        doc = myuser.find(myquery)
        x = {"uid": str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])}
        y = json.dumps(x); # parsare JSON

        
        for w in doc:
            print(w)
            
            print(y) #print RFID
            if len(w) > 1:
                print("Acces OK!")
                #print("Card UID: "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
                x = datetime.datetime.now()
                mydict = { "uid": str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]), "nume" : w["nume"], "data" : x }
                x = mylog.insert_one(mydict)
                print(len(w))
                GPIO.output(3, True)
                pwm.ChangeDutyCycle(2)
                time.sleep(5)
                GPIO.output(3, True)
                pwm.ChangeDutyCycle(7)
               
            else:
                print("Acces Neautorizat!")
                print("Card UID: "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
                time.sleep(2)




except KeyboardInterrupt:
  GPIO.cleanup()