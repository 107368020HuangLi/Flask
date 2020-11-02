from flask import render_template, flash,redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db
from app.models import User, Up, Down
from app.forms import RegisterForm, LoginForm, Upform, Downform
from datetime import datetime
import pymysql

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form_Up = Upform()

    if form_Up.validate_on_submit():
        nowtime = datetime.utcnow()
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        theTime = nowtime.strftime(ISOTIMEFORMAT)
        the_user_id = current_user.id
        input = Up(timestamp=theTime, user_id=the_user_id)
        db.session.add(input)
        db.session.commit()
        flash("Up SUCCESS", category='info')
        return redirect(url_for('down'))
    return render_template('index.html', form= form_Up)

@app.route('/down', methods=['GET', 'POST'])
@login_required
def down():
    form_down = Downform()

    if form_down.validate_on_submit():
        down_nowtime = datetime.utcnow()
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        down_theTime = down_nowtime.strftime(ISOTIMEFORMAT)
        up_id = Up.query.filter_by(user_id=current_user.id).order_by(Up.timestamp.desc()).first()
        final_up_id = up_id.id
        down_input = Down(downtime=down_theTime, up_id=final_up_id)
        db.session.add(down_input)
        db.session.commit()
        flash("Down SUCCESS", category='info')
        return redirect(url_for('logout'))
    return render_template('index.html', form=form_down)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username= username, password= password)
        db.session.add(user)
        db.session.commit()
        flash('GOOD. Register SUCCESS' , category="success")
        return redirect( url_for('index') )
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        #check
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('login successful', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return  redirect(next_page)
            return redirect( url_for('index') )
        flash('user is not exist', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('login'))


@app.route('/databord')
def databord():
    if current_user.is_authenticated:
        sql = "SELECT user.username, up.timestamp, down.downtime FROM user cross JOIN up, down " \
                "WHERE user.id=up.user_id AND up.id=down.up_id  AND user.id=" + str(current_user.id)
        query = db.engine.execute(sql)
        content = query.fetchall()
    return render_template('databord.html', content=content)