import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from KivyCalendar import DatePicker
from kivy.uix.spinner import Spinner
from kivy.uix.carousel import Carousel
from kivy.lang import Builder

from pages import Dialog

Builder.load_string("""
<DBtabs>:
    do_default_tab: False

    TabbedPanelItem:
        text: 'DELETE'
        font_name: 'fonts/moon-bold.otf'
        FloatLayout:
            pos: self.pos
            size: self.size
            Carousel:
                id: car
                pos_hint: {'x':0, 'y':0}
                size_hint_y: 1
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 0)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                loop: True
                direction: 'right'
                DeleteDataDay:
                DeleteDataMonth:

            Button:
                text: '>'
                size_hint: (0.1, 0.1)
                pos_hint: {'top': 1, 'right':1}

""")

def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class DBtabs(TabbedPanel):
    pass

class DeleteDataDay(BoxLayout):
    def __init__(self, **args):
        super(DeleteDataDay, self).__init__(**args)
        self.orientation = "vertical"
        self.size_hint_y = 1

        def callback(instance):
            if instance.text == 'DELETE ALL DATA':
                self.deleteAllData(formatDate(date.text))

        dayLbl = Label(text="DAY", bold=True, size_hint_y=0.1)
        self.add_widget(dayLbl)

        date = DatePicker(size_hint_y=0.20, pHint=(0.35, 0.35), size_hint_x=0.60)
        self.add_widget(date)

        delBtn = Button(text='DELETE ALL DATA', size_hint=(0.60, 0.20))
        delBtn.bind(on_release = callback)
        self.add_widget(delBtn)

    def deleteAllData(self, delDate):
        db = pymysql.connect("192.168.1.224", "root", "user@123", "essl", autocommit=True)
        cur = db.cursor()
        cur1 = db.cursor()

        cur.execute("SELECT ID FROM essl.user_master WHERE Status = 'OPEN'")
        for id in cur.fetchall():
            if id[0] == 1000:
                continue
            cur1.execute("DELETE FROM essl.%d WHERE MDATE = '%s'"%(id[0], delDate))

        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        pop = Dialog.dialog("DELETED SUCCESSFULLY!!!", "All data for the selected date has been deleted successfully !!", closePopBtn)
        pop.open()

class DeleteDataMonth(BoxLayout):
    def __init__(self, **args):
        super(DeleteDataMonth, self).__init__(**args)
        self.orientation = "vertical"
        self.size_hint_y = 1

        def callback(instance):
            if instance.text == 'DELETE ALL DATA':
                self.deleteAllData(month.text, year.text)

        monthLbl = Label(text="MONTH", bold=True, size_hint_y=0.1)
        self.add_widget(monthLbl)

        month = Spinner(text='Month', values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        self.add_widget(month)

        year = TextInput(hint_text='YYYY')
        self.add_widget(year)

        delBtn = Button(text='DELETE ALL DATA', size_hint=(0.60, 0.20))
        delBtn.bind(on_release = callback)
        self.add_widget(delBtn)

    def deleteAllData(self, month, year):
        db = pymysql.connect("192.168.1.224", "root", "user@123", "essl", autocommit=True)
        cur = db.cursor()
        cur1 = db.cursor()

        cur.execute("SELECT ID FROM essl.user_master WHERE Status = 'OPEN'")
        for id in cur.fetchall():
            if id[0] == 1000:
                continue
            cur1.execute("DELETE FROM essl.%d WHERE YEAR(MDATE) = '%s' AND MONTH(MDATE) = '%s'"%(id[0], year, month))

        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        pop = Dialog.dialog("DELETED SUCCESSFULLY!!!", "All data for the %s-%s has been deleted successfully !!"%(month, year), closePopBtn)
        pop.open()

def setup():
    popup = Popup(title='Database Edits', content=DBtabs(), size_hint=(0.75, 0.75))
    popup.open()
