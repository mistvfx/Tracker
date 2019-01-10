import pymysql
from pages import table, infoPopup
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
import datetime

id = [0]*1
date = [None]*1

def formatDate(date):
    allDateData = list(reversed(date))
    dt = (str(allDateData[0])+"-"+str(allDateData[1])+"-"+str(allDateData[2]))
    return dt

"""class getUserInfo(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        self.login()"""

def calActualWorkingHours(Details):
    process = []
    process_times = {}
    for pro in Details['process_name']:
        if pro not in process:
            process.append(Details['process_name'])
    for i in range(len(Details['process_name'])):
        process_times['{}'.format(Details['process_name'][i])].append(Details['total_time'][i])

    print(process_times)
    return process_times

def calTotalWorkingHours(times):
    total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for i in range(len(times)):
        total_time += datetime.datetime.strptime(times[i], '%H:%M:%S.%f').strftime("%H:%M:%S")
    return total_time

def getUserInfo():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    global id, date
    formattedDate = formatDate(date[int(len(date)-1)])
    #print(formattedDate)
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    cur.execute("SELECT window_name, process_name, process_id, date, total_time FROM %s.`%d` WHERE date = '%s'" %(db_name, id[int(len(id)-1)], formattedDate))

    Details={'window_name':[],
             'process_name':[],
             'process_id':[],
             'date':[],
             'total_time':[]}

    for data in cur.fetchall():
        Details['window_name'].append(data[0])
        Details['process_name'].append(data[1])
        Details['process_id'].append(data[2])
        Details['date'].append(data[3])
        Details['total_time'].append(data[4])
        #table.io.append(data[0])
        #table.time.append(data[1])
        #table.door.append(data[3])
        #table.accType.append(data[4])

    table.Details = Details
    table.id = id
    table.date = formatDate(date[len(date)-1])

    totalWorkingHours = calTotalWorkingHours(Details['total_time'])

    sumTime = calActualWorkingHours(Details)

    NonWrkHours = StdWrkHrs - sumTime
    AdditionalHours = sumTime - StdWrkHrs

    infoPopup.TWH.append(totalWorkingHours)
    infoPopup.AWH.append(sumTime)
    if sumTime < StdWrkHrs:
        infoPopup.NCH.append(NonWrkHours)
        infoPopup.ACH.append(datetime.timedelta())
    else:
        infoPopup.NCH.append(datetime.timedelta())
        infoPopup.ACH.append(AdditionalHours)

    cur.close()
    db.close()

def openPopup(ua):
    popUpCLoseBtn = Button(text='close', size_hint=(0.45, 1))
    infoPopup.closeBtn = popUpCLoseBtn
    global id, date

    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    cur.execute("SELECT Name FROM %s.user_master WHERE ID = '%d'"%(db_name, id[len(id)-1]))
    name = cur.fetchone()

    getUserInfo()

    if ua == 'user':
        tab = infoPopup.InfoTab(name, date)
    elif ua == 'admin':
        tab = infoPopup.InfoTabAdmin(name, date)

    popup = ModalView(size_hint=(0.85, 0.85))
    popup.add_widget(tab)
    #title="{}||{}".format(name[0], formatDate(date[len(date)-1])), content=tab,
    popup.open()
    popUpCLoseBtn.bind(on_press=popup.dismiss)
