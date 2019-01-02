# first you need to start apache and mysql from xampp
# then create a db named toures inside phpmyadmin
# then call this script via cmd "python creatdb.py"
# then go to 127.0.0.1:5000 via browser

#import MySQLdb
from flask import Flask, jsonify
#from flaskext.mysql import MySQL
import pymysql
app = Flask(__name__)
app.debug = True

def dropTable(name):
    return "DROP TABLE IF EXISTS {}".format(name)

# create tables
creatCustomer = """CREATE TABLE Customer (
Mail VARCHAR(160) NOT NULL,
CustTC VARCHAR(11) NOT NULL,
CustName VARCHAR(150) NOT NULL,
Phone VARCHAR(10) NOT NULL,
BirthDate DATE,
Password VARCHAR(30) NOT NULL,
PRIMARY KEY(Mail)
)
"""

creatReservation = """CREATE TABLE Reservation (
ReservationID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
Deadline DATE,
Price NUMERIC(8,2) NOT NULL,
PRIMARY KEY(ReservationID)
)
"""

creatTour = """CREATE TABLE Tour (
TourID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
BriefDescription VARCHAR(300),
FullDescription VARCHAR(6000),
Source VARCHAR(30),
Capacity INT(3) NOT NULL,
StartDate DATE,
EndDate DATE,
Rating INT(1),
BasePrice NUMERIC(8,2) NOT NULL,
ImgPath VARCHAR(50),
PRIMARY KEY(TourID)
)
"""

creatDependant = """CREATE TABLE Dependant (
DepID INT(10) UNSIGNED AUTO_INCREMENT,
DepTC VARCHAR(11) NOT NULL,
Name VARCHAR(30) NOT NULL,
BirthDate DATE,
Mail VARCHAR(160) NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(Mail) REFERENCES Customer(Mail),
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
PRIMARY KEY(DepID)
)
"""

# roomno in room ???
creatCruise = """CREATE TABLE Cruise (
CruiseName VARCHAR(30) NOT NULL,
CruiseCapacity INT(4) NOT NULL,
Stars INT(1),
PRIMARY KEY(CruiseName)
)
"""

creatHotel = """CREATE TABLE Hotel (
HotelName VARCHAR(30) NOT NULL,
Stars INT(1) NOT NULL,
PRIMARY KEY(HotelName)
)
"""

creatCruiseTour = """CREATE TABLE CruiseTour (
CruiseTourName VARCHAR(50) NOT NULL,
TourID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(TourID) REFERENCES Tour(TourID),
PRIMARY KEY(TourID, CruiseTourName)
)
"""

creatRegionalTour = """CREATE TABLE RegionalTour (
RegionalTourName VARCHAR(50) NOT NULL,
TourID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(TourID) REFERENCES Tour(TourID),
PRIMARY KEY(TourID, RegionalTourName)
)
"""

creatRoom = """CREATE TABLE Room (
RoomNO INT(4) NOT NULL,
RoomTYPE VARCHAR(10) NOT NULL,
Price INT(6) NOT NULL,
CruiseName VARCHAR(30) NOT NULL,
FOREIGN KEY(CruiseName) REFERENCES Cruise(CruiseName),
PRIMARY KEY(CruiseName, RoomNO)
)
"""

creatPromotion = """CREATE TABLE Promotion (
PromotionID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
PromotionType VARCHAR(10) NOT NULL,
SaleRate INT(4) NOT NULL,
PRIMARY KEY(PromotionID)
)
"""

creatSubtour = """CREATE TABLE Subtour (
SubtourID INT(10) NOT NULL AUTO_INCREMENT,
EventName VARCHAR(50) NOT NULL,
Description VARCHAR(2000) NOT NULL,
SubtourPrice NUMERIC(6,2) NOT NULL,
PRIMARY KEY(SubtourID)
)
"""

creatCity = """CREATE TABLE City (
CityName VARCHAR(30) NOT NULL,
Country VARCHAR(30) NOT NULL,
PRIMARY KEY(CityName)
)
"""

# Relations.....

