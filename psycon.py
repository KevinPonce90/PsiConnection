from ast import If
from threading import activeCount
from time import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mysqldb import MySQL, MySQLdb
from flask_mail import Mail, Message
from flask_bcrypt import bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, login_manager
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import date, datetime
import base64
import pdfkit
import os
import random

PSApp = Flask(__name__)
mysql = MySQL(PSApp)
csrf = CSRFProtect()
PSApp.config['MYSQL_HOST'] = 'localhost'
PSApp.config['MYSQL_USER'] = 'root'
PSApp.config['MYSQL_PASSWORD'] = 'mysql'
PSApp.config['MYSQL_DB'] = 'psyconnection'
PSApp.config['MYSQL_CURSORCLASS'] = 'DictCursor'
PSApp.config['UPLOAD_FOLDER'] = './static/img/'
PSApp.config['UPLOAD_FOLDER_PDF'] = './static/pdf/'
PSApp.config['MAIL_SERVER'] = 'smtp.gmail.com'
PSApp.config['MAIL_USERNAME'] = ''
PSApp.config['MAIL_PASSWORD'] = ''
PSApp.config['MAIL_PORT'] = 587
PSApp.config['MAIL_USE_TLS'] = True
PSApp.config['MAIL_USE_SSL'] = False
PSApp.config['MAIL_ASCII_ATTACHMENTS'] = True
mail = Mail(PSApp)
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ]
}


@PSApp.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM admin WHERE correoAd=%s", [email])
        if result > 0: #PONER EN ESTE IF UN ELSE O IF ELSE PARA QUE SI NO ES ADMINUISTRADOR SE TOME LA INFO DE PACIENTE.
            data = cur.fetchone()
            if bcrypt.hashpw(password1, data['passAd'].encode('utf-8')) == data['passAd'].encode('utf-8'):
                session["login"]    = True
                session['idAd']     = data['idAd']
                session['userid']   = data['priviAd']
                session['name']     = data['nombreAd']
                attempt = session.get('attempt')
                attempt = 5
                session['attempt'] = attempt
                flash("Inicio de Sesion exitoso", 'success')
                cur.close()
                return redirect(url_for('home'))
            else:
                attempt = session.get('attempt')
                attempt = attempt - 1
                session['attempt'] = attempt
                flash("Contraseña incorrecta", 'danger')
                if attempt == 1:
                    flash(
                        'Es tu ultimo intento, tendras que contactar a un desarrollador, Intento %d de 5' % attempt, 'error')
                else:
                    flash('Inicio De Sesion Invalido, Intento: %d de 5' %
                          attempt, 'error')
        else:
            attempt = session.get('attempt')
            attempt = attempt - 1
            session['attempt'] = attempt
            flash("Email incorrecto", 'danger')
            if attempt == 1:
                flash(
                    'Es tu ultimo intento, tendras que contactar a un desarrollador, Intento %d de 5' % attempt, 'error')
            else:
                flash('Inicio De Sesion Invalido, Intento: %d de 5' %
                      attempt, 'error')
            # return redirect('/pythonlogin/')

    return render_template('login.html', intentos=session['attempt'])

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users


@PSApp.route('/')
def home():
    session['attempt'] = 5
    # Check if user is loggedin
    if 'login' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['name'], role=session['userid'])
    if session['attempt'] >= 1:
        return redirect(url_for('login'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page


@PSApp.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('login', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('idAd', None)
    session.pop('name', None)
    # Redirect to login page
    return redirect(url_for('login'))


@PSApp.route('/index')
def index():
    # Check if user is loggedin
    if 'login' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['name'], role=session['userid'])
    if session['attempt'] >= 1:
        return redirect(url_for('login'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@PSApp.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Pagina no encontrada </h1>", 404


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~ CRUD Administradores ~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~ CRUD Pacientes ~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# ~~~~~~~~~~~~~~~~~~~ Crear Pacientes ~~~~~~~~~~~~~~~~~~~#
@PSApp.route('/CrearCuenta', methods=["GET", "POST"])
def crearCuenta():
    if request.method == 'POST':
        # SE RECIBE LA INFORMACION
        fechaNacPaci = request.form['fechaNacPaci'].encode('utf-8')
        fechaNacPaciCC = bcrypt.hashpw(fechaNacPaci, bcrypt.gensalt())

        nombrePaci = request.form['nombrePaci'].encode('utf-8')
        nombrePaciCC = bcrypt.hashpw(nombrePaci, bcrypt.gensalt())

        apellidoPPaci = request.form['apellidoPPaci'].encode('utf-8')
        apellidoPPaciCC = bcrypt.hashpw(apellidoPPaci, bcrypt.gensalt())

        apellidoMPaci = request.form['apellidoMPaci'].encode('utf-8')
        apellidoMPaciCC = bcrypt.hashpw(apellidoMPaci, bcrypt.gensalt())

        # CONFIRMAR CORREO CON LA BD
        correoPaci = request.form['correoPaci'].encode('utf-8')
        correoPaciCC = bcrypt.hashpw(correoPaci, bcrypt.gensalt())

        sexoPaci = request.form['sexoPaci'].encode('utf-8')
        sexoPaciCC = bcrypt.hashpw(sexoPaci, bcrypt.gensalt())

        contraPaci = request.form['contraPaci'].encode('utf-8')
        contraPaciCC = bcrypt.hashpw(contraPaci, bcrypt.gensalt())

        # FUNCION QUE CREA EL CODIGO DE SGURIDAD

        import random
        let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"

        gen = f"{let}{num}"
        lon = 8
        ran = random.sample(gen, lon)
        cod = "".join(ran)

        codVeriPaci = cod
        activoPaci = 1
        veriPaci = 2

        regPaciente = mysql.connection.cursor()
        regPaciente.execute("INSERT INTO paciente (fechaNacPaci, nombrePaci, apellidoPPaci, apellidoMPaci, correoPaci, sexoPaci, contraPaci, codVeriPaci, activoPaci, veriPaci) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (fechaNacPaciCC, nombrePaciCC, apellidoPPaciCC, apellidoMPaciCC, correoPaciCC, sexoPaciCC, contraPaciCC, codVeriPaci, activoPaci, veriPaci))
        mysql.connection.commit()

        # MANDAR CORREO CON CODIGO DE VERIRIFICACION

        flash('Cuenta creada con exito.')

        #MANDAR A UNA VENTANA PARA QUE META EL CODIGO DE VERFICIACION
        return redirect(url_for('confirmaCodigo'))
    else:
        flash('No se que poner')
        return render_template('index.html')


if __name__ == '__main__':
    PSApp.secret_key = 'suq2v,Y\=+BRGZgJT.#CaS3['
    csrf.init_app(PSApp)
    PSApp.register_error_handler(401, status_401)
    PSApp.register_error_handler(404, status_404)
    PSApp.run(port=3000, debug=True)
