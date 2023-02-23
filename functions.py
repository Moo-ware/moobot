import datetime
import json
import requests

eLevel = {
  0  : "",
  1  : "PRI",
  2  : "DUO",
  3  : "TRI",
  4  : "TET",
  5  : "PEN",
  20 : "PEN",
}

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

def matchEnhancement(key):
    return eLevel.get(key)


def timeCalc(timestamp):
    td = datetime.datetime.fromtimestamp(timestamp / 1e3) - datetime.datetime.now()
    return int(round(td.total_seconds() / 60))