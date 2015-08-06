import spidev
import time
import os
import unittest
import json

class alcohol_sensor:
	def __init__(self, ch):
		# open(bus, device) : open(X,Y) will open /dev/spidev-X.Y
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		# Define sensor channels
		self.alcohol_ch = ch
		self.Vc = 5 # referance voltage
		self.Rl = 200000 # load resistance
		self.RsroToConcentFile = 'MQ3Data.json'
		self.ResistToConcent = []

	def _loadMQ3Data(self):
		json_text = open(self.RsroToConcentFile).read()
		data = json.loads(json_text)
		RsroToConcent = data['RsroConcentration_Mapping']
		Ro = data['Ro']
		self.ResistToConcent = [ [i[0]*Ro, i[1]] for i in RsroToConcent]

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

	def _ConvertResistToConcentration(self, resist):
		return 'function undefinded'

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

	def test_ConvertResistToConcentration(self):
		self.my_alcohol_sensor._ConvertResistToConcentration(1)

'''def usage_example():
	alcohol_sensor(ch=0)
	# Definedd sensor channels
	alcohol_ch = 0
	
	# Define delay between readings
	delay = 1

	while True:
		# Read the light sensor data
		alcohol_data = ReadADC(alcohol_ch)
		alcohol_volts = ReadVolts(alcohol_data,2)
		alcohol_resist = ConvertVoltsToResist(alcohol_volts)

		# Print out results
		print "%.2f (V) %.0f (Ohm)" % (alcohol_volts, alcohol_resist)

		# Delay seconds
		time.sleep(delay)
'''

if __name__ == '__main__':
	unittest.main()
	#usage_example()
