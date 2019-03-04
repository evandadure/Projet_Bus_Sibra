#!/usr/bin/python3
#-*-coding:utf-8-*-
from datetime import datetime,timedelta


def get_content(data_file_name):
    try:
        with open(data_file_name, 'r') as f:
            content = f.read()      
        return content
    except OSError:
        # 'File not found' error message.
        print("File not found")

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    #print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def line_infos(content):
    slited_content = content.split("\n\n")
    infos_dic={}
    infos_dic["regular_path"] = slited_content[0]
    infos_dic["regular_date_go"] = dates2dic(slited_content[1])
    infos_dic["regular_date_back"] = dates2dic(slited_content[2])
    infos_dic["we_holidays_path"] = slited_content[3]
    infos_dic["we_holidays_date_go"] = dates2dic(slited_content[4])
    infos_dic["we_holidays_date_back"] = dates2dic(slited_content[5])
    return infos_dic

def setDateTime(date,heure):
    #print("date",date,"heure",heure)
    d = datetime.strptime(date,"%d/%m/%y")
    h = heure[:heure.find(":")]
    m = heure[heure.find(":")+1:]
    d = d.replace(hour=int(h),minute=int(m))
    return d

def getTimeDelta(heure1,heure2):
    delta = setDateTime("01/01/70",heure1)-setDateTime("01/01/70",heure2)
    return int(delta.total_seconds()/60)
#    m = delta[delta.find(":")+1:delta.find(":",delta.find(":")+1)]
#    return int(m)

def getHeure(date):
    return str(date.time())[0:5]

def addMinuteToTime(time,minutes):
    date = setDateTime("01/01/70",time)
    date+=timedelta(minutes=minutes)
    return getHeure(date)
    
def isSemaine(date):
    if(date.isoweekday() == 6):
        return "V"
    else:
        return "S"





# date = ["20/02/19", "07:44"]
# date = setDateTime(date[0],date[1])
# print(date)
# b = date + timedelta(minutes=3)
# print(b)

#dateNow = datetime.now()
#dateThen = setDateTime("13/02/19","10:41")
#print(getTimeDelta(dateNow,dateThen))

    


