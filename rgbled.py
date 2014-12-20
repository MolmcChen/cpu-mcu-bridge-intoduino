################################################################################
## @file    : rgbled.py
## @author  : Haoyao Chen
## @version : V1.0.0
## @date    : 10-12-2014
## @brief   : RGB led settings
 
##  Copyright (c) 2013-2014 Intoduino Team.  All right reserved.
##
##  This library is free software; you can redistribute it and/or
##  modify it under the terms of the GNU Lesser General Public
##  License as published by the Free Software Foundation, either
##  version 3 of the License, or (at your option) any later version.
##
##  This library is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  Lesser General Public License for more details.

##  You should have received a copy of the GNU Lesser General Public
##  License along with this library; if not, see <http://www.gnu.org/licenses/>.
#################################################################################
import os, tty, termios, select
from contextlib import contextmanager
from sys import stdin, stdout
from subprocess import call

class RGBLED_Command:
  def __init__(self, cp):
    self.processor = cp
    self.pwm_eriod = 10000000   #unit: ns
    self.red   = 255
    self.green = 255
    self.blue  = 255
    self.period  = 400000                   #unit: us. blink or breath period		
    self.count   = 10000
    self.pwm_duty_red   = self.period - 1
    self.pwm_duty_green = self.period - 1
    self.pwm_duty_blue  = self.period - 1  #DO NOT directly set the duty = period

  def setColor(self, data):
    if data[0]>255 or data[0]<0:
      return 0
    self.red   = data[0]
    if data[1]>255 or data[1]<0:
      return 0
    self.green = data[1]
    if data[2]>255 or data[2]<0:
      return 0
    self.blue  = data[2]
    
    #calculate the duty
    self.duty_red = calDuty(self.red)
    self.duty_green = calDuty(self.green)
    self.duty_blue = calDuty(self.blue)
    call(['/usr/bin/set_led_color', str(self.duty_red), str(self.duty_green), str(self.duty_blue)])
		
  def setBlink(self, period, count):  #data: the period of blink. Default: 400ms
    if period != '':
      self.period = period
    if count != '':
      self.count = count
    call(['/usr/bin/set_led_blink', str(self.duty_red), str(self.duty_green), str(self.duty_blue)], str(self.period), str(self.count))

  def setBreath(self, period, count): #data: the period of breath. Default: 60ms
    if period != '':
      self.period = period
    if count != '':
      self.count = count
    call(['/usr/bin/set_led_breath', str(self.duty_red), str(self.duty_green), str(self.duty_blue)], str(self.period), str(self.count))   
    
		
  def calDuty(self, brightness):  #calculate the duty given the brightness
    return brightness/256*self.period
	
    


