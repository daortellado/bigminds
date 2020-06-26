from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from functools import wraps
from flask_apscheduler import APScheduler
import os
import secrets

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import datetime

from sqlalchemy import func

app = Flask(__name__)

socketio = SocketIO(app)

app.debug = True

app.config['SECRET_KEY'] = 'xZxM5GMQ37CQw9kf6SRS33LadZTpSKt6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
database = SQLAlchemy(app)

from forms import LoginForm, TimeForm, AppSettingsForm, MediaFileUploadForm, ApptForm
from models import Instance, Message, Channel, EduSchedu, ClassNotiQueue, User, ApptNotiQueue, ApptSchedu
import events

# # config
# app.config.update(
#     DEBUG = True,
#     SECRET_KEY = 'secret_xxx'
# )

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
# class User(UserMixin):

#     def __init__(self, id):
#         self.id = id
#         self.name = "user" + str(id)
#         self.password = self.name + "_secret"
        
#     def __repr__(self):
#         return "%d/%s/%s" % (self.id, self.name, self.password)

#role check function

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "Admin":
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('not_admin'))
    return wrap

# create some users with ids 1 to 20       
# users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/', methods=['GET', 'POST'])
@login_required
def page():
    eduschedu = EduSchedu.query.first()
    apptschedu = ApptSchedu.query.first()
    userenroll = User.query.first()
    instance = Instance.query.first()
    image_file = url_for('static', filename=f'media/{instance.media_file}')
    messages = Message.query.order_by(Message.id.desc()).all()
    channels = Channel.query.order_by(Channel.id.desc()).all()
    notifications = ClassNotiQueue.query.order_by(ClassNotiQueue.id.desc()).all()
    appointments = ApptNotiQueue.query.order_by(ApptNotiQueue.id.desc()).all()
    room_name = 'home'
    # classenroll = userenroll.enrolled.all()[-1].classname
    appt_form = ApptForm(prefix='appt_form')
    if appt_form.validate_on_submit():
        apptschedu = ApptSchedu(teacher = str(appt_form.user_list.data), time = appt_form.time.data, dow = appt_form.dow.data, zoomlink = "zoom.com")
        database.session.add(apptschedu)
        usertest = User.query.first()
        apptscheduler = ApptSchedu.query.order_by(ApptSchedu.id.desc()).first()
        apptscheduler.apptstudents.append(usertest)
        database.session.commit()
        flash('Appointment Scheduled!', 'info')
        return redirect(url_for('page'))
    return render_template('home.html', title=instance.homepage_title, room=room_name,
                           messages=messages, channels=channels, notifications=notifications, appointments=appointments, chat_enabled = instance.chat_enabled,
                           current_user=current_user, appt_form=appt_form)

# time=eduschedu.time, dow=eduschedu.dow, classname=eduschedu.classname, zoomlink=eduschedu.zoomlink, appt_form=appt_form, appttime=apptschedu.time, apptdow=apptschedu.dow, teacher=apptschedu.teacher, apptzoomlink=apptschedu.zoomlink, classenroll=classenroll

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_page():
    time_form = TimeForm(prefix='time_form')
    monThings = EduSchedu.query.filter(EduSchedu.dow==0).order_by(EduSchedu.time.asc()).all()
    tueThings = EduSchedu.query.filter(EduSchedu.dow==1).order_by(EduSchedu.time.asc()).all()
    wedThings = EduSchedu.query.filter(EduSchedu.dow==2).order_by(EduSchedu.time.asc()).all()
    thuThings = EduSchedu.query.filter(EduSchedu.dow==3).order_by(EduSchedu.time.asc()).all()
    friThings = EduSchedu.query.filter(EduSchedu.dow==4).order_by(EduSchedu.time.asc()).all()
    satThings = EduSchedu.query.filter(EduSchedu.dow==5).order_by(EduSchedu.time.asc()).all()
    sunThings = EduSchedu.query.filter(EduSchedu.dow==6).order_by(EduSchedu.time.asc()).all()

    if time_form.validate_on_submit():
        eduschedu = EduSchedu(classname = time_form.classname.data, time = time_form.time.data, dow = time_form.dow.data, zoomlink = time_form.zoomlink.data)
        database.session.add(eduschedu)
        database.session.commit()
        flash('Class Updated!', 'info')
        if time_form.enroll.data == True:
            print('sup')
            usertest = User.query.first()
            eduscheduler = EduSchedu.query.order_by(EduSchedu.id.desc()).first()
            eduscheduler.students.append(usertest)
            database.session.commit()
        return redirect(url_for('admin_page'))

    return render_template('admin_page.html', time_form=time_form, monThings=monThings, tueThings=tueThings, wedThings=wedThings, thuThings=thuThings, friThings=friThings, satThings=satThings, sunThings=sunThings)

