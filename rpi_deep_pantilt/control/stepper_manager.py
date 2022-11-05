import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from multiprocessing import Manager
from multiprocessing import Process
import board
import adafruit_nunchuk




Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
nc = adafruit_nunchuk.Nunchuk(board.I2C())

# function to handle keyboard interrupt
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")
    	# disable the servos
    	Motor1.Stop()
    	Motor2.Stop()
    	GPIO.cleanup()
    # exit
	sys.exit()

# Independent Loop Processes
# 1. Panning
# 2. Tilting
# 3. Trigger

# function to handle pan motor
def pan():
	# loop indefinitely
	while True:
		x, y = nc.joystick
		demandy = abs(y-130)
		
		if demandy > 5:
			delay = (0.01/demandy)
			s = 0.05/delay
			if (y-130) > 0:
				Motor1.SetMicroStep('softward','1/32step')
				Motor1.TurnStep(Dir='forward', steps=int(s), stepdelay=delay)
				#print("steps / delay = {}/{}".format(int(s), delay))
			else:
				Motor1.SetMicroStep('softward','1/32step')
				Motor1.TurnStep(Dir='backward', steps=int(s), stepdelay=delay)
				#print("steps / delay = {}/{}".format(int(s), delay))
		else:
			Motor1.Stop()
			print ("pan stopped")
			time.sleep(0.5)

# function to handle tilt motor			
def tilt():
	# loop indefinitely	
	while True:	
		x, y = nc.joystick
		demandx = abs(x-130)
		if demandx > 3:
			delay = (0.01/demandx)
			s = 0.05/delay
			if (y-130) > 0:
				Motor2.SetMicroStep('softward','1/32step')
				Motor2.TurnStep(Dir='forward', steps=int(s), stepdelay=delay)
				#print("steps / delay = {}/{}".format(int(s), delay))
			else:
				Motor2.SetMicroStep('softward','1/32step')
				Motor2.TurnStep(Dir='backward', steps=int(s), stepdelay=delay)
				#print("steps / delay = {}/{}".format(int(s), delay))
		else:
			Motor2.Stop()
			print ("tilt stopped")
			time.sleep(0.5)		

# function to handle trigger actions	
def trigger():	
	# loop indefinitely
	while True:
		if nc.buttons.Z:
			# Add trigger relay code
			print("Pew! Pew! Pew!")

if __name__ == "__main__":
	
	# start manager for process-safe variables - maybe declare Motor1/2 in here?
	with Manager() as manager:
		# set values for joystick values
		#joyX = manager.Value("i", 0)
		#joyY = manager.Value("i", 0)
		#joyZ = manager.Value("i", 0)

		# set up independent processes
		processPanning = Process(target=pan)
		processTilting = Process(target=tilt)
		processTrigger = Process(target=trigger)
		
		# start all processes
		processPanning.start()
		processtilting.start()
		processTrigger.start()
		
		# join all processes
		processPanning.join()
		processTilting.join()
		processTrigger.join()
		
		# stop motors when all processes exit
		Motor1.Stop()
		Motor2.Stop()
        	
