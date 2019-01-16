import pymysql
from socket import *

def check_available_ips():
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()
    ips = []
    cur.execute("SELECT IP FROM %s.`user_master` WHERE ID != 1000"%(db_name))
    for data in cur.fetchall():
        ips.append(data[0])
    cur.close()
    db.close()
    print(ips)
    return ips

def is_up(addr):
    print(addr)
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)
    if not s.connect_ex((addr,135)):
        s.close()
        return 1
    else:
        s.close()

def scan_all_ip():
    try:
        db = pymysql.connect("192.168.1.224", "root", "user@123", "tracker", autocommit=True)
        db_name = "tracker"
    except:
        db = pymysql.connect("192.168.1.181", "mmt", "py@123", "MMT", autocommit=True)
        db_name = "MMT"
    cur = db.cursor()

    avail_ips = check_available_ips()

    new = 0

    #network = '10.10.5.' #need to change
    network = '192.168.1.' #need to change

    #search for ips and ping them
    for ip in range(1,256):
        addr = network + str(ip)
        if is_up(addr):
            print('%s \t- %s' %(addr, getfqdn(addr)))
            if addr in avail_ips:
                print('%s \t- %s [ALREADY AVAILABLE]' %(addr, getfqdn(addr)))
                continue
            else:
                cur.execute("INSERT INTO %s.`user_master` (ID, IP, Name, Department, Password) VALUES('%s', '%s', '%s', 'ARTIST', '%s')"%(db_name, addr.split(".")[-1], addr, getfqdn(addr), addr.split(".")[-1]))
                new += 1

    if new != 0:
        return 1
    else:
        return 0
