import pymysql
from pages import table
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
import datetime
from datetime import timedelta

id = 0
date = ""

def formatDate(date):
    print(date)
    allDateData = list(reversed(date.split(":")))
    dt = (str(allDateData[0]) +"-"+ str(allDateData[1]).zfill(2) +"-"+ str(allDateData[2]))
    return dt

def formatTime(td):
    seconds = td.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return ('{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))

def calActualWorkingHours(date, Details):
    #global date
    year, month, day = int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])

    process = []
    process_times = dict()
    for pro in Details:
        winTime = datetime.timedelta(hours=0, minutes=0, seconds=0)
        process_times[pro] = []
        for win in Details[pro]:
            winTime += (datetime.datetime.strptime(win[1], '%H:%M:%S.%f') - datetime.datetime(year, month, day, hour=0, minute=0, second=0))
        process_times[pro] = formatTime(winTime)

    #infoPopup.Details = process_times
    return process_times

def calTotalWorkingHours(date, dets):
    #global date
    year, month, day = int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])
    total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for pro in dets:
        for win in dets[pro]:
            total_time += (datetime.datetime.strptime(win[1], '%H:%M:%S.%f') - datetime.datetime(year, month, day, hour=0, minute=0, second=0))

    total_time = formatTime(total_time)
    return total_time

def getUserInfo(id, date):
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    #global id, date
    formattedDate = formatDate(date)
    #print(formattedDate)
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    #window_name, process_id, total_time
    cur.execute("SELECT DISTINCT(process_name) FROM %s.`%d` WHERE date = '%s'" %(db_name, id, formattedDate))

    """Details={'window_name':[],
             'process_name':[],
             'process_id':[],
             'date':[],
             'total_time':[]}"""

    processes = []
    Details = dict()
    cur1 = db.cursor()

    for data in cur.fetchall():
        processes.append(data[0])
        Details[data[0]] = []
        cur1.execute("SELECT window_name, total_time FROM %s.`%d` WHERE date = '%s' AND process_name = '%s'"%(db_name, id, formattedDate, data[0]))
        #print(data[0])

        for Data in cur1.fetchall():
            Details[data[0]].append([Data[0], Data[1]])

    #Details['process_name'].append(data[1])
    #Details['window_name'].append(data[0])
    #Details['process_id'].append(data[2])
    #Details['date'].append(data[3])
    #Details['total_time'].append(data[4])
    #table.io.append(data[0])
    #table.time.append(data[1])
    #table.door.append(data[3])
    #table.accType.append(data[4])

    table.Details = Details
    table.id = id
    table.date = formatDate(date)

    year, month, day = int(formattedDate.split("-")[0]), int(formattedDate.split("-")[1]), int(formattedDate.split("-")[2])
    totalWorkingHours = (datetime.datetime.strptime(calTotalWorkingHours(formattedDate, Details), '%H:%M:%S') - datetime.datetime(year, month, day, hour=0, minute=0, second=0))

    sumTime = calActualWorkingHours(formattedDate, Details)

    NonWrkHours = StdWrkHrs - totalWorkingHours
    AdditionalHours = totalWorkingHours - StdWrkHrs

    """infoPopup.TWH.append(totalWorkingHours)
    infoPopup.AWH.append(sumTime)
    if totalWorkingHours < StdWrkHrs:
        infoPopup.NCH.append(NonWrkHours)
        infoPopup.ACH.append(datetime.timedelta())
    else:
        infoPopup.NCH.append(datetime.timedelta())
        infoPopup.ACH.append(AdditionalHours)"""

    cur.close()
    db.close()
    return sumTime

def openPopup(ua, id, date):
    #global id, date

    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    cur.execute("SELECT Name FROM %s.user_master WHERE ID = '%d'"%(db_name, id))
    name = cur.fetchone()

    if ua == 'user':
        tab = infoPopup.InfoTab(name, date)
    elif ua == 'admin':
        tab = infoPopup.InfoTabAdmin(name, id, date)

    popup = ModalView(size_hint=(0.85, 0.85))
    popup.add_widget(tab)
    #title="{}||{}".format(name[0], formatDate(date[len(date)-1])), content=tab,
    popup.open()
    popUpCLoseBtn.bind(on_press=popup.dismiss)
