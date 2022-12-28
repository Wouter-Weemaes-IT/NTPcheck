#TODO:toevoegen gebruik maken van python: !/usr/bin/python3
import urllib.request
import time
import datetime
import json
import sys
JSONreturn = ""
InputURL = sys.argv[2]
UnixTimeStamp = 0


tijd = []
data = []

def addHTTP(inputURL):
    #check if the inputURL has http:// or https://
    if inputURL.startswith("http://") or inputURL.startswith("https://"):
        pass
    else:
        inputURL = "http://" + inputURL
    return inputURL
    

#mogelijke oplossing, zet de tijd om naar seconden, en vergelijk da
def dateTime(url):
    response = urllib.request.urlopen(url)
    date = response.info().get('Date')

    return date
#splitst the date header into a list, and takes the time out as well
#code currently has no need for time zone since any header read will be converted to local time
def TimeSplit(date):
    date = date.split(" ")
    
    seconden = date[4].split(":")
    #remove elements from date that are not needed
    del date[0]
    del date[3]
    del date[3]
    #add the time to the date list
    for i in range(len(seconden)):
        date.append(seconden[i])
    return date
#TODO:als het kan mooier maken ;)
#converts month to number
def MonthConverter(date):
    #convert the abreviated month to a number in index 1 without padded 0
    if date[1] == "Jan":
        date[1] = "1"
    elif date[1] == "Feb":
        date[1] = "2"
    elif date[1] == "Mar":
        date[1] = "3"
    elif date[1] == "Apr":
        date[1] = "4"
    elif date[1] == "May":
        date[1] = "5"
    elif date[1] == "Jun":
        date[1] = "6"
    elif date[1] == "Jul":
        date[1] = "7"
    elif date[1] == "Aug":
        date[1] = "8"
    elif date[1] == "Sep":
        date[1] = "9"
    elif date[1] == "Oct":
        date[1] = "10"
    elif date[1] == "Nov":
        date[1] = "11"
    elif date[1] == "Dec":
        date[1] = "12"
    return date
    
def ChangeOrderList(date):
    NewOrderList = [2,1,0,3,4,5]
    date = [date[i] for i in NewOrderList]
    #change all items into an int 
    date = [int(i) for i in date]
    return date
#converts the date to a unix timestamp
def ConvertTimeToUnix(date):
    date_time = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])
    TimeStamp = time.mktime(date_time.timetuple())
    return TimeStamp
#TODO:Betere naam geven, zoals ntp_check
def AllTogether(url):
    URL = addHTTP(url)
    #pulls needed data from headers
    try:
        date = dateTime(URL)
    except:
        print("{}")
        sys.exit(1)
    #filters out needed data & splits time into HH MM SS
    date = TimeSplit(date)
    #converts month into  an int
    #current format =   DD MM YYYY HH MM SS
    #wanted format =    YYYY, MM, DD, HH, MM, SS
    #new orderlist=    [2,1,0,3,4,5]
    date = MonthConverter(date)

    date = ChangeOrderList(date)
    UnixTimeStamp = ConvertTimeToUnix(date)
    return UnixTimeStamp

#TODO:main van maken.
#TODO: toevoegen documentatie args zie chat
spil = AllTogether("https://google.com")
teVergelijken = AllTogether(InputURL) 
#substract te difference to know if it's in sync
#JSONreturn = "NTP server is correctly syncronised", convert this to a JSON object  
JSONreturn = '{"message": "NTP server is not correctly synchronized", "status": "error"}' 
verschil = abs(spil - teVergelijken)
if verschil < 10:
    JSONreturn = '{"message": "NTP server is correctly synchronized", "status": "success"}'
json_object = json.loads(JSONreturn)
print(json_object)


#print("verschil", verschil)
