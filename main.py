from flask import Flask, render_template, jsonify, request, url_for, redirect
import pymysql, base64
from decimal import Decimal, getcontext


app = Flask(__name__)
#mysql = MySQL(app)
getcontext().prec = 2
passed = False
mail = None
selectedTourID = None
currentPrice = None
total = None
adults = None
children = None
data = None
lastresID = None
def intervals():
    print("in tervals")
    if request.method == 'POST':
        global total
        global adults
        global children
        adults = int(request.form['Adults'])
        children = int(request.form['Children'])
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        total = int(adults) + int(children)
        return "Capacity >= {} AND StartDate >= STR_TO_DATE({}, '%Y-%m-%d') AND EndDate <= STR_TO_DATE({}, '%Y-%m-%d')"\
               .format(total, "'{}'".format(startdate), "'{}'".format(enddate))
    else:
        return None
@app.route('/', methods=['POST', 'GET'])
def home():
    global total
    global passed
    global selectedTourID
    global lastresID
    total = None
    #selectedTourID = None
    if passed:
        if request.method == 'POST':
            lastresID = request.form['rescode']
            print(lastresID)
            return redirect(url_for('resinfo'))
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/allregional/', methods=['GET','POST'])
def allregional():
    global data
    global selectedTourID
    global currentPrice
    selectedTourID = None
    currentPrice = None
    data = None
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    cur.execute("SELECT * FROM RegionalTour")
    data = cur.fetchall()
    temp = {}
    print("\n\n")
    print(data)
    print("\n\n")
    if request.method == 'GET':
        for i in data:
            cur.execute("SELECT * FROM Tour WHERE TourID = {}".format(int(i[1])))
            temp[i[0]] = cur.fetchall()
    if request.method == "POST":
        print(request.data)
        if request.form['clickies'] == '0':
            temp = {}
            for i in data:
                print(i)
                interval = intervals()
                if interval != None:
                    print(interval)
                    cur.execute("SELECT * FROM Tour WHERE TourID = {} AND {}".format(int(i[1]), intervals()))
                else:
                    cur.execute("SELECT * FROM Tour WHERE TourID = {}".format(int(i[1])))
                temp[i[0]] = cur.fetchall()
            print(temp)
            for i in list(temp):
                if len(temp[i]) == 0:
                    del temp[i]
            

        
        else:

            print(selectedTourID)
            
                
            print(selectedTourID)
            selectedTourID = request.form['clickies']
            print(selectedTourID)
            return redirect(url_for('tourinfo'))
    return render_template('allregional.html', result=temp)
@app.route('/allcruise/', methods=['GET','POST'])
def allcruise():
    global data
    global selectedTourID
    global currentPrice
    selectedTourID = None
    currentPrice = None
    data = None
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    cur.execute("SELECT * FROM CruiseTour")
    data = cur.fetchall()
    temp = {}
    print("\n\n")
    print(data)
    print("\n\n")
    if request.method == 'GET':
        for i in data:
            cur.execute("SELECT * FROM Tour WHERE TourID = {}".format(int(i[1])))
            temp[i[0]] = cur.fetchall()
    #cur.execute("SHOW columns FROM Tour")
    #x = cur.fetchall()
    #temp['columns'] = [i[0] for i in x]
    print(request.data)
    if request.method == "POST":
        print('in post')
        if request.form['clickies'] == '0':
            temp = {}
            for i in data:
                print(i)
                interval = intervals()
                if interval != None:
                    print(interval)
                    cur.execute("SELECT * FROM Tour WHERE TourID = {} AND {}".format(int(i[1]), intervals()))
                else:
                    cur.execute("SELECT * FROM Tour WHERE TourID = {}".format(int(i[1])))
                temp[i[0]] = cur.fetchall()
            print(temp)
            for i in list(temp):
                if len(temp[i]) == 0:
                    del temp[i]
        
        else:

            print(selectedTourID)
            
                
            print(selectedTourID)
            selectedTourID = request.form['clickies']
            print(selectedTourID)
            return redirect(url_for('tourinfocruise'))
    return render_template('allcruise.html', result=temp)
        
@app.route('/room/')
def room():
    global data
    data = None
    return render_template('room.html')

