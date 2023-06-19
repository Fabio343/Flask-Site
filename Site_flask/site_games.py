from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import re


app = Flask(__name__,template_folder='templates', static_folder='static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '****@343'
app.config['MYSQL_DB'] = '***'

mysql = MySQL(app)

app.secret_key = 'your secret key'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def aboutpage():
    return render_template("About.html")

@app.route("/contato")
def contatopage():
    return render_template("formulario.html")


@app.route("/save_data", methods=['POST', 'GET'])
def save_db():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        message = request.form['message']
        cursor = mysql.connection.cursor()
        cursor.execute("insert into ****(name, last_name, email, message) VALUES(%s,%s,%s,%s)", (name, last_name, email, message))
        mysql.connection.commit()
        cursor.close()
    return render_template("save_base.html")


@app.route("/results")
def results():
    cursor = mysql.connection.cursor()
    cursor.execute("select name,message from ****")
    joblist = cursor.fetchall()
    cursor.close()
    return render_template("result.html",joblist=joblist)


@app.route("/research", methods=['GET', 'POST'])
def research():
    if request.method == "POST" and "name" in request.form:
        name = request.form['name']
        cursor = mysql.connection.cursor()
        cursor.execute("select name, message from ***** where name= %s", [name])
        joblist = cursor.fetchall()
        cursor.close()
        return render_template("research.html",joblist=joblist)


@app.route("/needforspeed")
def need():
    return render_template("need_for_speed.html")


@app.route("/resident")
def resident(): return render_template("resident.html")


@app.route("/yugioh")
def yugioh(): return render_template("yugioh.html")


@app.route("/random_forest")
def random_forest(): return render_template("Random_Forest.html")


@app.route("/regression")
def regression(): return render_template("regression.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id,name,email FROM *** WHERE name = % s AND password = % s', (name, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = list(account)[0]
            session['name'] = list(account)[1]
            session['email'] = list(account)[2]
            msg = 'Logged in successfully !'
            return render_template('profile_page.html', msg=msg)
        else:
            msg = 'Incorrect name / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM *** WHERE name = %s', (name,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO *** VALUES (NULL, %s, %s, %s)', (name, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route('/change_user_update')
def change_user():
    return render_template('change_user.html')


@app.route('/change_password_update')
def change_password():
    return render_template('change_password.html')


@app.route('/change_email_update')
def change_email():
    return render_template('change_email.html')


@app.route('/change_user_update', methods=['GET', 'POST'])
def change_user_update():
    if request.method == 'POST' and 'name' in request.form and 'newUserConfirmation' in request.form:
        new_user = request.form['name']
        new_user_confirm = request.form['newUserConfirmation']
        if new_user != new_user_confirm:
            return render_template('change_user.html', msg='Username is not Correct')
        else:
            user_id = session["id"]
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE **** SET name=%s where id=%s', (new_user, user_id))
            mysql.connection.commit()
    return render_template('login.html', msg='Username Changed')


@app.route('/change_password_update', methods=['GET', 'POST'])
def change_password_update():
    if request.method == 'POST' and 'Password' in request.form and 'newPasswordConfirmation' in request.form:
        new_password = request.form['Password']
        new_password_confirm = request.form['newPasswordConfirmation']
        if new_password != new_password_confirm:
            return render_template('change_password.html', msg='Password is not Correct')
        else:
            user_id = session["id"]
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE **** SET password=%s where id=%s', (new_password, user_id))
            mysql.connection.commit()
    return render_template('login.html.html', msg='Password Changed')


@app.route('/change_email_update', methods=['GET', 'POST'])
def change_email_update():
    if request.method == 'POST' and 'email' in request.form and 'newemailConfirmation' in request.form:
        new_email = request.form['email']
        new_email_confirm = request.form['newemailConfirmation']
        if new_email != new_email_confirm:
            return render_template('change_email.html', msg='Email is not Correct')
        else:
            user_id = session["id"]
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE **** SET email=%s where id=%s', (new_email, user_id))
            mysql.connection.commit()
    return render_template('login.html.html', msg='E-mail Changed')


if __name__ == "__main__":
    app.run(debug=True)
