# The Walk 1.0
# Note: complete version use CV2 and PIL to display maps and information on screen
# Roni Bandini, August 2023, @RoniBandini
# MIT License
# https://bandini.medium.com


from gmaps import Directions, Geocoding
import urllib.request
import cv2
from PIL import Image
from haversine import haversine, Unit
import math
from random import randint
import time
from datetime import datetime
from time import sleep
from gpiozero import Servo
import uuid
import requests, json
import openai


# Servo pins
rightFoot 	= Servo(2)
leftFoot	= Servo(3)

# Other settings
distanceKm	= 2
window_name = 'map'
up_width 	= 800
up_height 	= 480

# Google Maps API
googleMapsAPI='000000000000'
api 		= Directions(api_key=googleMapsAPI)
resolution	="400x400" # 800x480

# ChatGPT
openai.api_key  = "000000000000"
model_engine    = "text-davinci-003"
temperatura     = 0.8

# Weather API
BASE_URL    = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY     = "000000000000"

def writeLog(myLine):
    dt = datetime.now()
    with open('thewalklog.csv', 'a') as f:
        myLine=str(dt)+","+myLine
        f.write(myLine+"\n")

def saveJournal(myLine):
    dt = datetime.now()
    with open('thewalkjournal.csv', 'a') as f:
        myLine=str(dt)+" - "+myLine
        f.write(myLine+"\n")

def writeCoordinates(myCoordinates):
    with open('coordinates.csv', 'w+') as f:
        f.write(myCoordinates)

def readCoordinates():
    with open("coordinates.csv", 'r') as f:
        lines = f.readlines()
    myCoordinates=lines[0]
    myCoordinates	= myCoordinates.replace("\n","")
    return myCoordinates


def getWeather(myLat, myLong):
    URL = BASE_URL + "lat=" +str(myLat)+ "&lon=" +str(myLong)+ "&units=metric&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        report = data['weather']
        return report[0]['description']
    else:
        print("No weather information")

# Get a map point at a distance
def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    a = math.radians(bearing)
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(a))
    lon2 = lon1 + math.atan2(math.sin(a) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat2))
    return (math.degrees(lat2), math.degrees(lon2),)

# Walk
def walk(myDistance):

    try:
        while myDistance>0:
            rightFoot.min()
            leftFoot.min()
            sleep(0.5)
            rightFoot.mid()
            leftFoot.mid()
            sleep(0.5)
            myDistance=myDistance-1
            print("Walking...")
    except KeyboardInterrupt:
        print("Exit")
        sys.exit(0)


def escribirDiario(myFecha,myClima,myDistancia,myDestino, myCantidadDePalabras):

    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M:%S")

    prompt          ="Write a personal diary entry full of adjectives and perceptions for "+myFecha+" date at "+currentTime +" using "+myCantidadDePalabras+" words. You have just walked " +myDistancia+ " meters under "+myClima+" weather until reaching "+myDestino

    completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=temperatura,
            )

    return completion.choices[0].text

def getAddress(myLat, myLong):

    myLat       = float(myLat)
    myLong      = float(myLong)
    apiGeoCoding = Geocoding(api_key=googleMapsAPI)
    return apiGeoCoding.reverse(myLat, myLong)[0]["formatted_address"]

def getDateAndTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


print("The Walk")
print("@RoniBandini, September 2023")
print("MIT License")
print("")


myLoop=1

while True:
#while myLoop<2:

    totalDistance = 0

    filename 	= str(uuid.uuid4())
    myBearing	= randint(1, 360)

    origin      = readCoordinates()
    originArray = origin.split(",")

    myLat       = float(originArray[0])
    myLong      = float(originArray[1])

    destination	= str(get_point_at_distance(myLat, myLong, distanceKm, myBearing, R=6371))
    destination	= destination.replace("(","")
    destination	= destination.replace(")","")

    print("Origin:"+origin)
    print("Bearing:"+str(myBearing))
    print("Random destination:"+destination)

    # Get directions
    results=api.directions(origin, destination, mode="walking")

    myCounter=1

    for myStep in results[0]['legs'][0]['steps']:

        myLatStart	=str(myStep['start_location']["lat"])
        myLongStart	=str(myStep['start_location']["lng"])
        myLatEnd	=str(myStep['end_location']["lat"])
        myLongEnd	=str(myStep['end_location']["lng"])
        myDistance	=int(myStep['distance']["value"])

        # get Weather
        myWeather=getWeather(myLatEnd,myLongEnd)

        # get destination address
        myDestinationAddress=getAddress(myLatEnd,myLongEnd)
        print("Destination address: "+myDestinationAddress)

    	# get route map
        imgURL = "https://maps.googleapis.com/maps/api/staticmap?size="+resolution+"&path="+myLatStart+","+myLongStart+"|"+myLatEnd+","+myLongEnd+"&markers=size:mid%7Ccolor:red%7C"+myLatEnd+","+myLongEnd+"&key="+googleMapsAPI
        myRouteFileName="/home/roni/images/route-"+str(filename)+"-"+str(myCounter)+".jpg"
        urllib.request.urlretrieve(imgURL, myRouteFileName)

        walk(myDistance)

        writeCoordinates(myLatEnd+','+myLongEnd)

    	# take destination picture
        imgURL = "https://maps.googleapis.com/maps/api/streetview?size="+resolution+"&location="+myLatEnd+","+myLongEnd+"&fov=80&heading=0&source=outdoor&pitch=0&key="+googleMapsAPI
        mySnapFileName="/home/roni/images/snap-"+str(filename)+"-"+str(myCounter)+".jpg"
        urllib.request.urlretrieve(imgURL, mySnapFileName)

        print("Duration: "+str(int(myStep['duration']["value"])/60))
        print("Distance: "+ str(myDistance)+" meters")
        print("Starting:" +myLatStart+","+myLongStart)
        print("Ending: "+ myLatEnd+","+myLongEnd)
        print("Weather: "+ myWeather)

        totalDistance=totalDistance+myDistance

        # log
        myLine=myLatStart+','+myLongStart+','+myLatEnd+','+myLongEnd+','+str(myDistance)+',\''+myRouteFileName+"\',\'"+mySnapFileName+"\',\'"+myWeather+"\',\'"+myDestinationAddress+"\'"
        writeLog(myLine)

        myCounter=myCounter+1

    # write journal
    myJournal=escribirDiario(getDateAndTime(),myWeather,str(totalDistance),myDestinationAddress, "50")

    # save journal into file
    saveJournal(myJournal)

    myJournal=myJournal+" -- journey entry written by ChatGPT"

    print("Journal entry: "+ myJournal)

    sleep(10)

    myLoop=myLoop+1