creatCusSelectSub = """CREATE TABLE CusSelectsSub (
Mail VARCHAR(160) NOT NULL,
SubtourID INT(10) NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(Mail) REFERENCES Customer(Mail),
FOREIGN KEY(SubtourID) REFERENCES Subtour(SubtourID),
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
PRIMARY KEY(Mail, ReservationID, SubtourID)
)
"""

creatCusCancelRes = """CREATE TABLE CusCancelRes (
Time DATE NOT NULL,
Mail VARCHAR(160) NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(Mail) REFERENCES Customer(Mail),
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
PRIMARY KEY(Mail, ReservationID)
)
"""

creatCusMakeRes = """CREATE TABLE CusMakeRes (
Mail VARCHAR(160) NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(Mail) REFERENCES Customer(Mail),
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
PRIMARY KEY(Mail, ReservationID)
)
"""

# ouch
creatCusChooseRoom = """CREATE TABLE CusChooseRoom (
Mail VARCHAR(160) NOT NULL,
RoomNo INT(4) NOT NULL,
CruiseName VARCHAR(30) NOT NULL,
FOREIGN KEY(CruiseName) REFERENCES Cruise(CruiseName),
FOREIGN KEY(Mail) REFERENCES Customer(Mail),

PRIMARY KEY(Mail, CruiseName, RoomNo)
)
"""
#FOREIGN KEY(RoomNo) REFERENCES Room(RoomNo, CruiseName),
# dep related cus relation acquired from dependant ?

creatCusRatesTour = """CREATE TABLE CusRatesTour (
Mail VARCHAR(160) NOT NULL,
TourID INT(10) UNSIGNED NOT NULL,
Rate INT(1),
FOREIGN KEY(Mail) REFERENCES Customer(Mail),
FOREIGN KEY(TourID) REFERENCES Tour(TourID),
PRIMARY KEY(Mail, TourID)
)
"""

creatCruiseHas = """CREATE TABLE CruiseHas (
CruiseName VARCHAR(30) NOT NULL,
TourID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(CruiseName) REFERENCES Cruise(CruiseName),
FOREIGN KEY(TourID) REFERENCES CruiseTour(TourID),
PRIMARY KEY(TourID, CruiseName)
)
"""

creatRegHas = """CREATE TABLE RegHas (
HotelName VARCHAR(30) NOT NULL,
TourID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(HotelName) REFERENCES Hotel(HotelName),
FOREIGN KEY(TourID) REFERENCES RegionalTour(TourID),
PRIMARY KEY(TourID, HotelName)
)
"""

creatHotelPlacedCity = """CREATE TABLE HotelPlacedCity (
HotelName VARCHAR(30) NOT NULL,
CityName VARCHAR(30) NOT NULL,
FOREIGN KEY(HotelName) REFERENCES Hotel(HotelName),
FOREIGN KEY(CityName) REFERENCES City(CityName),
PRIMARY KEY(HotelName, CityName)
)
"""

creatCityIncludesSub = """CREATE TABLE CityIncludesSub (
CityName VARCHAR(30) NOT NULL,
SubtourID INT(10) NOT NULL,
FOREIGN KEY(SubtourID) REFERENCES Subtour(SubtourID),
FOREIGN KEY(CityName) REFERENCES City(CityName),
PRIMARY KEY(SubtourID, CityName)
)
"""

creatTourVisitCity = """CREATE TABLE TourVisitCity (
TourID INT(10) UNSIGNED NOT NULL,
CityName VARCHAR(30) NOT NULL,
TransportationType VARCHAR(30) NOT NULL,
Date DATE,
FOREIGN KEY(CityName) REFERENCES City(CityName),
FOREIGN KEY(TourID) REFERENCES Tour(TourID),
PRIMARY KEY(TourID, CityName)
)
"""

creatResArisesFrom = """CREATE TABLE ResArisesFrom (
TourID INT(10) UNSIGNED NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
FOREIGN KEY(TourID) REFERENCES Tour(TourID),
PRIMARY KEY(TourID, ReservationID)
)
"""

creatResProvidesPro = """CREATE TABLE ResProvidesPro (
PromotionID INT(10) UNSIGNED NOT NULL,
ReservationID INT(10) UNSIGNED NOT NULL,
FOREIGN KEY(ReservationID) REFERENCES Reservation(ReservationID),
FOREIGN KEY(PromotionID) REFERENCES Promotion(PromotionID),
PRIMARY KEY(PromotionID, ReservationID)
)
"""

