from socket import *
try:
    import RPi.GPIO as GPIO # general purpose input-output for the RP
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

HOST = #master
PORT = 5001
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

GPIO.setmode(GPIO.BOARD) # I think it is better to use BOARD
channel = #channel number based on the numbering system have specified (BOARD or BCM)

GPIO.setup(channel, GPIO.IN) #set up incoming channel for the pion

pion_input = False # initialize just in case, not sure how it works for now, may have defaulted to false right away
pion_input = GPIO.input(channel)

while 1:
    if (pion_input): # things happened!
        # get things unpacked from the input
        
        # TODO: limit the running time? we have to protect from a stupid output.
        # TODO: in case of any error, we should send the signal back indicating that pion couldn't make it 
        # do the work
        
        
        s.send(answer, id) # send result of work back to server
        # s.close()
        # print 'Received', repr(data)