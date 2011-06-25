#!/usr/bin/python3
# -*- coding: UTF-8 -*-

###
# Created  :Wed Jun 22 08:48:16 UTC 2011
# Modified :
###

import re
import os
import sys

class ASSToSRTTool:
  '''
  This is a tool can convert subtitle file ass format to srt format.
  Showing format:
  ass:Dialogue: 0,0:00:03.32,0:00:05.70,*Default,NTP,0000,0000,0000,,这个世界存在于立方体的箱子中
  step 1: find all line startswith 'Dialogue'
          dialogues = re.findall('^Dialogue:.+', lines)
  step 2: split them by ','
          tmps = [e.split(',') for e in dialogues]
  step 3: Extra start time , end time and dialogue content
          [(e[1], e[2], ''.join(e[9:]) for e in tmps]
  '''
  DIALOGUE_PATTERN = r'Dialogue:.+'
  def __init__(self):
    pass

  def readASSFile(self, filepath):
    noBlank = lambda x : len(''.join(x[9:])) > 0
    with open(filepath) as assfile:
      fileContents = assfile.read()
      p = ASSToSRTTool.DIALOGUE_PATTERN
      dialogues = re.findall(p, fileContents)
      tmps = [e.split(',') for e in dialogues]
      tmpData = [self.generateSRTData(e) for e in tmps if noBlank(e)]
      self.srtData = SRTData(tmpData)

  def formatTime(self, time):
    '''
    convert time like "0:17:40.13" to "00:17:40,13"
    '''
    time = '0' + time + '0'
    return time.replace('.', ',')

  def generateSRTData(self, assElement):
    sTime = self.formatTime(assElement[1])
    eTime = self.formatTime(assElement[2])
    content = ' '.join(assElement[9:])
    return SRTElement(sTime, eTime, content)


class SRTElement:
  def __init__(self, sTime, eTime, content, index = 0):
    self.sTime = sTime
    self.eTime = eTime
    self.content = re.sub(r'\{.+\}', '', content)
    self.index = index

  def __str__(self):
    return '\n{}\n{} --> {}\n{}\n'.format(self.index, self.sTime, self.eTime, self.content)

class SRTData:
  def __init__(self, srtElements):
    self.data = srtElements

  def resort(self):
    self.data.sort(key=lambda x:x.sTime)
    for i in range(0,len(self.data)):
      self.data[i].index = i + 1

if __name__ == '__main__':
  filePath = sys.argv[1]
  a2s = ASSToSRTTool()
  a2s.readASSFile(filePath)
  a2s.srtData.resort()

  with open(filePath[:-3]+'srt', 'w') as srt:
    for data in a2s.srtData.data:
      srt.write(data.__str__())
