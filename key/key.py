#import libraries
from flask import Flask, request, session, abort, redirect, render_template, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flaskext.mysql import MySQL
import datetime
from itsdangerous import URLSafeSerializer, BadSignature
from flask_mail import Mail, Message

#craete a flask app instance
app = Flask(__name__)

#set the secret key
app.secret_key = "development_key"

#app configaration section for mysql server connection
#this set of configuration is for production environment
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'xxxxx'
app.config['MYSQL_DATABASE_USER'] = 'xxxxx'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xxxxx'
app.config['MYSQL_DATABASE_DB'] = 'xxxxxx'
mysql.init_app(app)

mail = Mail()

app.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'example@gmail.com',
	MAIL_PASSWORD = 'example',
    MAIL_DEFAULT_SENDER = 'example@gmail.com'
	)
mail.init_app(app)

serializer = URLSafeSerializer('secret-key')

#this set of configuration is for development environment
#mysql = MySQL()
#app.config['MYSQL_DATABASE_HOST'] = 'xxxx'
#app.config['MYSQL_DATABASE_PORT'] = xxxx
#app.config['MYSQL_DATABASE_USER'] = 'xxxx'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'xxxx'
#app.config['MYSQL_DATABASE_DB'] = 'xxxxx'
#mysql.init_app(app)


def getCurrentUser():
    #this function return current user in string info restored in database
    return session['user']


def getTodayString():
    #return today's date string in format "yyyy-mm-dd"
    now = datetime.datetime.now()
    month = str(now.month)
    if len(month) == 1:
        month = '0'+month
    return str(now.year)+'-'+month+'-'+str(now.day)

def regulateDatePickerString(dateString):
    #change and return the  "year month day" dateString in French into "yyyy-mm-dd" format
    dataList = dateString.split()
    month = dataList[1]
    if dataList[1] == 'January':
        month = '01'
    if dataList[1] == 'February':
        month = '02'
    if dataList[1] == 'March':
        month = '03'
    if dataList[1] == 'April':
        month = '04'
    if dataList[1] == 'May':
        month = '05'
    if dataList[1] == 'June':
        month = '06'
    if dataList[1] == 'July':
        month = '07'
    if dataList[1] == 'August':
        month = '08'
    if dataList[1] == 'September':
        month = '09'
    if dataList[1] == 'October':
        month = '10'
    if dataList[1] == 'November':
        month = '11'
    if dataList[1] == 'December':
        month = '12'
    return dataList[0] + '-' + month + '-' + dataList[2]

