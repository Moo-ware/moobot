import datetime
import json
import requests
from pytz import timezone


eLevel = {
  0  : "",
  1  : "PRI",
  2  : "DUO",
  3  : "TRI",
  4  : "TET",
  5  : "PEN",
  20 : "PEN",
}

spawnTimes = {
    'Monday' : {
        '0015' : 'Kutum & Karanda',
        '0200' : 'Karanda',
        '0500' : 'Kzarka',
        '0900' : 'Kzarka',
        '1200' : 'Offin	',
        '1600' : 'Kutum	',
        '1900' : 'Nouver',
        '2215' : 'Kzarka'
    },
    'Tuesday' : {
        '0015' : 'Karanda',
        '0200' : 'Kutum',
        '0500' : 'Kzarka',
        '0900' : 'Nouver',
        '1200' : 'Kutum',
        '1600' : 'Nouver',
        '1900' : 'Karanda',
        '2215' : 'Garmoth'
    },
    'Wednesday' : {
        '0015' : 'Kutum & Kzarka',
        '0200' : 'Karanda',
        '0900' : 'Karanda',
        '1200' : 'Nouver',
        '1600' : 'Kutum & Offin',
        '1900' : 'Vell',
        '2215' : 'Karanda & Kzarka',
        '2315' : 'Quint & Muraka'
    },
    'Thursday' : {
        '0015' : 'Nouver',
        '0200' : 'Kutum',
        '0500' : 'Kzarka',
        '0900' : 'Kutum',
        '1200' : 'Nouver',
        '1600' : 'Kzarka',
        '1900' : 'Kutum',
        '2215' : 'Garmoth'
    },
    'Friday' : {
        '0015' : 'Kzarka & Karanda',
        '0200' : 'Nouver',
        '0500' : 'Karanda',
        '0900' : 'Kutum',
        '1200' : 'Karanda',
        '1600' : 'Nouver',
        '1900' : 'Kzarka',
        '2215' : 'Kutum & Kzarka'
    },
    'Saturday' : {
        '0015' : 'Karanda',
        '0200' : 'Offin',
        '0500' : 'Nouver',
        '0900' : 'Kutum',
        '1200' : 'Nouver',
        '1600' : 'Quint & Muraka',
        '1900' : 'Kzarka & Karanda'
    },
    'Sunday' : {
        '0015' : 'Nouver & Kutum',
        '0200' : 'Kzarka',
        '0500' : 'Kutum',
        '0900' : 'Nouver',
        '1200' : 'Kzarka',
        '1600' : 'Vell',
        '1900' : 'Garmoth',
        '2215' : 'Kzarka & Nouver'
    },
}

dayOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def spawnFromNow():
    spawnList = []
    eastern = timezone('US/Eastern')
    day = datetime.datetime.now(eastern).strftime('%H%M-%A').split('-')
    for i in spawnTimes[day[1]]:
        if int(noOctal(i)) > int(noOctal(day[0])):
            time = [int(noOctal(i[0:2])) - int(noOctal(day[0][0:2])), int(noOctal(i[2:])) - int(noOctal(day[0][2:]))]
            timefromnow = str(datetime.timedelta(minutes=(time[0] * 60 + time[1] - 1)))[:-3]
            spawnList.append([timefromnow, spawnTimes[day[1]][i]])
        
        elif int(noOctal(i)) == int(noOctal(day[0])) or (int(noOctal(day[0])) - int(noOctal(i))) <= 4 :
            spawnList.append(['SPAWNED', spawnTimes[day[1]][i]])
    
    if len(spawnList) < 3:
        nextDay = day
        if nextDay[1] == 'Sunday':
            nextDay[1] = 'Monday'
        else:
            nextDay[1] = dayOfWeek[dayOfWeek.index(day[1]) + 1]
        for i in spawnTimes[nextDay[1]]:
            time = [int(noOctal(i[0:2])) - int(noOctal(nextDay[0][0:2])), int(noOctal(i[2:])) - int(noOctal(nextDay[0][2:]))]
            timefromnow = str(datetime.timedelta(minutes=(time[0] * 60 + time[1] - 1)))[:-3]
            spawnList.append([timefromnow, spawnTimes[nextDay[1]][i], 1])
        return spawnList
    else:
        return spawnList
  
def specialSpawns():
    specialSpawnList = []


def GetWaitlist():
    url = 'https://na-trade.naeu.playblackdesert.com/Home/GetWorldMarketWaitList'
    headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
    }
    payload = {}

    response = requests.request('POST', url, json=payload, headers=headers)
    
    x = json.loads(response.text)
    return x

def GetWaitlistEU():
    url = 'https://eu-trade.naeu.playblackdesert.com/Home/GetWorldMarketWaitList'
    headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
    }
    payload = {}

    response = requests.request('POST', url, json=payload, headers=headers)
    
    x = json.loads(response.text)
    return x

def matchEnhancement(key):
    return eLevel.get(key)


def timeCalc(timestamp):
    td = datetime.datetime.fromtimestamp(timestamp / 1e3) - datetime.datetime.now()
    return int(round(td.total_seconds() / 60))

def noOctal(num):
    for x, i in enumerate(num):
        if int(i) == 0:
            continue  
        return (num[x:])
    return 0
