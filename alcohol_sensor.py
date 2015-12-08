import spidev
import time
import os
import unittest
import json
import numpy as np

class alcohol_sensor:
	def __init__(self, ch):
		# open(bus, device) : open(X,Y) will open /dev/spidev-X.Y
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		# Define sensor channels
		self.alcohol_ch = ch
		self.Vc = 5.0 # referance voltage
		#self.Rl = 200000 # load resistance
		self.RsroToConcentFile = 'MQ3Data.json'
		self.ResistToConcent = []
		self._loadMQ3Data()

	def _loadMQ3Data(self):
		json_text = open(self.RsroToConcentFile).read()
		data = json.loads(json_text)
		RsroToConcent = data['RsroConcentration_Mapping']
		Ro = data['Ro']
		self.ResistToConcent = [ [i[0]*Ro, i[1]] for i in RsroToConcent]
		print self.ResistToConcent
		self.Rl = data['Rl']

	# Read SPI data from MCP3008, Channel must be an integer 0-7
	def _ReadADC(self):
		if ((self.alcohol_ch > 7) or (self.alcohol_ch < 0)):
			return -1
		adc = self.spi.xfer2([1,(8+self.alcohol_ch)<<4,0])
		data = ((adc[1]&3)<<8) + adc[2]
		return data

	# Convert data to voltage level
	def _ReadVolts(self, data, deci):
		volts = (data * 5) / float(1023)
		volts = round(volts, deci)
		return volts

	# Calculate Resist from voltage
	def _ConvertVoltsToResist(self, Vrl):
		Rs = (self.Vc/Vrl-1)*self.Rl
		return Rs

	def getVolts(self):
		data = self._ReadADC()
		volts = self._ReadVolts(data, 2)
		return volts

	def getResist(self):
		volts = self.getVolts()
		resist = self._ConvertVoltsToResist(volts)
		return resist

	def getConcentration(self):
		volts = self.getVolts()
		resist = self._ConvertVoltsToResist(volts)
		concent = self._convertResistToConcentration(resist)
		print 'resist:%f  concent: %f' % (resist, concent)
		return concent

	def _convertResistToConcentration(self, resist):
		interval = self._findResistInterval(resist)
		if interval==-1:
			return 0 # less then alc_sensor curve table
		if interval == len(self.ResistToConcent)-1:
			return 10 # higher  then alc_sencor curve table
		# interpolation method to get concentation
		resist_l = self.ResistToConcent[interval][0]
		resist_h = self.ResistToConcent[interval+1][0]
		concent_l = self.ResistToConcent[interval][1]
		concent_h = self.ResistToConcent[interval+1][1]
		concent = concent_l + ((np.abs(resist - resist_l)/np.abs(resist_h-resist_l))*(concent_h - concent_l))
		return concent

	def _findResistInterval(self, resist):
		if resist > self.ResistToConcent[0][0]: # smaller then first one
			return -1
		for i in range(len(self.ResistToConcent)-1):
			if resist <= self.ResistToConcent[i][0] and resist > self.ResistToConcent[i+1][0]:
				return i
		else:
			return len(self.ResistToConcent)-1


# Unit test
class Test_AlcoholSensor(unittest.TestCase):
	def setUp(self):
		self.my_alcohol_sensor = alcohol_sensor(0)

	def test__ReadADC(self):
		adc_data = self.my_alcohol_sensor._ReadADC()
		self.assertEqual(int, type(adc_data))

	def test_ReadVolts(self):
		voltes = self.my_alcohol_sensor._ReadVolts(1023 ,2)
		self.assertEqual(5, voltes)
		voltes = self.my_alcohol_sensor._ReadVolts(0 ,2)
		self.assertEqual(0, voltes)
		voltes = self.my_alcohol_sensor._ReadVolts(511 ,2)
		self.assertEqual(2.5, voltes)

	def test_ConvertVoltsToResist(self):
		resist = self.my_alcohol_sensor._ConvertVoltsToResist(5)
		self.assertEqual(0, resist)
		resist = self.my_alcohol_sensor._ConvertVoltsToResist(2.5)
		self.assertEqual(200000, resist)

	def test_getVolts(self):
		volts = self.my_alcohol_sensor.getVolts()
		self.assertEqual(float, type(volts))

	def test_getResist(self):
		resist = self.my_alcohol_sensor.getResist()
		self.assertEqual(float, type(resist))

	def test_loadRsroToConcentationTable(self):
		self.my_alcohol_sensor._loadMQ3Data()
		self.assertEqual(list, type(self.my_alcohol_sensor.ResistToConcent))
		self.assertTrue(len(self.my_alcohol_sensor.ResistToConcent)>0)

	def test_convertResistToConcentration(self):
		self.my_alcohol_sensor.ResistToConcent = [[22,0],[9,1],[6,2],[5,3],[3,4],[2,5],[1,6]]
		concert = self.my_alcohol_sensor._convertResistToConcentration(0.5)
		self.assertEqual(9999, concert)
		concert = self.my_alcohol_sensor._convertResistToConcentration(1.5)
		self.assertEqual(5.5, concert)
		concert = self.my_alcohol_sensor._convertResistToConcentration(3.2)
		self.assertEqual(3.9, concert)
		concert = self.my_alcohol_sensor._convertResistToConcentration(5.2)
		self.assertEqual(2.8, concert)
		concert = self.my_alcohol_sensor._convertResistToConcentration(25)
		self.assertEqual(0, concert)

	def test_findResistInterval(self):
		self.my_alcohol_sensor.ResistToConcent = [[22,0],[9,1],[6,2],[5,3],[3,4],[2,5],[1,6]]
		interval = self.my_alcohol_sensor._findResistInterval(1.5)
		self.assertEqual(5, interval)
		interval = self.my_alcohol_sensor._findResistInterval(4.4)
		self.assertEqual(3, interval)
		interval = self.my_alcohol_sensor._findResistInterval(3)
		self.assertEqual(4, interval)
		interval = self.my_alcohol_sensor._findResistInterval(0.5)
		self.assertEqual(6, interval)
		interval = self.my_alcohol_sensor._findResistInterval(23)
		self.assertEqual(-1, interval)

def usage_example():
	alchl_sensor = alcohol_sensor(ch=0)
	# Define delay between readings
	delay = 1

	while True:
		concent = alchl_sensor.getConcentration()

		# Print out results
		print "alcohol %f" % concent

		# Delay seconds
		time.sleep(delay)


if __name__ == '__main__':
	#unittest.main()
	usage_example()
