from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ragon'
app.config['MYSQL_DB'] = 'navigus'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/meeting/<string:id>/')
def meeting(id):
    
    cur = mysql.connection.cursor()

  
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    meeting = cur.fetchone()

    return render_template('meeting.html', meeting=meeting)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

       
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password_candidate = request.form['password']

        
        cur = mysql.connection.cursor()

        
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            
            data = cur.fetchone()
            password = data['password']

          
            if sha256_crypt.verify(password_candidate, password):
              
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
 
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM meetings WHERE user = %s", [session['username']])

    meetings = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', meetings=meetings)
    else:
        msg = 'No Meeting Created'
        return render_template('dashboard.html', msg=msg)
 
    cur.close()
    


class MeetingForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    day = StringField('Day', [validators.Length(min=1, max=40)])
    month = StringField('Month', [validators.Length(min=1, max=20)])
    time = StringField('Time', [validators.Length(min=1, max=10)])

class JoinForm(Form):
    organiser = StringField('Organiser', [validators.Length(min=1, max=200)])

# Join Meetings
@app.route('/join_meetings', methods=['GET', 'POST'])
@is_logged_in
def join_meetings():
    form = JoinForm(request.form)
    return render_template('join_meetings.html', form=form)    

@app.route('/add_meetings', methods=['GET', 'POST'])
@is_logged_in
def add_meetings():
    form = MeetingForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        day = form.day.data
        month = form.month.data
        time= form.time.data

        cur = mysql.connection.cursor()    
        cur.execute("INSERT INTO meetings(title, Day, month, time, user) VALUES(%s, %s, %s, %s, %s)",(title, day, month, time, session['username']))
        mysql.connection.commit()
        cur.close()

        flash('Meeting Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_meetings.html', form=form)



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
