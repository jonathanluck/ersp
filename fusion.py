import IRSensor
import UltrasonicSensor
import time

IR = IRSensor.IRSensor()
US = UltrasonicSensor.UltrasonicSensor(10, 8)

while True:
	print "IR: ", IR.avgDistance(40)
	print "US: ", US.avgDistance(40)
	time.sleep(1)
