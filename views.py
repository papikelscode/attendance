from flask import Blueprint,request,jsonify,render_template, url_for, flash
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
from models import attendance,luggage,users,db,visitor,Articles
from datetime import date, datetime, time
from flask_login import login_required, login_user, logout_user, current_user
from random import randint
from mailer import EmailSender
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from requests import post

ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}

basedir = os.path.abspath(os.path.dirname((__file__)))
picFolder = './static/userspic'
picDB = os.path.join(basedir,picFolder)

def SendSms(body,recipients):
    payload = {
        'email':'dspirit118@gmail.com',
        'password':'Abdulkereem22',
        'message':body,
        'sender_name':'ITF',
        'recipients':str(234)+recipients
    }
    resp = post('https://app.multitexter.com/v2/app/sms',data=payload)
    print(resp.text)
    return resp.text

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


mailSent = EmailSender()

main = Blueprint('endpoint', __name__)

@main.route('/')
def index():
    posts = Articles.query.all()
    return render_template('index.html',posts=posts)

@main.route('/signupstaff')
def signupstaff():
    return render_template('auth/signup.html')


@main.route('/clockin',methods=['POST'])
def clockin():
    data = request.json
    checkUser= users.query.filter_by(IDnumber=data['idnumber']).first()
    try:
        check_attendtoday = attendance.query.filter_by(users_id=checkUser.id).first()
        if check_attendtoday.timein.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'):
            print('today')
            return jsonify({'status': 400,'msg':'sorry you have clocked in today'})
    except AttributeError:
        if checkUser:
            new_attendance = attendance(users_id=checkUser.id)
            db.session.add(new_attendance)
            db.session.commit()
            return jsonify({'status': 200,'msg':'user clocked in'})
        return jsonify ({'status':404, 'msg': 'user not found'})


@main.route('/post/<id>')
def postx(id):
    article = Articles.query.filter_by(id=id).first()
    return render_template('post.html',article=article)


@main.route('/clockout',methods=['PUT'])
def clockout():
    data = request.json
    user = users.query.filter_by(IDnumber=data['idnumber']).first()
    updateAttend = attendance.query.filter_by(users_id=user.id).first()
    print(updateAttend.timein)
    if updateAttend.timein.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'):
        updateAttend.timeout = datetime.now()
        db.session.commit()
        return jsonify({'status':200,'msg':'clock out done!!!' })
    return jsonify({'status':400, 'msg':'something went wrong!!!'})









@main.route('/createUser', methods=['POST'])
def createUser():
    try:
        data = request.form
        if 'pic' not in request.files:
            flash("Your passport is requred to complete your registration",'is-danger')
            return redirect(url_for('endpoint.signupstaff'))

        pic = request.files['pic']    

        if  pic.filename == '':
            flash("No file selected",'is-danger')
            return redirect(url_for('endpoint.signupstaff'))
            

        if  pic and allowed_file(pic.filename):
            file = secure_filename(pic.filename)
            pic.save(os.path.join(picDB,file))
            hashedPassword = generate_password_hash(data['password'],method='sha256')
            new_user = users(first_name=data['fname'],
                                    last_name=data['lname'],
                                    phone=data['phone'],
                                    email=data['email'],
                                    password=hashedPassword,
                                    IDnumber=data['idnumber'],
                                    picture=pic.filename,
                                    is_staff=True)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Welcome to your dashboard, your registation is completed",'is-success')
            return redirect(url_for('endpoint.dashboard'))   
        flash("File extension not allowed",'is-danger')
        return redirect(url_for('endpoint.signupstaff'))
    except IntegrityError:
        flash("User already exist",'is-danger')
        return redirect(url_for('endpoint.signupstaff'))
    except Exception as e:
        flash(str(e),'is-danger')
        return redirect(url_for('endpoint.signupstaff'))


        

        
        



@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('endpoint.dashboard'))
    if request.method == 'POST':
        data = request.json
        user = users.query.filter_by(IDnumber=data['idnumber']).first()
        if user:
            if check_password_hash(user.password,data['password']):
               login_user(user,remember=True)
               return jsonify ({'status':200,'msg':'user authenticated'})
            return jsonify({'status':404,'msg':'invalid password'})
        return jsonify({'status':404,'msg':'user not found'})
    return render_template ('auth/login.html')



