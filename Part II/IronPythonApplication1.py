# -*- coding: utf-8 -*-
import sys,os
import clr

import sqlite3

sys.path.append(os.path.abspath('..'))

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System')
#clr.AddReferenceToFileAndPath('C:\Data\Daan\Daan.Instrument.Connector.dll')
clr.AddReferenceToFile('log4net.dll')
clr.AddReferenceToFile('Google.ProtocolBuffers.dll')
clr.AddReferenceToFile('Daan.Instrument.Log.dll')
clr.AddReferenceToFile('Daan.Instrument.Connector.dll')

from System.Windows.Forms import Application, Button, Form
from System.Drawing import Point
from System import *

from DBInterface import *

#from Google.ProtocolBuffers import *
#from Daan.Instrument.Log import *

from Daan.Instrument.Connector import *
from Daan.Instrument.Entity import *
from Daan.Instrument.Type import *
from Daan.Instrument.Connector.Common import *
'''
class InsConnector(object):
    @classmethod
    def SendHeart(cls):
        InsConnector.SendHeart(cls)

'''
x = 0
y = 0
form = Form()
form.Text = "Hello World"
button = Button(Text="Button Text")
form.Controls.Add(button)
def click(sender, event):
    global x,y
    button.Location = Point(x,y)
    # x += 5
    # y += 5
    try:
        #CommonConfig.load()
        
        #  insconnector = InsConnector()
        # heart.RunDate = DateTime.Parse("2016-03-08 08:11:12")
        print 'start testing'

        DBInterface.db_connect_initialize()

        heart = DBInterface.fetch_one_unsent_item_from_InsHeart()
        if heart:
            InsConnector.SendHeart(heart)
            DBInterface.set_insheart_as_sent(heart)

        DBInterface.db_disconnect()

        #Windows.Forms.MessageBox.Show(heart.TempIncubation)
    except Exception as ex:
        #Windows.Forms.MessageBox.Show(ex)
        print ex

button.Click += click
Application.Run(form)