def refresh(cur):
    # first delete relations to prevent fk issues
    cur.execute(dropTable("CusSelectsSub"))
    cur.execute(dropTable("CusCancelRes"))
    cur.execute(dropTable("CusRatesTour"))
    cur.execute(dropTable("CusChooseRoom"))

    cur.execute(dropTable("CusMakeRes"))
    cur.execute(dropTable("CruiseHas"))
    cur.execute(dropTable("RegHas"))
    cur.execute(dropTable("HotelPlacedCity"))
    cur.execute(dropTable("CityIncludesSub"))
    cur.execute(dropTable("TourVisitCity"))
    cur.execute(dropTable("ResArisesFrom"))
    cur.execute(dropTable("ResProvidesPro"))
                          

    # then delete entities
    cur.execute(dropTable("Dependant"))
    cur.execute(dropTable("Customer"))
    cur.execute(dropTable("CruiseTour"))
    cur.execute(dropTable("RegionalTour"))
    cur.execute(dropTable("Hotel"))
    cur.execute(dropTable("Tour"))
    cur.execute(dropTable("Reservation"))
    cur.execute(dropTable("Promotion"))
    cur.execute(dropTable("City"))
    cur.execute(dropTable("Subtour"))
    cur.execute(dropTable("Room"))
    cur.execute(dropTable("Cruise"))
    

    # then create entities
    cur.execute(creatCustomer)
    cur.execute(creatDependant)
    cur.execute(creatTour)   
    cur.execute(creatReservation)  
    cur.execute(creatCity)   
    cur.execute(creatSubtour) 
    cur.execute(creatCruise)
    cur.execute(creatPromotion) 
    cur.execute(creatHotel)
    cur.execute(creatCruiseTour)
    cur.execute(creatRegionalTour)
    cur.execute(creatRoom)
    # then create relations
    cur.execute(creatCusChooseRoom)
    cur.execute(creatCusSelectSub)
    cur.execute(creatCusCancelRes)
    cur.execute(creatCusRatesTour)


    cur.execute(creatCusMakeRes)
    cur.execute(creatCruiseHas)
    cur.execute(creatRegHas)
    cur.execute(creatHotelPlacedCity)
    cur.execute(creatCityIncludesSub)
    cur.execute(creatTourVisitCity)
    cur.execute(creatResArisesFrom)
    cur.execute(creatResProvidesPro)
        
indexlol = """<!DOCTYPE html>
<html>
<head>program me daddy UwU</head><br>
<body>
<a href="http://127.0.0.1:5000/recreate">create db</a><br>
<a href="http://127.0.0.1:5000/example">insert customer and tour</a><br>
<a href="http://127.0.0.1:5000/seeCust">see customers</a>
</body>
</html>
"""
@app.route("/")
def index():
    return(indexlol)
@app.route("/recreate/")
def recreate():
    db = pymysql.connect("localhost", "root", "","toures")
#    db = MySQL.connect()
    cur = db.cursor()

    refresh(cur)
    
    data = cur.fetchall()
    #print(data)
    #return jsonify(data)
    return("database created from scratch")

qlist = []

customers = """INSERT INTO Customer(
Mail,CustTC,CustName,Phone,BirthDate,Password)
VALUES
("example@ex.com", "1111", "example customer", "1231231232", "1991-11-11", "pass"),
("example2@ex.com", "12212", "example customer2", "1231231231", "1991-11-11", "pass2")
"""

qlist.append(customers)