@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('endpoint.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    user_attendance  = attendance.query.filter_by(users_id= current_user.id).all()
    total_attendance = attendance.query.filter_by(users_id=current_user.id).count()

    timein  = db.session.query(attendance).filter_by(users_id=current_user.id, timein=attendance.timein).count()
    timeout = db.session.query(attendance).filter_by(users_id=current_user.id, timeout=attendance.timeout).count()

    total_visitor = visitor.query.filter_by(invitedDate = str(datetime.now().strftime('%Y-%m-%d'))).count()  
    current_visitor = visitor.query.filter_by(active=True).count()
    unavail = visitor.query.filter(visitor.timeout !=None).count()
    expected_visitors = visitor.query.filter_by(timein=None).count()
    myinvites = visitor.query.filter_by(invited_by=current_user.id).all()

    #role = 
    return render_template('dashboard/dashboard.html',
                                                    user_attendance=user_attendance,
                                                    total_attendance=total_attendance,
                                                    timein=timein,
                                                    timeout=timeout,
                                                    total_visitor=total_visitor,
                                                    current_visitor=current_visitor,
                                                    unavail=unavail,
                                                    expected_visitors=expected_visitors,
                                                    myinvites=myinvites)                                                





@main.route('/clockvisitor/<invitecode>')
def clockvisitor(invitecode):
    print(invitecode)
    vistr = visitor.query.filter_by(inviteCode=invitecode).first()
    if vistr.timein != None:
        vistr.active = False
        vistr.timeout = datetime.now()
        db.session.commit()
        return jsonify({'status':200})
    vistr.timein = datetime.now()
    vistr.active = True
    db.session.commit()
    return jsonify({'status':200})





@main.route('/invite', methods=['GET','POST'])
def invite():
    if request.method == 'POST':
        inviteid = randint(35635,49848)
        inviteCode = "ITF"+str(inviteid)
        data = request.json
        new_visitor = visitor(first_name = data['fname'],
                                         last_name=data['lname'], 
                                         phone=data['phone'],
                                         email=data['email'],
                                         inviteCode =inviteCode,
                                         invited_by=current_user.id,
                                         invitedDate=str(datetime.now().strftime('%Y-%m-%d')))
        mailSent.subject = "Invitation to ITF"
        mailSent.recipient = data['email']
        mailSent.msgbody = "You are invited to ITF  MSTC Abuja, your invite code"+inviteCode
        response = mailSent.send()
        SendSms("You are invited to ITF MSTC Abuja, your invite code " +inviteCode,data['phone'])
        db.session.add(new_visitor)
        if response:
            db.session.commit() 
            return jsonify({"status":200, 'msg':'Done'})   
        db.session.rollback()
        return jsonify({"status":500, 'msg':"sorry we couldnt send invitation code"})                 

    myinvites = visitor.query.filter_by(invited_by=current_user.id).all()
    return render_template('dashboard/invite.html', myinvites=myinvites)

@main.route('/additem',methods=['POST'])
def additem():
    data = request.json
    print(data)
    guest = visitor.query.filter_by(inviteCode=data['invitecode']).first()
    if guest:
        newItem = luggage(item_name=data['itemname'],visitors_id=guest.id)
        db.session.add(newItem)
        db.session.commit()
        return jsonify({'status':200})
    return jsonify({'status':'404'})

@main.route('/visitorsitem/<visitorID>')
def Visitor(visitorID):
    itm = luggage.query.filter_by(visitors_id=visitorID).all()
    return render_template('components/itemstable.html',itm=itm)  



@main.route('/settings')
def settings():
    return render_template('auth/settings.html')


@main.route('/password',methods=['POST'])
def changepassword():
    data = request.json
    if data['password'] == data['conpassword']:
        checkpword = check_password_hash(current_user.password,data['currentpassword'])
        if checkpword:
            newpassword = generate_password_hash(data['password'],method='sha256')
            current_user.password = newpassword
            db.session.commit()
            return jsonify({'status':'200'})
        return jsonify({'status':'400'})
    return jsonify({'status':'404'})



@main.route('/database')
def database():
    db.drop_all()
    db.create_all()
    return 'database created'  