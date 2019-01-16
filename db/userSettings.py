import pymysql
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.properties import *
import re

from pages import Dialog, infoPopup
from pages.specialFeatures import MouseOver

Data = 0

Builder.load_string("""
<Lbl>:
    font_name: 'fonts/GoogleSans-Bold.ttf'
    size_hint_x: 0.22
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    halign: "center"
    valign: "middle"
    color: (0, 0, 0, 1)
    pos_hint: {'center_y':0.82, 'center_x':0.25}
    canvas.before:
        Color:
            rgba: (1, 1, 1, 0)
        Rectangle:
            size: self.size
            pos: self.pos

<In>:
    font_name: 'fonts/GoogleSans-Regular.ttf'
    multiline: False
    write_tab: False
    background_color: (1, 1, 1, 0)
    size_hint: (0.75, 0.75)
    pos_hint: {'top':0.8, 'center_x':0.5}
    on_text: root.update_padding()
    padding_x: (self.width - self.text_width) / 2
    padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    canvas.before:
        Color:
            rgba: (0.5, 0, 1, 0.85)
        Line:
            width: 2
            rectangle: (self.x, self.y, self.width, self.height)

<MaterialTextBox>:
    size_hint_y: 1

<Btn>:
    font_name: 'fonts/GoogleSans-Medium.ttf'
    size_hint: (0.25, 1)
    background_color: (1, 1, 1, 0)
    color: (0, 0, 0, 1)

<UserSettingPop>:
    size_hint: (0.5, 0.55)

    SettingsTabs:
        do_default_tab: False

<UserInfoTab>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.25
        MaterialTextBox:
            In:
                id: userid
                text: root.user_id
            Lbl:
                text: "Artist ID"
        MaterialTextBox:
            In:
                id: userip
                text: root.user_ip
            Lbl:
                text: "Machine IP"
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.25
        MaterialTextBox:
            In:
                id: username
                text: root.user_name
            Lbl:
                text: "Name"
        MaterialTextBox:
            In:
                id: userdept
                text: root.user_dept
            Lbl:
                text: "Dept"
    FloatLayout:
        size_hint_y: 0.05
        BoxLayout:
            orientation: 'horizontal'
            size_hint_x: 0.4
            pos_hint: {'center_y':0.5, 'right':1}
            Btn:
                text: 'Save'
                on_release: root.save_user_details()
            Btn:
                text: 'Deploy'
                on_release: root.deploy_tracking()
            Btn:
                text: 'Cancel'
                on_release: root.dismiss_popup()


<SettingsTabs>:
    TabbedPanelItem:
        text: 'User-Info'
        font_name: 'fonts/moon-bold.otf'
        UserInfoTab:
""")
class MaterialTextBox(FloatLayout):
    pass

class In(TextInput):
    text_width = NumericProperty()

    def update_padding(self, *args):
        self.text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )

class Lbl(Label):
    pass

class Btn(Button, MouseOver):
    def on_hover(self):
        self.color = (1, 1, 1, 1)
        with self.canvas.before:
                Color(117/255, 117/255, 225/255, 1)
                Rectangle(pos= self.pos, size= self.size)

    def on_exit(self):
        self.color = (0, 0, 0, 1)
        with self.canvas.before:
                Color(1, 1, 1, 1)
                Rectangle(pos= self.pos, size= self.size)

class UserSettingPop(ModalView):
    def __init__(self, artistID):
        super(UserSettingPop, self).__init__()
        pass

class SettingsTabs(TabbedPanel):
    pass

class UserInfoTab(BoxLayout):
    user_id = StringProperty(None)
    user_ip = StringProperty(None)
    user_name = StringProperty(None)
    user_dept = StringProperty(None)
    def __init__(self, **args):
        super(UserInfoTab, self).__init__(**args)
        global Data
        self.user_id = str(Data[0])
        self.user_ip = Data[1]
        self.user_name = Data[2]
        self.user_dept = Data[3]

    def save_user_details(self):
        try:
            db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
            db_name = "tracker"
        except:
            db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
            db_name = "MMT"
        cur = db.cursor()
        cur.execute("UPDATE %s.user_master SET ID = '%s', IP = '%s', Name = '%s', Department = '%s' WHERE ID = '%s'"%(db_name, self.ids.userid.text, self.ids.userip.text, self.ids.username.text, self.ids.userdept.text, Data[0]))
        cur.execute("CREATE TABLE IF NOT EXISTS `%s`.`%s` (`S.No` INT NOT NULL AUTO_INCREMENT, `window_name` VARCHAR(225) NULL, `process_name` VARCHAR(225) NULL, `process_id` INT NULL, `date` DATE NULL, `total_time` VARCHAR(45) NULL, PRIMARY KEY (`S.No`));"%(db_name, self.ids.userid.text))

    def deploy_tracking(self):
        pass

    def dismiss_popup(self):
        pass

def fetch_data(id):
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    cur.execute("SELECT ID, IP, Name, Department FROM %s.user_master WHERE ID = '%s' "%(db_name, id))
    global Data
    pre_data = []
    for data in cur.fetchone():
        pre_data.append(data)
    Data = pre_data