@app.route('/signin', methods = ['POST','GET'])
#the login function check if we have the matching email account and password in the database,
#if no, abort the application
#if so, mark the current status in admin table of this user to be true
def signin():
    error = None
    if request.method == 'POST':
        useremail = request.form['Useremail']
        password = request.form['Password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from admin where email=%s", (useremail,))
        data = cursor.fetchone()
        if data is None:
            error = "Username is incorrect."
        elif not check_password_hash(data[1], password):
            error = "Password is incorrect."
        elif data[5] == 'deactivated':
            error = "Account needs to be activated."
        else:
            flash("Logged in successfully")
            session['user'] = data
            session['logged_in'] = True
            return redirect(url_for('lend'))
    return render_template('signin.html', error=error)

@app.route('/lend', methods = ['POST', 'GET'])
#the 1/3 step of lend, display available keys
def lend():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #pull all available keys info
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select distinct keyNumber from clef where status='available' and active = 'yes' order by keyNumber asc;")
    keys = cursor.fetchall()
    #render html with available keys
    return render_template('lend.html', keys = keys)

@app.route('/infoLend', methods = ['POST', 'GET'])
#the 2/3 step of lend, request further information needed
def infoLend():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get keyNumber from html form
    keyNumber = request.form['keyNumber']
    conn = mysql.connect()
    cursor = conn.cursor()
    #pull client info
    cursor.execute("select * from client;")
    clients = cursor.fetchall()
    #pull available copies info
    cursor.execute("select * from clef where keyNumber='"+keyNumber+"' and status='available' and active = 'yes'")
    copies = cursor.fetchall()
    #pull depositValue info
    cursor.execute("select distinct depositValue from clef where keyNumber='"+keyNumber+"' and status='available' and active = 'yes'")
    depositValue = cursor.fetchone()
    #render html with available copies, client address, depositValue, and keyNumber
    return render_template('infoLend.html', copies = copies, clients = clients, depositValue = depositValue, keyNumber = keyNumber)

@app.route('/resultLend', methods = ['POST', 'GET'])
#The 3/3 step of lend, final confirmation and receipt
def resultLend():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get keyNumber, copyNumber, client email, paymentMethod, return deadline and depositValue from html form
    keyNumber = request.form['keyNumber']
    copyNumber = request.form['copyNumber']
    email = request.form['email']
    paymentMethod = request.form['paymentMethod']
    lendDate = str(request.form['lendDate'])
    lendDate = regulateDatePickerString(lendDate)
    expectedReturnDate = str(request.form['expectedReturnDate'])
    expectedReturnDate = regulateDatePickerString(expectedReturnDate)
    depositValue = request.form['depositValue']
    #get current user info in string
    currentUser = session['user'][0]
    #pull client info

    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        cursor.execute("select * from client where email='"+email+"'")
        client = cursor.fetchone()
        #commit new lend record into table lent
        cursor.execute("insert into lent values('"+keyNumber+"', '"+copyNumber+"', '"+email+"', '"+lendDate+"', '"+paymentMethod+"', '"+expectedReturnDate+"', '"+currentUser+"');")
        #commit status of the key copy just lent out
        cursor.execute("update clef set status='lent' where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"';")
        #pull this copies info
        cursor.execute("select * from lent where keyNumber='"+keyNumber+"'and copyNumber='"+copyNumber+"';")
        lent = cursor.fetchone()
        #render html with client address info, key just lentout info, its depositValue and admin
        conn.commit()
        return render_template('resultLend.html', client = client, lent = lent, depositValue = depositValue, currentUser = currentUser)
    except:
        error = "There was a problem lending out this key. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('lend'))

@app.route('/return', methods = ['POST', 'GET'])
#The 1/2 step of return, client address confirmation
def retrieve():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #pull all lending key copies with corresponding client address information
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select l.keyNumber, l.copyNumber, c.firstName, c.lastName, c.address, c.city, c.province, c.postcode from lent l, client c where c.email=l.email")
    keys = cursor.fetchall()
    #render html with lending key and its corresponding client address information
    return render_template('return.html', keys = keys)

@app.route('/resultReturn', methods=['POST', 'GET'])
#The 2/2 step of return, final confirmation and receipt
def resultReturn():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get today's date in string, it is gonna be used as returnDate(today)
    returnDate = getTodayString()
    #get current admin user
    currentUser = getCurrentUser()[0]
    #get keyNumber, keyCopy from html from
    keyNumber_copyNumber = str(request.form['keyNumber_copyNumber'])
    numberList = keyNumber_copyNumber.split()
    keyNumber = numberList[0]
    copyNumber = numberList[1]
    #pull client email, lendDate, paymenthod of lending from table lent

    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        #get client email, lendDate and paymentMethod
        cursor.execute("select email, lendDate, paymentMethod from lent where keyNumber='"+keyNumber+"' and copyNumber="+copyNumber+"")
        lend = cursor.fetchone()
        email = lend[0]
        lendDate = str(lend[1])
        lendpaymentMethod = lend[2]
        #pull client address using client email
        cursor.execute("select * from client where email ='"+email+"';")
        client = cursor.fetchone()
        #pull depositValue using keyNumber
        cursor.execute("select distinct depositValue from clef where keyNumber='"+keyNumber+"'")
        depositValue = cursor.fetchone()
        #commit the return records into return history table
        cursor.execute("insert into returnhistory (keyNumber, copyNumber, email, lendDate, returnDate, lendPaymentMethod, admin) values('"+keyNumber+"', '"+copyNumber+"', '"+email+"', '"+lendDate+"', '"+returnDate+"', '"+lendpaymentMethod+"', '"+currentUser+"')")
        #delete the lending records from lend table
        cursor.execute("delete from lent where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"'")

        cursor.execute("SELECT active FROM clef WHERE keyNumber=%s AND copyNumber=%s", (keyNumber, copyNumber))
        active = cursor.fetchone()[0]

        if active.lower() == 'yes':
            # Update clef table to set status of the key copy just returned back to 'available'
            cursor.execute("update clef set status='available' where keyNumber='" + keyNumber + "' and copyNumber='" + copyNumber + "'")

        elif active.lower() == 'no':
            cursor.execute("DELETE FROM clef WHERE keyNumber=%s AND copyNumber=%s", (keyNumber, copyNumber))

        #render html receipt with client address, depositValue, returnDate(today), lendDate, keyNumber and admin
        conn.commit()

        return render_template('resultReturn.html', client = client, depositValue = depositValue, returnDate = returnDate, lendDate = lendDate, keyNumber = keyNumber, currentUser = currentUser)

    except:
        error = "There was a problem returning this key. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('retrieve'))
@app.route('/reportPassedDueKeys', methods = ['POST', 'GET'])
#pret
def reportPassedDueKeys():
    if not session.get('logged_in'):
        abort(401)
    today = getTodayString()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select l.keyNumber, l.copyNumber,  l. lendDate, l.expectedReturnDate, c.firstName, c.lastName, c.phoneNumber, l.email from lent l, client c where l.email=c.email and l.expectedReturnDate<='"+today+"'")
    keys = cursor.fetchall()
    return render_template('reportPassedDueKeys.html', keys = keys)


@app.route('/loss', methods = ['POST', 'GET'])
#The 1/3 step of loss, lending key selectio and client address confirmation
def loss():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #pull all lending key and its correspoding client inforation from table lent
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select l.keyNumber, l.copyNumber, c.firstName, c.lastName, c.address, c.city, c.province, c.postcode from lent l, client c where l.email=c.email")
    keys = cursor.fetchall()
    #render html with all avialable lending keys with its client address attached respectively
    return render_template('loss.html', keys = keys)

@app.route('/infoLoss', methods = ['POST', 'GET'])
#The 2/3 step of loss, request penalty value and furthe informaiton
def infoLoss():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get keyNumber and keyCopy from html form
    keyNumber_copyNumber = str(request.form['keyNumber_copyNumber'])
    numberList = keyNumber_copyNumber.split()
    keyNumber = numberList[0]
    copyNumber = str(numberList[1])
    #pull penalty value for losing
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select penaltyValue from value v, clef c where c.keyNumber='"+keyNumber+"' and c.copyNumber='"+copyNumber+"' and c.depositValue=v.depositValue")
    penaltyValue = cursor.fetchone()[0]
    #render html with penaltyValue, keyNumber and copyNumber
    return render_template('infoLoss.html', penaltyValue = penaltyValue, keyNumber = keyNumber, copyNumber = copyNumber)

@app.route('/resultLoss', methods = ['POST', 'GET'])
#The 3/3 step of loss, final confirmation and receipt
def resultLoss():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get today's date in string
    lossDate = getTodayString()
    #get current admin user in string
    currentUser = getCurrentUser()[0]
    #get keyNumber, copyNumber, penaltyValue, paymentMethod from html form
    keyNumber = request.form['keyNumber']
    copyNumber = request.form['copyNumber']
    penaltyValue = request.form['penaltyValue']
    methodPay = request.form['methodPay']
    #pull client email and lendDate from table lent
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select email, lendDate from lent where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"'")
        lend = cursor.fetchone()
        email = lend[0]
        lendDate = str(lend[1])
        #pull client address from table client by client email
        cursor.execute("select * from client where email='"+email+"'")
        client = cursor.fetchone()
        #commit loss record into losshistory table
        cursor.execute("insert into losshistory values('"+keyNumber+"', '"+copyNumber+"', '"+email+"', '"+lendDate+"', '"+lossDate+"', '"+methodPay+"','"+currentUser+"') ")
        #delete lend record of the key copy just lost
        cursor.execute("delete from lent where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"'")
        #update the status of the key just lost into 'loss'
        cursor.execute("update clef set status='lost' where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"'")
        #puill newly lost key inforamtion form table losshistory
        #the reason to not using the informaiton above but pull it back from database is to validate this transection
        #to see if the loss record is succesfully added
        cursor.execute("select * from losshistory where keyNumber='"+keyNumber+"' and copyNumber='"+copyNumber+"'")
        loss = cursor.fetchone()
        #render html receipt with penaltyValue, client address informaiton, key inforamiton of the key just lost and admin
        conn.commit()
        return render_template('resultLoss.html', penaltyValue = penaltyValue, client = client, loss = loss, currentUser = currentUser)
    except:
        error = "There was a problem recording the loss of this key. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('loss'))

@app.route('/addKey', methods = ['POST', 'GET'])
#perte
def addKey():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM room")
    rooms = cursor.fetchall()
    return render_template('addKey.html', rooms = rooms)

@app.route('/resultAddKey', methods = ['POST', 'GET'])
#ajouter clef
def resultAddKey():
    if not session.get('logged_in'):
        abort(401)
    keyNumber = request.form['keyNumber']
    copyNumberStart = int(request.form['copyNumberStart'])
    copyNumberEnd = int(request.form['copyNumberEnd'])+1
    depositValue = request.form['depositValue']
    opens = request.form['opens']
    status = request.form['status']
    active = 'yes'
    rooms = request.form.getlist('room')
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        for copyNumber in range(copyNumberStart, copyNumberEnd):
            cursor.execute("insert into clef values('"+keyNumber+"', '"+str(copyNumber)+"','"+depositValue+"', '"+opens+"', '"+status+"', '"+active+"')")
        for room in rooms:
            cursor.execute("insert into unlocks values('"+keyNumber+"', "+str(room[0])+")")
        cursor.execute("select * from clef where keyNumber='"+keyNumber+"' and copyNumber>='"+str(copyNumberStart)+"' and copyNumber<='"+str(copyNumberEnd)+"'")
        keys = cursor.fetchall()
        conn.commit()
        return render_template('resultAddKey.html', keys = keys)
    except:
        error = "There was a problem adding this key. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("addKey"))

@app.route('/deleteKey', methods = ['POST', 'GET'])
def deleteKey():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute('SELECT DISTINCT keyNumber FROM clef WHERE active=%s', ('yes',))
        keys = cursor.fetchall()
        return render_template('deleteKey.html', keys=keys)

    elif request.method == 'POST':
        key = request.form['key']
        cursor.execute('SELECT copyNumber, opens, status FROM clef WHERE keyNumber=%s AND status!=%s', (key, 'lent'))
        deleteKeys = cursor.fetchall()

        cursor.execute("select c.copyNumber, c.opens, l.email, l.lendDate, l.expectedReturnDate, l.admin from lent l, clef c where l.keyNumber='" + key + "' and l.keyNumber=c.keyNumber and l.copyNumber=c.copyNumber;")
        deactivateKeys = cursor.fetchall()

        cursor.execute('SELECT address FROM room JOIN unlocks ON id=roomID WHERE keyNumber=%s', (key,))
        rooms = cursor.fetchall()
        return render_template('infoDeleteKey.html', key=key, deleteKeys=deleteKeys, deactivateKeys=deactivateKeys, rooms=rooms)

@app.route('/resultDeleteKey', methods = ['POST'])
def resultDeleteKey():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == 'POST':
        key = request.form['key']

        try:
            cursor.execute('DELETE FROM clef WHERE keyNumber=%s AND status!=%s', (key, 'lent'))
            cursor.execute('UPDATE clef SET active=%s WHERE keyNumber=%s AND status=%s', ('no', key, 'lent'))
            conn.commit()
            message = 'Key successfully deleted.'
            flash(message)
            return redirect(url_for('deleteKey'))

        except:
            conn.rollback()
            error = 'There was a problem deleting this key. Please try again.'
            flash(error)
            return redirect(url_for('deleteKey'))

@app.route('/changeKey', methods = ['POST', 'GET'])
#searh profile for one clinet
def changeKey():
    if not session.get('logged_in'):
        abort(401)
    cursor = mysql.connect().cursor()
    cursor.execute("select distinct keyNumber, room from room ")
    keys = cursor.fetchall()
    return render_template('changeKey.html', keys = keys)

@app.route('/resultChangeKey', methods = ['POST', 'GET'])
#searh profile for one clinet
def resultChangeKey():
    if not session.get('logged_in'):
        abort(401)
    keyNumber = request.form['keyNumber']
    room = request.form['room']
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("update room set room='"+room+"' where keyNumber='"+keyNumber+"'")
        cursor.execute("select * from clef where keyNumber='"+keyNumber+"'")
        keys = cursor.fetchall()
        conn.commit()
        return render_template('resultChangeKey.html', keys = keys, room = room)
    except:
        error = "This key could not be changed. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("changeKey"))


@app.route('/reportClient', methods = ['POST', 'GET'])
#The 1/2 step of
def reportClient():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from client")
    clients = cursor.fetchall()
    return render_template('reportClient.html', clients = clients)

@app.route('/resultReportClient', methods = ['POST', 'GET'])
#searh profile for one clinet
def resultReportClient():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from client where email='"+email+"';")
    client = cursor.fetchone()
    #lending
    cursor.execute("select l.keyNumber, l.copyNumber, r.address, cl.opens, l.lendDate, l.expectedReturnDate from room r, unlocks u, lent l, client c, clef cl where c.email='"+email+"' and l.email=c.email and l.keyNumber=cl.keyNumber and cl.keynumber=u.keyNumber and u.roomID = r.id and l.copyNumber=cl.copyNumber")
    lend = cursor.fetchall()
    #lost
    cursor.execute("select lo.keyNumber, lo.copyNumber, r.address, cl.opens, lo.lendDate, lo.lossDate from room r, unlocks u, losshistory lo, client c, clef cl where c.email='"+email+"' and lo.email=c.email and lo.keyNumber=cl.keyNumber and cl.keynumber=u.keyNumber and u.roomID = r.id and lo.copyNumber=cl.copyNumber")
    lost = cursor.fetchall()
    #return history
    cursor.execute("select re.keyNumber, re.copyNumber, r.address, cl.opens, re.lendDate, re.returnDate from room r, unlocks u, returnhistory re, client c, clef cl where c.email='"+email+"' and re.email=c.email and re.keyNumber=cl.keyNumber and cl.keynumber=u.keyNumber and u.roomID = r.id and re.copyNumber=cl.copyNumber")
    returnhistory = cursor.fetchall()
    return render_template('resultReportClient.html', client = client, lend = lend, lost = lost, returnhistory=returnhistory)

@app.route('/addClient', methods = ['POST', 'GET'])
#add new client
def addClient():
    if not session.get('logged_in'):
        abort(401)
    return render_template('addClient.html')

@app.route('/resultAddClient', methods = ['POST', 'GET'])
#add new client
def resultAddClient():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address = request.form['address']
    city = request.form['city']
    province = request.form['province']
    postcode = request.form['postcode']
    phoneNumber = request.form['phoneNumber']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user is not None:
        error = 'User with email {} is already registered.'.format(email)
        flash(error)
        return redirect(url_for('addClient'))

    else:
        try:
            cursor.execute("insert into client values('"+email+"', '"+firstName+"', '"+lastName+"', '"+address+"', '"+city+"', '"+province+"', '"+postcode+"', '"+phoneNumber+"')")
            cursor.execute("select * from client where email='"+email+"'")
            client = cursor.fetchone()
            conn.commit()
            return render_template('resultAddClient.html', client = client)
        except:
            error = "There was a problem adding this client. Please try again."
            flash(error)
            conn.rollback()
            return redirect(url_for("addClient"))

@app.route('/changeClient', methods = ['POST', 'GET'])
#add new client
def changeClient():
    if not session.get('logged_in'):
        abort(401)
    cursor = mysql.connect().cursor()
    cursor.execute("select * from client")
    clients = cursor.fetchall()
    return render_template('changeClient.html', clients = clients)

@app.route('/infoChangeClient', methods = ['POST', 'GET'])
#add new client
def infoChangeClient():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    cursor = mysql.connect().cursor()
    cursor.execute("select * from client where email='"+email+"'")
    client = cursor.fetchone()
    return render_template('infoChangeClient.html', client = client)

@app.route('/resultChangeClient', methods = ['POST', 'GET'])
#add new client
def resultChangeClient():
    if not session.get('logged_in'):
        abort(401)
    oldEmail = request.form['oldEmail']
    newEmail = request.form['newEmail']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address = request.form['address']
    city = request.form['city']
    province = request.form['province']
    postcode = request.form['postcode']
    phoneNumber = request.form['phoneNumber']
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("update client set email='"+newEmail+"', firstName='"+firstName+"', lastName='"+lastName+"', address='"+address+"', city='"+city+"', province='"+province+"', postcode='"+postcode+"', phoneNumber='"+phoneNumber+"' where email='"+oldEmail+"'")
        cursor.execute("select * from client where email='"+newEmail+"'")
        client = cursor.fetchone()
        conn.commit()
        return render_template('resultChangeClient.html', client = client)
    except:
        error = "There was a problem updating this client. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("changeClient"))


@app.route('/reportOffices', methods = ['POST', 'GET'])
def reportOffices():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select distinct keyNumber from clef")
    keys = cursor.fetchall()
    return render_template("reportOffices.html", keys = keys)

@app.route('/resultReportOffices', methods = ['POST', 'GET'])
#bureau
def resultReportOffices():
    if not session.get('logged_in'):
        abort(401)
    keyNumber = request.form['keyNumber']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select distinct r.room, c.opens from room r, clef c where c.keyNumber='"+keyNumber+"' and c.keyNumber=r.keyNumber;")
    offices = cursor.fetchall()
    return render_template('resultReportOffices.html', offices = offices, keyNumber = keyNumber)

@app.route('/addRoom', methods = ['POST', 'GET'])
#add a keyNumber-room relation-1
def addRoom():
    if not session.get('logged_in'):
        abort(401)
    return render_template('addRoom.html')

@app.route('/resultAddRoom', methods = ['POST', 'GET'])
#bureau
def resultAddRoom():
    if not session.get('logged_in'):
        abort(401)
    room = request.form['room']
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("insert into room (address) values(%s)", (room,))
        cursor.execute("SELECT DISTINCT keyNumber FROM clef WHERE active='yes'")
        keys = cursor.fetchall()
        cursor.execute("SELECT * FROM room WHERE address=%s", (room,))
        room = cursor.fetchone()
        conn.commit()
        return render_template('infoUpdateRoom.html', keys=keys, room=room)
    except:
        error = "There was a problem adding this room. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("addRoom"))

@app.route('/deleteRoom', methods = ['POST', 'GET'])
#bureau
def deleteRoom():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from room")
    rooms = cursor.fetchall()
    return render_template('deleteRoom.html', rooms = rooms)

@app.route('/infoDeleteRoom', methods = ['POST', 'GET'])
#bureau
def infoDeleteRoom():
    if not session.get('logged_in'):
        abort(401)
    room = request.form['room']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT keyNumber FROM unlocks WHERE roomID=%s", (int(room),))
    keys = cursor.fetchall()
    cursor.execute("SELECT * FROM room WHERE id=%s", (int(room),))
    room = cursor.fetchone()
    return render_template('infoDeleteRoom.html', room = room, keys = keys)

@app.route('/resultDeleteRoom', methods = ['POST', 'GET'])
#bureau
def resultDeleteRoom():
    if not session.get('logged_in'):
        abort(401)
    roomID = request.form['roomID']
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("delete from room where id = %s", (int(roomID),))
        conn.commit()
        message = "Room successfully deleted"
        flash(message)
    except:
        error = "There was a problem deleting this room."
        conn.rollback()
        flash(error)

    return redirect(url_for('deleteRoom'))

@app.route('/updateRoom', methods = ['POST', 'GET'])
#bureau
def updateRoom():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from room")
    rooms = cursor.fetchall()
    return render_template('updateRoom.html', rooms = rooms)

@app.route('/infoUpdateRoom', methods = ['POST', 'GET'])
#bureau
def infoUpdateRoom():
    if not session.get('logged_in'):
        abort(401)
    roomID = request.form['room']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM room WHERE id=%s", (roomID,))
    room = cursor.fetchone()
    cursor.execute("SELECT DISTINCT keyNumber FROM clef WHERE keyNumber NOT IN (SELECT keyNumber FROM unlocks WHERE roomID = %s) AND active='yes'", (int(roomID),))
    keys = cursor.fetchall()
    cursor.execute("SELECT DISTINCT keyNumber FROM unlocks WHERE roomID=%s", (int(roomID),))
    delete_keys = cursor.fetchall()
    return render_template('infoUpdateRoom.html', room = room, keys = keys, delete_keys = delete_keys)

@app.route('/resultUpdateRoom', methods = ['POST', 'GET'])
#bureau
def resultUpdateRoom():
    if not session.get('logged_in'):
        abort(401)
    keyNumbers = request.form.getlist('keys')
    deleteKeyNumbers = request.form.getlist('delete_keys')
    roomID = request.form['roomID']
    address = request.form['address']
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE room SET address=%s WHERE id=%s", (address, roomID))
    except:
        error = "There was a problem updating this room's name. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('updateRoom'))
    try:
        for keyNumber in keyNumbers:
            cursor.execute("INSERT INTO unlocks VALUES (%s, %s)", (str(keyNumber), int(roomID)))
    except:
        error = "There was a problem adding keys to this room. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('updateRoom'))
    try:
        for deleteKeyNumber in deleteKeyNumbers:
            cursor.execute("DELETE FROM unlocks WHERE keyNumber=%s AND roomID=%s", (str(deleteKeyNumber), int(roomID)))
    except:
        error = "There was a problem deleting keys from this room. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for('updateRoom'))

    cursor.execute("SELECT * FROM room WHERE id=%s", (roomID,))
    room = cursor.fetchone()
    cursor.execute("SELECT keyNumber, copyNumber, opens FROM clef WHERE keyNumber IN (SELECT keyNumber FROM unlocks WHERE roomID=%s)", (int(roomID),))
    keys = cursor.fetchall()
    conn.commit()
    return render_template('resultReportKeysbyRoom.html', room = room, keys = keys)



@app.route('/reportKey', methods=['POST', 'GET'])
#The 1/2 step of report by keyNumber, show all keyNumer and request a selection upon them.
def reportKey():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #pull all distict keyNumber from table clef
    cursor = mysql.connect().cursor()
    cursor.execute("select distinct keyNumber from clef;")
    keys = cursor.fetchall()
    #render html with all keynumbers
    return render_template('reportKey.html', keys = keys)

@app.route('/resultReportKey', methods=['POST', 'GET'])
#The 2/2 step of report by keyNumber, show 4 tables of keys
# in available, lending, missing, lost status respectivly
def resultReportKey():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get keyNumber form html form
    keyNumber = request.form['keyNumber']
    #pull copies of different status
    cursor = mysql.connect().cursor()
    #find out how many copies of those keys in total in the database
    cursor.execute("select count(*) from clef where keyNumber='"+keyNumber+"'")
    copyCount = cursor.fetchone()[0]

    cursor.execute("SELECT active FROM clef WHERE keyNumber=%s", (keyNumber,))
    active = cursor.fetchone()[0]

    #findo out what rooms it opens
    cursor.execute("select r1.address from room r1 join unlocks u1 on r1.id=u1.roomID where u1.keyNumber='"+keyNumber+"'")
    rooms = cursor.fetchall()
        #1.copyies status = available
    cursor.execute("select copyNumber, opens from clef where keyNumber='"+keyNumber+"' and status='available'")
    available = cursor.fetchall()
        #2.copies status = lend
    cursor.execute("select * from lent l, clef c where l.keyNumber='"+keyNumber+"' and l.keyNumber=c.keyNumber and l.copyNumber=c.copyNumber;")
    lend = cursor.fetchall()
        #3.copies status = lost
    cursor.execute("select * from losshistory lo, clef c where lo.keyNumber='"+keyNumber+"' and lo.keyNumber=c.keyNumber and c.copyNumber=lo.copyNumber ")
    lost = cursor.fetchall()
        #4.missing
    cursor.execute("select copyNumber, opens from clef where keyNumber='"+keyNumber+"' and status='missing'")
    missing = cursor.fetchall()
    #render html with key copy in status of lend, available, lost, and missing
    return render_template('resultReportKey.html', active=active, lend = lend, keyNumber = keyNumber, available = available, lost = lost, missing = missing, copyCount = copyCount, rooms=rooms)

@app.route('/reportKeysbyRoom', methods=['POST', 'GET'])
#The 1/2 step of report by room, display all rooms and request a selection upon them.
def reportKeysbyRoom():
    #chec if login session
    if not session.get('logged_in'):
        abort(401)
    #pull all distinct room from table room
    cursor = mysql.connect().cursor()
    cursor.execute("select * from room;")
    offices = cursor.fetchall()
    #render html with all rooms as options to be selected
    return render_template('reportKeysbyRoom.html', offices = offices)

@app.route('/resultReportKeysbyRoom', methods=['POST', 'GET'])
#The 2/2 step of report by room, showing all key copies binging to that room,
#	and what door each copy opens respectively
def resultReportKeysbyRoom():
    #check if login session
    if not session.get('logged_in'):
        abort(401)
    #get room from html form
    room = request.form['room']
    #pull all copies that opens that room, with its keyNumber and what door it opens(room door or mailbox)
    cursor = mysql.connect().cursor()
    cursor.execute("select c.keyNumber, c.copyNumber, c.opens from unlocks u JOIN clef c ON u.keyNumber=c.keyNumber WHERE u.roomID=%s", (int(room),))
    keys = cursor.fetchall()
    cursor.execute("select * from room where id = %s", (int(room),))
    room = cursor.fetchone()
    #render html with a table that shows records of keyNumber, copuNumber and what door it opens.
    return render_template('resultReportKeysbyRoom.html', keys=keys, room = room)

@app.route('/resultAllAdmins', methods = ['POST', 'GET'])
#show all admins
def resultAllAdmins():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    cursor.execute("select * from admin order by type;")
    admins = cursor.fetchall()
    return render_template('resultAllAdmins.html', admins = admins)

@app.route('/addAdmin', methods = ['POST', 'GET'])
#bureau
def addAdmin():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    return render_template('addAdmin.html')

@app.route('/resultAddAdmin', methods = ['POST', 'GET'])
#the inital status of an admin
#type == reguar as theres is only one hard-coded super admin===root
#status == active
#current == no
def resultAddAdmin():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user is not None:
        error = 'Admin with email {} is already registered.'.format(email)
        flash(error)
        return redirect(url_for("addAdmin"))
    else:
        try:
            cursor.execute("insert into admin values('"+email+"', '"+generate_password_hash(password)+"', '"+firstName+"', '"+lastName+"','regular','active', 'no')")
            cursor.execute("select * from admin where email='"+email+"'")
            admin = cursor.fetchone()
            conn.commit()
            return render_template('resultAddAdmin.html', admin=admin)
        except:
            error = "There was a problem adding this admin. Please try again."
            flash(error)
            conn.rollback()
            return redirect(url_for('addAdmin'))

@app.route('/activateAdmin', methods = ['POST', 'GET'])
#bureau
def activateAdmin():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    cursor.execute("select * from admin where type!='super' and status='deactivated'")
    admins = cursor.fetchall()
    return render_template('activateAdmin.html', admins = admins)

@app.route('/resultActivateAdmin', methods = ['POST', 'GET'])
#bureau
def resultActivateAdmin():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    #activate reguer user
    try:
        cursor.execute("update admin set status='active' where email='"+email+"'")
        cursor.execute("select * from admin;")
        admins = cursor.fetchall()
        #show all admins left as a result
        conn.commit()
        return render_template('resultAllAdmins.html', admins = admins)
    except:
        error = "There was a problem activating this admin. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("activateAdmin"))

@app.route('/deactivateAdmin', methods = ['POST', 'GET'])
#bureau
def deactivateAdmin():
    if not session.get('logged_in'):
        abort(401)
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    cursor.execute("select * from admin where type!='super' and status='active'")
    admins = cursor.fetchall()
    return render_template('deactivateAdmin.html', admins = admins)

@app.route('/resultDeactivateAdmin', methods = ['POST', 'GET'])
#bureau
def resultDeactivateAdmin():
    if not session.get('logged_in'):
        abort(401)
    email = request.form['email']
    conn = mysql.connect()
    cursor = conn.cursor()
    #check if user have the authority to access admin
    adminType = session['user'][4]
    if not adminType == 'super':
        return render_template("invalidPriority.html")
    try:
        cursor.execute("update admin set status='deactivated' where email='"+email+"'")
        cursor.execute("select * from admin;")
        admins = cursor.fetchall()
        #show all admins left as a result
        conn.commit()
        return render_template('resultAllAdmins.html', admins = admins)
    except:
        error = "There was a problem deactivating this admin. Please try again."
        flash(error)
        conn.rollback()
        return redirect(url_for("deactivateAdmin"))

@app.route('/signout')
#signout
def signout():
    session.pop('logged_in', None)
    session.pop('user', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    conn.commit()
    return redirect(url_for('signin'))

@app.route('/changepasswordhash', methods = ['GET'])
def changePasswordHash():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    try:
        for admin in admins:
            cursor.execute("UPDATE admin SET password = %s WHERE email = %s", (generate_password_hash(admin[1]), admin[0]))

        conn.commit()
    except:
        error = "There was a problem changing password hashes."
        flash(error)
        conn.rollback()
    return redirect(url_for('signin'))

@app.route('/getResetLink', methods = ['GET', 'POST'])
def getResetLink():
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == 'GET':
        return render_template('getResetLink.html')

    elif request.method == 'POST':
        email = request.form['email']
        cursor.execute('SELECT * FROM admin WHERE email=%s', (email,))
        admin = cursor.fetchone()
        if admin is None:
            error = "User with this email does not exist."
            flash(error)
            return redirect(url_for('getResetLink'))
        else:
            userinfo = [admin[0], admin[1]]
            token = serializer.dumps(userinfo)
            link = "testkey.csj.ualberta.ca:5000/resetPassword?token=" + token

            text = "Your password reset link is " + link

            msg = Message(subject="Password Reset for Testkey", recipients=[email], body=text)
            mail.send(msg)

            message = "Reset password sent"
            flash(message)
            return redirect(url_for('signin'))

@app.route('/resetPassword', methods = ['GET', 'POST'])
def resetPassword():

    if request.method == 'GET':
        token = request.args.get('token')
        try:
            userinfo = serializer.loads(token)
        except BadSignature:
            error = "Invalid reset link. Please try again."
            flash(error)
            redirect(url_for('signin'))
        except:
            error = "There was a problem loading reset page. Please try again."
            flash(error)
            redirect(url_for('signin'))

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE email=%s", (userinfo[0]))
        admin = cursor.fetchone()

        if admin is None:
            error = "User does not exist"
            flash(error)
            return redirect(url_for('signin'))
        elif userinfo[1] != admin[1]:
            error = "This password has already been changed."
            flash(error)
            return redirect(url_for('signin'))
        elif admin[5] == 'deactivated':
            error = "Account needs to be activated."
            flash(error)
            return redirect(url_for('signin'))
        else:
            return render_template('resetPassword.html', admin=admin)



    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE admin SET password = %s WHERE email = %s", (generate_password_hash(password), email))
            message = "Password successfully changed!"
            flash(message)
            conn.commit()
            return redirect(url_for('signin'))

        except:
            error = "There was a problem changing your password. Please try again."
            flash(error)
            return redirect(url_for('signin'))


@app.route('/changePassword', methods = ['GET', 'POST'])
def changePassword():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return render_template('changePassword.html')
    elif request.method == 'POST':
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        newPasswordConfirm = request.form['newPasswordConfirm']
        email = session['user'][0]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM admin WHERE email=%s', (email,))
        oldPasswordHash = cursor.fetchone()
        if not check_password_hash(oldPasswordHash[0], oldPassword):
            error = "Current password is incorrect. Please try again."
            flash(error)
            return redirect(url_for('changePassword'))
        elif str(newPassword) != str(newPasswordConfirm):
            error = "New passwords do not match. Please try again."
            flash(error)
            return redirect(url_for('changePassword'))
        elif (str(newPassword) == "") or (str(newPasswordConfirm) == ""):
            error = "Passwords cannot be empty. Please try again."
            flash(error)
            return redirect(url_for('changePassword'))
        else:
            newPasswordHash = generate_password_hash(newPassword)
            try:
                cursor.execute("UPDATE admin SET password=%s WHERE email=%s", (newPasswordHash, email))
                conn.commit()
                message = "Password successfully changed!"
                flash(message)
                return redirect(url_for('lend'))
            except:
                error = "There was a problem updating your password. Please try again."
                flash(error)
                conn.rollback()
                return redirect(url_for('changePassword'))


@app.route('/updateAdmin', methods = ['GET', 'POST'])
def updateAdmin():
    if not session.get('logged_in'):
        abort(401)
    elif getCurrentUser()[4] != "super":
        return render_template('invalidPriority.html')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()

        if request.method == 'GET':
            cursor.execute('SELECT firstName, lastName, email FROM admin')
            admins = cursor.fetchall()
            return render_template('updateAdmin.html', admins=admins)

        elif request.method == 'POST':
            email = request.form['admin']
            cursor.execute('SELECT * FROM admin WHERE email=%s', (email,))
            admin = cursor.fetchone()
            return render_template('infoUpdateAdmin.html', admin=admin)

@app.route('/infoUpdateAdmin', methods=['POST'])
def infoUpdateAdmin():
    if not session.get('logged_in'):
        abort(401)
    elif getCurrentUser()[4] != "super":
        return render_template('invalidPriority.html')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()

        if request.method == 'POST':
            oldEmail = request.form['oldEmail']
            email = request.form['email']
            firstName = request.form['firstName']
            lastName = request.form['lastName']

            try:
                cursor.execute('UPDATE admin SET email=%s, firstName = %s, lastName = %s WHERE email = %s', (email, firstName, lastName, oldEmail))
                conn.commit()
                message = "Admin updated."
                flash(message)
                return redirect(url_for('updateAdmin'))

            except:
                conn.rollback()
                error = "There was a problem updating this admin. Please try again."
                flash(error)
                return redirect(url_for('updateAdmin'))


@app.route('/activateClient', methods=['GET', 'POST'])
def activateClient():
    if not session.get('logged_in'):
        abort(401)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT * FROM client WHERE active='no'")
            clients = cursor.fetchall()
            return render_template('activateClient.html', clients=clients)
        elif request.method == 'POST':
            client = request.form['client']
            try:
                cursor.execute("UPDATE client SET active='yes' WHERE email=%s", (client,))
                conn.commit()
                message = 'Client successfully activated.'
                flash(message)
                return redirect(url_for('activateClient'))

            except:
                conn.rollback()
                error = 'There was a problem activating this client. Please try again.'
                flash(error)
                return redirect(url_for('activateClient'))

@app.route('/deactivateClient', methods = ['GET', 'POST'])
def deactivateClient():




#app running function
if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
    #app.run()




