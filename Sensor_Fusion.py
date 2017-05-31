import numpy
import math
import IRSensor
import UltrasonicSensor
import time
import json

def makeweights(var1, var2):
    #weights for (1)IR and (2)ultrasonic
    w1 = var2 / (var1 + var2)
    w2 = var1 / (var1 + var2)

    if (w1 < 0.05):
        w1 = 0.05
        w2 = 0.95

    if (w2 < 0.05):
        w2 = 0.05
        w1 = 0.95
    return(w1,w2)

#creating the probability density function
def mixture(x, mean1, var1, mean2, var2):

    #standard deviation
    sd1 = math.sqrt(var1)
    sd2 = math.sqrt(var2)
    
    w1, w2 = makeweights(var1, var2)

    #Gaussain distribution for IR
    power1 = -pow(x - mean1, 2)/(2*pow(sd1, 2))
    dist1 = 1/math.sqrt(2*math.pi*pow(sd1, 2)) * pow(math.e, power1)


    #Gaussian distribution for ultrasonic
    power2 = -pow(x - mean2, 2)/(2*pow(sd2, 2))
    dist2 = 1/math.sqrt(2*math.pi*pow(sd2, 2)) * pow(math.e, power2)

    #mixture model
    distribution = w1*dist1 + w2*dist2
    return distribution


out_filename = "data.json"
IR = IRSensor.IRSensor()
US = UltrasonicSensor.UltrasonicSensor(10, 8)

num = 1000
#start, stop, number of samples
xvalues = numpy.linspace(0, 1000, num)
while True:
	yvalues = []
	ir = IR.avgDistance(50);
	us = US.avgDistance(25);
	irweight, usweight = makeweights(ir[1], us[1])
	#print(ir,us)
	if(ir[0] > 700 and us[0] == -1):
		print "No data"
		continue
	
	for x in xvalues:
	    yvalues.append(mixture(x, ir[0], ir[1], us[0], us[1]))
	#creating the cumulative distribution function
	step = xvalues[1] - xvalues[0]
	area = []
	xaxis = []
	total = 0

	target = 0.5
	#multiple distances
	#distances = [[None, None, None] for i in range(10)]
	#actual values for the quartiles
	values = []
	tol = 0.005

	for y in range(0, num - 2):
	    ave = (yvalues[y] + yvalues[y+1])/2
	    xaxis.append(xvalues[y+1])
	    total += ave * step

	    if((target - tol <= total <= target + tol) or total > target):
	    	#print "Distance: ", xaxis[y]
		out = [ir[0], ir[1], irweight, us[0], us[1], usweight, xaxis[y]]
		f = open(out_filename, 'w')
		f.write(json.dumps(out))
		f.close()
		break

	    area.append(total)
