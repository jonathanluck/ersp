import RPi.GPIO as GPIO
import time
import numpy
GPIO.setmode(GPIO.BOARD)


class UltrasonicSensor:
	def __init__(self, trigger, echo):
		self.TRIG = trigger
		self.ECHO = echo
		GPIO.setup(self.TRIG,GPIO.OUT)
		GPIO.setup(self.ECHO,GPIO.IN)
        
	def getDistance(self):
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)
		timeout= pulse_start = pulse_end = time.time()
	
		while GPIO.input(self.ECHO) == 0:
			pulse_start = time.time()
			if(time.time() - timeout > 0.024):
				return -1
		
		while GPIO.input(self.ECHO)==1:
			pulse_end = time.time()
		
		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150
		distance = round(distance, 2)
		return distance
	
	def medianDistance(self, n):
		a = []
		for i in range(n):
			a.append(self.getDistance())
		return sorted(a)[n/2]
	
	def avgDistance(self, n):
		a = []
		for i in range(n):
			b = self.getDistance()
			if(b != -1):
				a.append(b)
		return(numpy.average(a), numpy.var(a))
