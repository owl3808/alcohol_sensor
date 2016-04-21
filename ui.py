# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
import os

pic_path=os.getcwd() + "/pic"

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
	self.showFullScreen()


    def startTest(self):
	# do text
	# display result
	self.outputArea.setPixmap(QPixmap(pic_path+'/5.jpg'))

app=QApplication(sys.argv)
testWidget=TestWidget()
testWidget.show()
sys.exit(app.exec_())
