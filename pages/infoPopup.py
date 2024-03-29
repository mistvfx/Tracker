from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.clock import Clock
import threading
from kivy.properties import *
import datetime
from functools import partial

from pages import table
from db import getInfo

closeBtn = Button()
TWH = [0]*1
AWH = [0]*1
NCH = [0]*1
ACH = [0]*1
Details = dict()

Builder.load_string("""
<hdrLayout>:
    orientation: 'horizontal'
    size_hint: (1, 0.10)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<tblLayout>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<infoLbl>:
    color: (0, 0, 0, 1)
    bold: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<infoTabAdmin>:
    FloatLayout:
        Label:
            id: userinfo
            pos_hint: {'center_x':0.5, 'center_y':0.5}

<infoTab>:
    BoxLayout:
        orientation: 'vertical'
        FloatLayout:
            pos: self.pos
            size: self.size
            size_hint_y: 0.06
            Label:
                id: userinfo
                font_name: 'fonts/GoogleSans-Bold.ttf'
                pos_hint: {'center_x':0.5, 'center_y':0.5}
        HdrLayout:
            GridLayout:
                cols:3
                size_hint: (0.65, 1)
                Label:
                    text: 'I/O'
                    bold: True
                Label:
                    text: 'TIME'
                    bold: True
                Label:
                    text: 'DOOR'
                    bold: True
        TblLayout:
            id: table_layout

<AppBtn@Button>:
    background_color: (1, 1, 1, 0)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    color: (0, 0, 0, 1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<InfoTabAdmin>:
    BoxLayout:
        orientation: 'horizontal'
        RecycleView:
            data: root.details
            viewclass: 'AppBtn'
            RecycleBoxLayout:
                size_hint: (1,None)
                height: self.minimum_height
                spacing: 2
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: (0, 0, 0, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
""")

class HdrLayout(BoxLayout):
    pass

class TblLayout(BoxLayout):
    pass

class InfoLbl(Label):
    pass

def formatTime(time):
    seconds = time.total_seconds()
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    return ('{}:{}'.format(hours, minutes))

class InfoTab(BoxLayout):
    def __init__(self, name, date):
        super(InfoTab, self).__init__()
        self.ids.userinfo.text = '{}|{}'.format(name[0], date[len(date)-1])
        self.popUI()

    def popUI(self):
        #overallLayout = BoxLayout(orientation='vertical')
        #self.add_widget(overallLayout)

        """ Defining Header and closeBtn """

        #headerLayout = hdrLayout()
        #overallLayout.add_widget(headerLayout)

        #header = GridLayout(cols=3, size_hint=(0.65, 1))
        #headerLayout.add_widget(header)
        #headers = ['I/O', 'TIME', 'DOOR']
        #for i in range(3):
            #headerLabel = Label(text=headers[i], bold=True)
            #header.add_widget(headerLabel)

        #global closeBtn
        #headerLayout.add_widget(closeBtn)

        """ Table and info """

        #tableLayout = tblLayout()
        #overallLayout.add_widget(tableLayout)

        tab = table.dataTable()
        tab.size_hint=(0.65, 1)
        self.ids.table_layout.add_widget(tab)

        """ Defining Info """

        info = GridLayout(cols=2, size_hint=(0.35, 1))
        self.ids.table_layout.add_widget(info)

        global TWH, AWH, NCH, ACH

        #tw = ("%.2f"%(round(TWH[len(TWH)-1].total_seconds()/3600, 2)))
        tw = formatTime(TWH[len(TWH)-1])

        #aw = ("%.2f"%(round(AWH[len(AWH)-1].total_seconds()/3600, 2)))
        aw = formatTime(AWH[len(AWH)-1])

        #nc = ("%.2f"%(round(NCH[len(NCH)-1].total_seconds()/3600, 2)))
        nc = formatTime(NCH[len(NCH)-1])

        #ac = ("%.2f"%(round(ACH[len(ACH)-1].total_seconds()/3600, 2)))
        ac = formatTime(ACH[len(ACH)-1])

        infoQ = ['Total Hours :', tw, 'Working Hours :', aw, 'Non-Completed Actual Hours:', nc, 'Additional Hours:', ac]

        for i in range(len(infoQ)):
            infoLabels = InfoLbl(text=infoQ[i])
            if i % 2 == 1:
                infoLabels.size_hint_x= 0.30
            info.add_widget(infoLabels)

class InfoTabAdmin(BoxLayout):
    details = ListProperty(None)
    def __init__(self, id, date):
        super(InfoTabAdmin, self).__init__()
        if (datetime.datetime.strftime(datetime.datetime.now(), "%d:%m:%Y")) == date:
            self.t1 = threading.Thread(target=self.startClock(id, date))
            self.t1.start()
            self.t2 = threading.Thread(target=self.openPopup())
            self.t2.start()
        else:
            self.getData(id, date)
            self.openPopup()

    def startClock(self, id, date):
        self.dets = Clock.schedule_interval(lambda dt: self.getData(id, date), 0.5)

    def stopClock(self, *args):
        print("ok")
        try:
            self.t1.join(); self.t2.join()
            Clock.unschedule(self.dets)
        except:
            pass

    def openPopup(self):
        popup = ModalView(size_hint=(0.85, 0.85))
        popup.add_widget(self)
        popup.bind(on_dismiss=self.stopClock)
        popup.open()

    def getData(self, id, date):
        Details = getInfo.getUserInfo(int(id), date)
        self.details = [{'text': "{} | {}".format(det, Details[det]), 'size_hint':(1,None)} for det in Details]
