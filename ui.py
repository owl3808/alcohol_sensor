# -*- coding: utf-8 -*-

import sys
import os
from PyQt4.QtGui import *
import pygame
from time import sleep

pic_path=os.getcwd() + "/pic"
audio_path=os.getcwd() + "/audio"

class TestWidget(QWidget):
	def __init__(self):
		QWidget.__init__(self, windowTitle=u"A Simple Example for PyQt.")
		self.outputArea=QLabel()
		self.outputArea.setText(u'開車不喝酒 喝酒不開車\n開車前請進行酒測')
		self.startButton=QPushButton(u"開始酒測", self)
		self.setStyleSheet('font-size: 18pt; font-family: Courier;')
		self.startButton.clicked.connect(self.startTest)

		self.setLayout(QVBoxLayout())
		self.layout().addWidget(self.outputArea)
		self.layout().addWidget(self.startButton)
		#self.showFullScreen()


	def startTest(self):
		# do text
		self.outputArea.setText(u"請開始吹氣")
		self.outputArea.repaint()
		concent = 0
		avg_concent = 0
		for i in range(5):
			self.outputArea.setText(u"請開始吹氣..."+str(5-i))
			self.outputArea.repaint()
			for i in range(5):
				concent = concent + alchl_sensor.getConcentration() * 0.2
				sleep(0.2)
			avg_concent = concent * 0.2 # average 5 times

		# Print out results
		print "alcohol %f" % concent
		if avg_concent == 0:
			self.outputArea.setPixmap(QPixmap(pic_path+'/1.jpg'))
			pygame.mixer.music.load(audio_path + '/alc0.mp3')
			pygame.mixer.music.play(1)
		elif avg_concent <= 0.15:
			self.outputArea.setPixmap(QPixmap(pic_path+'/2.jpg'))
			pygame.mixer.music.load(audio_path + '/alc0-015.mp3')
			pygame.mixer.music.play(1)
		elif avg_concent > 0.15 and avg_concent < 0.25:
			self.outputArea.setPixmap(QPixmap(pic_path+'/3.jpg'))
			pygame.mixer.music.load(audio_path + '/alc015-025.mp3')
			pygame.mixer.music.play(1)
		elif avg_concent >= 0.25 and avg_concent < 0.4:
			self.outputArea.setPixmap(QPixmap(pic_path+'/4.jpg'))
			pygame.mixer.music.load(audio_path + '/alc025-040.mp3')
			pygame.mixer.music.play(1)
		elif avg_concent >= 0.4 and avg_concent < 0.55:
			self.outputArea.setPixmap(QPixmap(pic_path+'/5.jpg'))
			pygame.mixer.music.load(audio_path + '/alc040-055.mp3')
		else :
			self.outputArea.setPixmap(QPixmap(pic_path+'/6.jpg'))
			pygame.mixer.music.load(audio_path + '/alc055.mp3')
			pygame.mixer.music.play(1)
		#localtime = time.asctime( time.localtime(time.time()) )
		#print str(localtime)

class fack_alcosensor:
	value = 0
	def __init__(self):
		self.value=0
	def getConcentration(self):
		return self.value

def test():
	global alchl_sensor
	alchl_sensor =  fack_alcosensor()
	alchl_sensor.value = 0.22 # set alco value
	pygame.mixer.pre_init(44100, -16, 2048)
	pygame.init()
	pygame.mixer.init()
	app=QApplication(sys.argv)
	testWidget=TestWidget()
	testWidget.show()
	sys.exit(app.exec_())

# Main function
def main():
	from alcohol_sensor import alcohol_sensor
	alchl_sensor = alcohol_sensor(ch=0)
	pygame.mixer.pre_init(44100, -16, 2048)
	pygame.init()
	pygame.mixer.init()
	app=QApplication(sys.argv)
	testWidget=TestWidget()
	testWidget.show()
	sys.exit(app.exec_())

# single pc test
#test()

# main
main()