@app.route('/pastreservations/', methods=['GET', 'POST'])
def pastreservations():
    
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    global mail
    global selectedTourID
    cur.execute("SELECT ReservationID FROM CusMakeRes WHERE Mail = {}".format("'{}'".format(mail)))
    data = cur.fetchall()
    x = ", ".join(["'{}'".format(str(i[0])) for i in data])
    if len(x) > 1:
        cur.execute("SELECT TourID, BriefDescription, StartDate, EndDate, Rating, BasePrice, ImgPath FROM Reservation NATURAL JOIN ResArisesFrom NATURAL JOIN Tour WHERE ReservationID IN ({}) AND EndDate < CURDATE()".format(x))
        data = cur.fetchall()
        data = list(data)
        for row in data:
            row = list(row)
    print('before post')
    if request.method == 'POST':
        print('in POST')
        selectedTourID = request.form['sendrate']
        print(selectedTourID)
        return redirect(url_for('rate'))
        
    return render_template('pastreservations.html', result = data)

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    global mail
    mail = ''
    if request.method == 'POST':
        
        db = pymysql.connect("localhost", "root", "","toures")
        cur = db.cursor()
        name = request.form['name']
        tc = request.form['tc']
        mail = request.form['email']
        phone = request.form['phone']
        bday = request.form['bday']
        psw = request.form['psw']
        print(bday)
        cur.execute("INSERT INTO Customer(Mail, CustTC, CustName, Phone, BirthDate, Password) \
        VALUES ('{}','{}','{}','{}','{}','{}')".format(mail,tc,name,phone,bday,psw))
        db.commit()
        redirect('login.html')
    return render_template('signup.html')


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        global mail
        psw = request.form['psw']
        uname = request.form['uname']
        db = pymysql.connect("localhost", "root", "","toures")
        cur = db.cursor()
        mail = uname
        uname = "'{}'".format(uname)
        cur.execute("SELECT Password FROM Customer WHERE Mail = {};".format(uname))
        dbpsw = cur.fetchall()
        if len(dbpsw) != 0:
            global passed
            if dbpsw[0][0] == psw:
                passed = True
                
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/tourinfo/')
def tourinfo():
    db = pymysql.connect("localhost", "root", "","toures")
    global currentPrice
    global data
    global adults
    global children
    global total
    cur = db.cursor()
    
    cur.execute("SELECT RegionalTourName, FullDescription, Source, StartDate, EndDate, Rating, BasePrice FROM Tour NATURAL JOIN RegionalTour WHERE TourID = {}".format(int(selectedTourID)))
    #cur.execute("SELECT FullDescription, Source, StartDate, EndDate, Rating, BasePrice FROM Tour WHERE TourID = {}".format(int(selectedTourID)))
    tourInfo = cur.fetchall()
    print(tourInfo)
    if currentPrice == None:
        currentPrice = Decimal(tourInfo[0][6]) * Decimal(adults) + Decimal(tourInfo[0][6]) * Decimal(children * (4/5))
  
        cur.execute("SELECT CityName, EventName, Description, SubtourPrice, SubtourID FROM TourVisitCity NATURAL JOIN CityIncludesSub NATURAL JOIN Subtour WHERE TourID = {}".format(int(selectedTourID)))
        data = cur.fetchall()
        data = list(data)
    if request.method == 'POST':
        if "add" in request.form['addremove']:
            subtourID = request.form['addremove'][3:]
            subPrice = 0
            for i in data:
                if int(i[4]) == int(subtourID):
                    subPrice = Decimal(i[3])*Decimal(total)
                    data.remove(i)

            
            currentPrice+=Decimal(subPrice)
            print(currentPrice)
    return render_template('tourinfo.html', tourInfo=tourInfo, data=data, totalprice=("%.2f" % round(currentPrice,2)))


@app.route('/touristinfo/', methods=['POST', 'GET'])
def touristinfo():
    global total
    global currentPrice
    global mail
    global selectedTourID
    global adults
    global children
    global total
    global lastresID
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    if request.method == 'POST':
        deps = []
        for i in range(total-1):
            deps.append([request.form['firstname' + str(i)], request.form['lastname' + str(i)], request.form['birthdate' + str(i)], request.form['tc' + str(i)]])

        print(deps)
        cur.execute("INSERT INTO Reservation (ReservationID, Deadline, Price) VALUES (NULL, CURDATE(), {})".format(currentPrice)) #CURDATE SHOULD BE CHANGED
        cur.execute("SELECT LAST_INSERT_ID() FROM Reservation")
        myid = cur.fetchall()
        myid = myid[0][0]
        cur.execute("SELECT Capacity FROM Tour WHERE TourID = {}".format(int(selectedTourID)))
        cap = cur.fetchall()
        print(cap)
        cap = cap[0][0]
        print(cap)
        cap = cap - total
        cur.execute("INSERT INTO CusMakeRes(Mail, ReservationID) VALUES ('{}',{})".format(mail, myid))
        cur.execute("INSERT INTO ResArisesFrom(TourID, ReservationID) VALUES({}, {})".format(selectedTourID, myid))
        cur.execute("UPDATE Tour SET Capacity = {} WHERE TourID = {}".format(int(cap), int(selectedTourID)))
        lastresID = myid
        for i in deps:
            cur.execute("INSERT INTO Dependant(DepID, DepTC, Name, BirthDate, mail) VALUES (NULL, '{}', '{}', STR_TO_DATE('{}', '%Y-%m-%d'), '{}')".format(i[3], i[0] + ' ' + i[1], i[2], mail))
        db.commit()
        

        return redirect(url_for('resinfo'))
                
    return render_template('touristinfo.html', total=total)

