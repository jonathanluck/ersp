import Adafruit_ADS1x15
import time
import math
import numpy


class IRSensor:
	def __init__(self):
		
		self.adc = Adafruit_ADS1x15.ADS1015()
	
	def getDistance(self):
		return self.analogtodistance(self.adc.read_adc(0, 2/3))

	def analogtodistance(self, n):
		n =  n * 6114.0 / 2048.0 * 1024.0 / 5000.0
		n = 1.0 / n
		return pow(math.e, (0.0028345967 + n)/0.00105134097)
	
	def medianDistance(self, n):
		a = []
		for i in range(n):
			a.append(self.getDistance())
			time.sleep(0.001)
		return sorted(a)[n/2]
	
	def avgDistance(self, n):
		a = []
		for i in range(n):
			b = self.getDistance()
			if(b <= 700):
				a.append(b)
		return(numpy.average(a), numpy.var(a))