tours = """INSERT INTO Tour (
TourID,BriefDescription,FullDescription,Source,Capacity,StartDate,EndDate,Rating,BasePrice, ImgPath)
VALUES
(NULL, "tour1 bd", "tour1 fd", "yozgat", 15, "2005-11-2", "2005,12-2",3, 2000, "static/airconditioner.png"),
(NULL, "tour2 bd", "tour2 fd", "kars", 18, "2005-11-3", "2005-12-3",4, 2001, "static/regional.jpg"),
(NULL, "tour3 bd", "tour3 fd", "london", 15, "2005-11-2", "2005,12-2",3, 2002, "static/airconditioner.png"),
(NULL, "tour4 bd", "tour4 fd", "rize", 15, "2005-11-2", "2005,12-2",3, 2003, "static/regional.jpg"),
(NULL, "tour5 bd", "tour5 fd", "istanbul", 15, "2003-11-2", "2003,12-2",3, 2007, "static/suite.jpg"),
(NULL, "tour6 bd", "tour6 fd", "rize", 15, "2002-11-2", "2002,12-2",3, 2003, "static/shower.jpg"),
(NULL, "tour7 bd", "tour7 fd", "rize", 15, "2002-11-2", "2002,12-2",3, 2003, "static/tourinf.jpg")
"""
qlist.append(tours)
cruise = """INSERT INTO Cruise (
CruiseName,CruiseCapacity,Stars)
VALUES
("cruise1", 300, 2),
("cruise2", 200, 4)"""
qlist.append(cruise)
hotel = """INSERT INTO Hotel (
HotelName, Stars)
VALUES
("hotel1",3),
("hotel2",4)"""
qlist.append(hotel)
cruisetour = """INSERT INTO CruiseTour (
CruiseTourName,TourID)
VALUES
("ct1", 1),
("ct2", 3)"""
qlist.append(cruisetour)
regtour = """INSERT INTO RegionalTour (
RegionalTourName,TourID)
VALUES
("rt1", 2),
("rt2", 4)"""
qlist.append(regtour)

dependant = """INSERT INTO Dependant (
DepID,DepTC,Name,BirthDate,Mail)
VALUES
(NULL, "123", "dep1", "1993-3-3", "example@ex.com"),
(NULL, "123", "dep2", "1993-3-3", "example@ex.com"),
(NULL, "123", "dep3", "1993-3-3", "example2@ex.com"),
(NULL, "123", "dep4", "1993-3-3", "example2@ex.com"),
(NULL, "123", "dep5", "1993-3-3", "example2@ex.com")
"""
qlist.append(dependant)

reserv = """INSERT INTO Reservation (
ReservationID, Deadline, Price)
VALUES
(NULL, "2008-1-1", 343),
(NULL, "2008-1-1", 349),
(NULL, "2008-1-1", 344),
(NULL, "2008-1-1", 345)
"""
qlist.append(reserv)

cmr = """INSERT INTO CusMakeRes
(Mail, ReservationID)
VALUES
("example@ex.com",1),
("example2@ex.com",2),
("example@ex.com",3),
("example@ex.com",4)
"""
qlist.append(cmr)

raf = """INSERT INTO ResArisesFrom
(TourID, ReservationID)
VALUES
(1,1),
(2,2),
(3,3),
(4,4)
"""
qlist.append(raf)

city = """INSERT INTO CITY(
CityName, Country)
VALUES
("ankara", "turkey"),
("yozgat", "turkey"),
("rize", "turkey"),
("london", "england")
"""
qlist.append(city)
tvc = """INSERT INTO TourVisitCity (
TourID, CityName, TransportationType, Date)
VALUES
(1,"ankara","bus","2005-3-1"),
(1,"yozgat","ferry","2008-4-3")
"""
qlist.append(tvc)

subs = """INSERT INTO Subtour(
SubtourID, EventName, Description, SubtourPrice)
VALUES
(NULL, "leblebi yeme festivali", "leb demeden", 5),
(NULL, "sushi fest", "japonyanin buz gibi sulari", 12),
(NULL, "kola dokme", "kahrolsun emperyalizm", 1)
"""
qlist.append(subs)
cis = """INSERT INTO CityIncludesSub(
CityName, SubtourID)
VALUES
("yozgat", 1),
("ankara", 2)
"""
qlist.append(cis)
@app.route("/example/")
def example():
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    for i in qlist:
        cur.execute(i)
    db.commit()
    cur.execute("SELECT * FROM Tour")
    data = cur.fetchall()

    return("thank you daddy UwU")
@app.route("/seeCust/")
def seeCust():
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()

    cur.execute("SELECT * FROM Customer")
    data = cur.fetchall()

    return jsonify(data)

if __name__ == '__main__':
    app.run()
