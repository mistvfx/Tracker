import pymysql
from db import getInfo, calcWrkHrs, monthlyWrkHours

def checkCredentials(username, password):
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"

    cur = db.cursor()
    try:
        cur.execute("SELECT ID, Name, Department, Password FROM {}.user_master WHERE Status = 'OPEN'".format(db_name))
    except:
        cur.execute("CREATE TABLE IF NOT EXISTS `{}`.`user_master` (`ID` INT NOT NULL, `IP` VARCHAR(45) NOT NULL, `Name` VARCHAR(45) NOT NULL, `Department` VARCHAR(45) NOT NULL, `Password` VARCHAR(45) NOT NULL, `Status` VARCHAR(45) NOT NULL DEFAULT 'OPEN', `email` VARCHAR(45) NULL, `LR` VARCHAR(45) NOT NULL DEFAULT 0, PRIMARY KEY (`ID`));".format(db.db_name))
        cur1 = db.cursor()
        cur1.execute("INSERT INTO {}.`user_master` (ID, IP, Name, Department, Password, LR) VALUES('1000', '192.168.1.224', 'ADMIN', 'ADMIN', '0')".format(db_name))
        cur.execute("SELECT ID, Name, Department, Password FROM {}.user_master WHERE Status = 'OPEN' ".format(db_name))
    finally:
        pass


    for data in cur.fetchall():
        if username == "" or password == "":
            return 0
        if username in str(data[0]) and password in str(data[3]):
            if str(data[2]) == 'ADMIN':
                cur.close()
                db.close()
                return 1
            elif str(data[2]) != 'ADMIN':
                from pages import userPage
                userPage.id = (data[0])
                userPage.user = (str(data[1]))
                userPage.department = (str(data[2]))
                getInfo.id.append(int(data[0]))
                calcWrkHrs.id.append(int(data[0]))
                calcWrkHrs.getUserTime()
                monthlyWrkHours.id.append(int(data[0]))
                cur.close()
                db.close()
                return 2

    cur.close()
    db.close()
    return 0