@app.route('/tourinfocruise/', methods=['POST','GET'])
def tourinfocruise():
    db = pymysql.connect("localhost", "root", "","toures")
    global currentPrice
    global data
    global adults
    global children
    global total
    cur = db.cursor()
    cur.execute("SELECT CruiseTourName, FullDescription, Source, StartDate, EndDate, Rating, BasePrice, Capacity FROM Tour NATURAL JOIN CruiseTour WHERE TourID = {}".format(int(selectedTourID)))
    tourInfo = cur.fetchall()
    print(tourInfo)
    if currentPrice == None:
        currentPrice = Decimal(tourInfo[0][6]) * Decimal(adults) + Decimal(tourInfo[0][6]) * Decimal(children * (9/10))
  
        cur.execute("SELECT CityName, EventName, Description, SubtourPrice, SubtourID FROM TourVisitCity NATURAL JOIN CityIncludesSub NATURAL JOIN Subtour WHERE TourID = {}".format(int(selectedTourID)))
        data = cur.fetchall()
        data = list(data)
    if request.method == 'POST':
        if "add" in request.form['addremove']:
            subtourID = request.form['addremove'][3:]
            subPrice = 0
            for i in data:
                if int(i[4]) == int(subtourID):
                    subPrice = Decimal(i[3]) * Decimal(total)
                    data.remove(i)

            
            currentPrice+=Decimal(subPrice)
            print(currentPrice)
            """
            elif "remove" in request.form['addremove']:
                subtourID = request.form['addremove'][6:]
                print(subtourID)
                subPrice = 0
                for i in data:
                    if i[4] == subtourID:
                        subPrice = i[3]
                currentPrice-=Decimal(subPrice)
                print(currentPrice)
            """
        #return render_template('tourinfocruise.html', data=data)
    return render_template('tourinfocruise.html', data=data, totalprice=("%.2f" % round(currentPrice,2)), tourInfo=tourInfo)

@app.route('/rate/', methods=['POST','GET'])
def rate():
    global selectedTourID
    global mail
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    cur.execute("SELECT TourID, BriefDescription, StartDate, EndDate, Rating, BasePrice, ImgPath FROM Reservation NATURAL JOIN ResArisesFrom NATURAL JOIN Tour WHERE ReservationID = {}".format(int(selectedTourID)))
    result = cur.fetchall()        
    if request.method == 'POST':
        rating = request.form['rating']
        
        cur.execute("INSERT INTO CusRatesTour(Mail, TourID, Rate) VALUES ('{}', {}, {}) ON DUPLICATE KEY UPDATE Rate = {}".format(mail, int(selectedTourID), int(rating),int(rating)))
        db.commit()
    return render_template('rate.html', result=result)

@app.route('/resinfo/', methods=['GET', 'POST'])
def resinfo():
    global lastresID
    global mail
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    cur.execute("SELECT Mail, CustName  From CusMakeRes NATURAL JOIN Customer WHERE ReservationID = {}".format(int(lastresID)))
    current = cur.fetchall()
    print(current)
    curmail = current[0][0]
    
    print(curmail)
    print(mail)
    if(curmail == mail):
        cur.execute("SELECT ReservationID, Deadline, StartDate,EndDate, Price, ImgPath FROM Reservation NATURAL JOIN ResArisesFrom NATURAL JOIN Tour WHERE ReservationID = {}".format(int(lastresID)))
        data = cur.fetchall()
        print(data)
        lastresID=None
    else:
        print('access denied')
    return render_template('resinfo.html', name=current[0][1], data=data)
@app.route('/developer/', methods=['GET'])
def developer():
    
    db = pymysql.connect("localhost", "root", "","toures")
    cur = db.cursor()
    """
    cur.execute("SELECT tourID, AVG(DATEDIFF(CURDATE()-BirthDate)) FROM Tour \
NATURAL JOIN ResArisesFrom NATURAL JOIN Reservation NATURAL \
JOIN CusMakeRes NATURAL JOIN Customer GROUP BY TourID")
    a = cur.fetchall()
    x = []
    a = list(a)
    for i in a:
        i = list(i)
        x.append(list(i))
        print(i)
        i[1] = float(i[1])
    print(a)
    print(x)
    for i in x:
        i[1] = float(i[1])/365
    return jsonify(x)
    """
    cur.execute("SELECT Mail, Count(ReservationID) FROM CusMakeRes GROUP BY Mail")
    a= cur.fetchall()
    print(a)
    return jsonify(a)
    
if __name__ == '__main__':
    app.run(debug=True)
