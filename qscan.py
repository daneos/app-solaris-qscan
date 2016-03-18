#!/usr/bin/env python

import os
import re
import sys
import time
import numpy
import taurus
import PyTango
from StringIO import StringIO
from taurus.external.qt import uic, QtCore, QtGui

ui = StringIO("""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>526</width>
    <height>463</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>QuickScanGUI</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QGroupBox {
     border: 2px solid black;
     border-radius: 10px;
	padding: 7px;
 }

QGroupBox::title {
	position: relative;
	top: -5px;
	padding: 2px;
}</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout_8">
    <item>
     <layout class="QHBoxLayout" name="horizontalLayout_8">
      <item>
       <widget class="QGroupBox" name="step1">
        <property name="minimumSize">
         <size>
          <width>250</width>
          <height>0</height>
         </size>
        </property>
        <property name="title">
         <string>Step 1: Select device</string>
        </property>
        <layout class="QVBoxLayout" name="verticalLayout_2">
         <item>
          <widget class="QLineEdit" name="devFilterEdit">
           <property name="placeholderText">
            <string>filter</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QListWidget" name="devList"/>
         </item>
        </layout>
       </widget>
      </item>
      <item>
       <widget class="QGroupBox" name="step2">
        <property name="minimumSize">
         <size>
          <width>250</width>
          <height>0</height>
         </size>
        </property>
        <property name="title">
         <string>Step 2: Select attribute</string>
        </property>
        <layout class="QVBoxLayout" name="verticalLayout_3">
         <item>
          <widget class="QLineEdit" name="attrFilterEdit">
           <property name="placeholderText">
            <string>filter</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QListWidget" name="attrList"/>
         </item>
        </layout>
       </widget>
      </item>
     </layout>
    </item>
    <item>
     <layout class="QHBoxLayout" name="horizontalLayout_7">
      <item>
       <layout class="QVBoxLayout" name="verticalLayout_5">
        <item>
         <widget class="QGroupBox" name="step3">
          <property name="title">
           <string>Step 3: Set range and delay</string>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout_4">
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_3">
             <item>
              <widget class="QLabel" name="fromLabel">
               <property name="text">
                <string>From:</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="fromSpin">
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="maximum">
                <double>999999999.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_4">
             <item>
              <widget class="QLabel" name="toLabel">
               <property name="text">
                <string>To:</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="toSpin">
               <property name="maximum">
                <double>999999999.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_5">
             <item>
              <widget class="QLabel" name="stepLabel">
               <property name="text">
                <string>Step:</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="stepSpin">
               <property name="maximum">
                <double>999999999.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_6">
             <item>
              <widget class="QLabel" name="delayLabel">
               <property name="text">
                <string>Delay:</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QSpinBox" name="delaySpin">
               <property name="maximum">
                <number>999999999</number>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="msLabel">
               <property name="maximumSize">
                <size>
                 <width>20</width>
                 <height>16777215</height>
                </size>
               </property>
               <property name="text">
                <string>ms</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <widget class="QPushButton" name="setValuesButton">
             <property name="text">
              <string>Set</string>
             </property>
             <property name="icon">
              <iconset theme="go-bottom">
               <normaloff/>
              </iconset>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QVBoxLayout" name="verticalLayout_7">
        <item>
         <widget class="QGroupBox" name="groupBox">
          <property name="title">
           <string>Step 4: Run</string>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout_6">
           <item>
            <widget class="QPushButton" name="runButton">
             <property name="enabled">
              <bool>false</bool>
             </property>
             <property name="text">
              <string>Run</string>
             </property>
             <property name="icon">
              <iconset theme="media-playback-start">
               <normaloff/>
              </iconset>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
        <item>
         <widget class="QGroupBox" name="devInfo">
          <property name="minimumSize">
           <size>
            <width>250</width>
            <height>0</height>
           </size>
          </property>
          <property name="maximumSize">
           <size>
            <width>16777215</width>
            <height>16777215</height>
           </size>
          </property>
          <property name="title">
           <string>Device Info</string>
          </property>
          <property name="flat">
           <bool>false</bool>
          </property>
          <property name="checkable">
           <bool>false</bool>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout">
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout">
             <item>
              <widget class="TaurusLed" name="devStateLed">
               <property name="minimumSize">
                <size>
                 <width>0</width>
                 <height>0</height>
                </size>
               </property>
               <property name="aspectRatioMode">
                <enum>Qt::KeepAspectRatio</enum>
               </property>
               <property name="ledStatus">
                <bool>true</bool>
               </property>
               <property name="ledInverted">
                <bool>false</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="devNameLabel">
               <property name="text">
                <string>---</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_2">
             <item>
              <widget class="QLabel" name="attrNameLabel">
               <property name="text">
                <string>---</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="TaurusLabel" name="attrValueLabel">
               <property name="maximumSize">
                <size>
                 <width>16777215</width>
                 <height>50</height>
                </size>
               </property>
               <property name="text">
                <string>---</string>
               </property>
               <property name="alignment">
                <set>Qt::AlignCenter</set>
               </property>
              </widget>
             </item>
             <item>
              <widget class="TaurusValueLineEdit" name="attrValueEdit">
               <property name="maximumSize">
                <size>
                 <width>100</width>
                 <height>16777215</height>
                </size>
               </property>
              </widget>
             </item>
            </layout>
           </item>
          </layout>
         </widget>
        </item>
       </layout>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
 </widget>
 <customwidgets>
  <customwidget>
   <class>TaurusLabel</class>
   <extends>QLabel</extends>
   <header>taurus.qt.qtgui.display</header>
  </customwidget>
  <customwidget>
   <class>TaurusValueLineEdit</class>
   <extends>QLineEdit</extends>
   <header>taurus.qt.qtgui.input</header>
  </customwidget>
  <customwidget>
   <class>TaurusLed</class>
   <extends>QLed</extends>
   <header>taurus.qt.qtgui.display</header>
  </customwidget>
  <customwidget>
   <class>QLed</class>
   <extends>QPixmapWidget</extends>
   <header>taurus.qt.qtgui.display</header>
  </customwidget>
  <customwidget>
   <class>QPixmapWidget</class>
   <extends>QWidget</extends>
   <header>taurus.qt.qtgui.display</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
""")