@app.route('/not_admin')
def not_admin():
    return render_template('not_admin.html')

@app.route('/admin/reset-comments', methods=['GET'])
def reset_comments():
    Message.query.delete()
    Channel.query.delete()
    database.session.commit()
    flash('Chat cleared!', 'info')
    return redirect(url_for('admin_page'))

@app.route('/admin/reset-views', methods=['GET'])
def reset_views():
    EduSchedu.query.delete()
    ApptSchedu.query.delete()
    ClassNotiQueue.query.delete()
    ApptNotiQueue.query.delete()
    database.session.commit()
    flash('Classes, Appointments and Notifcations cleared!', 'info')
    return redirect(url_for('admin_page'))
 
# somewhere to login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']        
#         if password == username + "_secret":
#             id = username.split('user')[1]
#             user = User(id)
#             login_user(user)
#             return redirect(request.args.get("next"))
#         else:
#             return abort(401)
#     else:
#         return Response('''
#         <h2>You must log in:</h2>
#         <div class="form-group">
#         <form action="" method="post">
#             <p><input type=text name=username class="form-control">
#             <p><input type=password name=password class="form-control">
#             <p><input type=submit value=Login>
#         </form>
#         </div>
#         ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('page'))  # Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('page'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login.jinja2',
                           form=form,
                           title='Log in.',
                           template='login-page',
                           body="Log in with your User account.")


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
# @login_manager.user_loader
# def load_user(userid):
#     return User(userid)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

#drop test record
# database.session.query(EduSchedu).filter(EduSchedu.id==1).delete()
# database.session.commit()

#adding test row

# newEdu = EduSchedu(id = 1,
#                     time = datetime.time(21,7), dow = 2, classname = 'art',
#                     zoomlink = 'google.com')

# database.session.add(newEdu)   
# database.session.commit()

# adding test user

# newUser = User(id = 2,
#                     name = 'notadmin', email = 'notadmin',
#                     role = '', password = 'notadmin')

# database.session.add(newUser)   
# database.session.commit()

# JOB/shutdown proc

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def class_noti(link):
    noti_object = ClassNotiQueue(linkcont=link.zoomlink, now=datetime.datetime.now().strftime("%H:%M"), nameclass = link.classname)
    database.session.add(noti_object)
    database.session.commit()
    json_data_noti = {
        'nameclass' : link.classname,
        'linkcont' : link.zoomlink,
        'now' : datetime.datetime.now().strftime("%H:%M")
    }
    socketio.emit('noti', json_data_noti)

def appt_noti(apptlink):
    appt_object = ApptNotiQueue(linkcont=apptlink.zoomlink, now=datetime.datetime.now().strftime("%H:%M"), teacher = apptlink.teacher)
    database.session.add(appt_object)
    database.session.commit()
    json_data_apptnoti = {
        'teacher' : apptlink.teacher,
        'linkcont' : apptlink.zoomlink,
        'now' : datetime.datetime.now().strftime("%H:%M")
    }
    socketio.emit('apptnoti', json_data_apptnoti)

# def job_function():
#     link = EduSchedu.query.first()
#     if link.datetime == 'blue':
#         print(link.zoomlink)
#         class_noti(link)
def job_function():
    link = EduSchedu.query.all()
    apptlink = ApptSchedu.query.all()
    today = int(datetime.datetime.now().weekday())
    nowtime = str(datetime.datetime.now().strftime("%H:%M:00"))
    for i in range(len(link)):
        print(link[i].time)
        print(nowtime)
        print(today)
        print(link[i].dow)
        if link[i].dow == today and str(link[i].time) == nowtime:
            print(link[i].zoomlink)
            class_noti(link[i])
    for i in range(len(apptlink)):
        print(apptlink[i].time)
        print(nowtime)
        print(today)
        print(apptlink[i].dow)
        if apptlink[i].dow == today and str(apptlink[i].time) == nowtime:
            print(apptlink[i].zoomlink)
            appt_noti(apptlink[i])

#test relationship
# usertest = User.query.first()
# eduscheduler = EduSchedu.query.first()
# eduscheduler.students.append(usertest)
# database.session.commit()

@socketio.on('username')
def senduser():
    usernametosend = current_user.name
    instance = Instance.query.first()
    instance.page_views += 1
    database.session.commit()
    print(usernametosend)
    socketio.emit('username', usernametosend)

scheduler = APScheduler()
scheduler.add_job(func=job_function, trigger='cron', hour='0-23', minute='0-59', id='1', day_of_week='0-6')
scheduler.start()

if __name__ == "__main__":
    socketio.run(app)