def error(parent, message):
	QtGui.QMessageBox.critical(parent, "Error", message)
	sys.exit(-1)

class QuckScanMain(QtGui.QMainWindow):
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		uic.loadUi(ui, self)
		self.setCentralWidget(self.centralwidget)

		# connect signals
		self.connect(self.devFilterEdit, QtCore.SIGNAL("textChanged(QString)"), self.filterDevices)
		self.connect(self.attrFilterEdit, QtCore.SIGNAL("textChanged(QString)"), self.filterAttrs)

		self.connect(self.setValuesButton, QtCore.SIGNAL("clicked()"), self.setRange)
		self.connect(self.runButton, QtCore.SIGNAL("clicked()"), self.run)

		self.connect(self.devList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.selectDevice)
		self.connect(self.attrList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.selectAttr)

		# load devices
		self.devices = []
		try:
			self.devices = taurus.Database().get_device_exported('*')
		except Exception as e:
			error(self, "Could not connect to Tango database:\n%s" % str(e))
		self.filterDevices(".*")

		# other data
		self.attributes = []
		self.range = None
		self.delay = 0
		self.selectedDev = None
		self.selectedAttr = None

		self.tryUnlockRun()

	def filterDevices(self, text):
		if not text:
			text = ".*"
		self.devList.clear()
		self.devList.addItems(filter(lambda s: re.search(str(text), s, re.I), self.devices))

	def filterAttrs(self, text):
		if not text:
			text = ".*"
		self.attrList.clear()
		self.attrList.addItems(filter(lambda s: re.search(str(text), s, re.I), self.attributes))

	def tryUnlockRun(self):
		if self.selectedDev is not None:
			if self.selectedAttr is not None:
				if self.range is not None:
					self.runButton.setEnabled(True)
					self.runButton.setText("Run")
					return
				else:
					self.runButton.setText("Select range and delay")
			else:
				self.runButton.setText("Select attribute")
		else:
			self.runButton.setText("Select device")
		self.runButton.setEnabled(False)

	def selectDevice(self, item):
		self.attributes = []
		self.attrList.clear()
		devName = str(item.text())
		self.devNameLabel.setText(devName)
		self.selectedDev = devName
		try:
			self.dev = PyTango.DeviceProxy(devName)
			self.devStateLed.setModel(devName + "/State")
		except Exception as e:
			error(self, "Can't connect to device %s:\n%s" % (devName, str(e)))
		self.attributes = self.dev.get_attribute_list()
		self.filterAttrs(".*")
		if self.selectedAttr in self.attributes:
			self.selectAttrByName(self.selectedAttr)
		else:
			self.selectedAttr = None
		self.tryUnlockRun()

	def selectAttr(self, item):
		attrName = str(item.text())
		self.selectAttrByName(attrName)
		self.tryUnlockRun()

	def selectAttrByName(self, name):
		self.attrNameLabel.setText(name)
		self.attrValueLabel.setModel(self.selectedDev + "/" + name)
		self.attrValueEdit.setModel(self.selectedDev + "/" + name)
		self.selectedAttr = name

	def setRange(self):
		fromValue = float(self.fromSpin.value())
		toValue = float(self.toSpin.value())
		stepValue = float(self.stepSpin.value())
		if fromValue > toValue:
			stepValue = -stepValue
		self.range = numpy.append(numpy.arange(fromValue, toValue, stepValue), toValue)
		self.delay = float(self.delaySpin.value())/1000
		self.tryUnlockRun()

	def run(self):
		for i in self.range:
			self.dev.write_attribute(str(self.selectedAttr), i)
			time.sleep(self.delay)


if __name__ == "__main__":
	from signal import signal, SIGINT, SIG_DFL
	from taurus.qt.qtgui.application import TaurusApplication

	signal(SIGINT, SIG_DFL)			# exit on Ctrl+C

	# start application
	Application = TaurusApplication(sys.argv)
	main = QuckScanMain()
	main.show()
	sys.exit(Application.exec_())
