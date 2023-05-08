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
from cryptography.fernet import Fernet

import cryptography
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
PSApp.config['MYSQL_DB'] = 'psiconnection'
PSApp.config['MYSQL_CURSORCLASS'] = 'DictCursor'
PSApp.config['UPLOAD_FOLDER'] = './static/img/'
PSApp.config['UPLOAD_FOLDER_PDF'] = './static/pdf/'
PSApp.config['MAIL_SERVER'] = 'smtp.gmail.com'
PSApp.config['MAIL_USERNAME'] = 'psi.connection09@gmail.com'
PSApp.config['MAIL_PASSWORD'] = 'togieyicxqyzseil'
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




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~ Sistema de Cifrado ~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def encriptado():
    selectoken      =   mysql.connection.cursor()
    selectoken.execute("SELECT clave FROM token")
    cl              =   selectoken.fetchone()

    # SE CONVIERTE DE TUPLE A DICT
    clave   =   cl.get('clave')

    # SE CONVIERTE DE DICT A STR
    clave   =   str(clave)

    # SE CONVIERTE DE STR A BYTE
    clave   = clave.encode('utf-8')

    # SE CREA LA CLASE FERNET
    cifrado = Fernet(clave)

    return cifrado




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~ CRUD Administradores ~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#~~~~~~~~~~~~~~~~~~~ Crear Administradores ~~~~~~~~~~~~~~~~~~~#
@PSApp.route('/CrearCuentaAdmin', methods=["GET", "POST"])
def crearCuentaAdmin():
    if request.method == 'POST':

        #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
        encriptar = encriptado()

        # SE RECIBE LA INFORMACION
        nombreAd        = request.form['nombreAd'].encode('utf-8')
        nombreAdCC      = encriptar.encrypt(nombreAd)

        apellidoPAd     = request.form['apellidoPAd'].encode('utf-8')
        apellidoPAdCC   = encriptar.encrypt(apellidoPAd)

        apellidoMAd     = request.form['apellidoMAd'].encode('utf-8')
        apellidoMAdCC   = encriptar.encrypt(apellidoMAd)

        # CONFIRMAR CORREO CON LA BD
        correoAd        = request.form['correoAd'].encode('utf-8')

        print("````````````````````````````````")
        print(correoAd)
        print(type(correoAd))
        correoAdCC      = encriptar.encrypt(correoAd)

        contraAd        = request.form['contraAd'].encode('utf-8')
        contraAdCC      = encriptar.encrypt(contraAd)

        # FUNCION QUE CREA EL CODIGO DE SGURIDAD // CREAR FUNCION APARTE

        import random
        let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"

        gen = f"{let}{num}"
        lon = 8
        ran = random.sample(gen, lon)
        cod = "".join(ran)

        codVeriAd   = cod
        activoAd    = 1
        veriAd      = 2
        priviAd     = 1

        regAdmin = mysql.connection.cursor()
        regAdmin.execute("INSERT INTO admin (nombreAd, apellidoPAd, apellidoMAd, correoAd, contraAd, codVeriAd, activoAd, veriAd, priviAd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (nombreAdCC, apellidoPAdCC, apellidoMAdCC, correoAdCC, contraAdCC, codVeriAd, activoAd, veriAd, priviAd))
        mysql.connection.commit()

        # MANDAR CORREO CON CODIGO DE VERIRIFICACION
        idAd                = regAdmin.lastrowid
        print(idAd)
        selAd               = mysql.connection.cursor()
        selAd.execute("SELECT * FROM admin WHERE idAd=%s",(idAd,))
        ad                  = selAd.fetchall()
        
        # SE CREA UNA LISTA
        datosAd = []

        # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 

        for admin in ad:
            # SELECCIONA Y DECODIFICA EL NOMBRE
            nombr = admin.get('nombreAd')
            nombr = encriptar.decrypt(nombr)
            nombr = nombr.decode()

            # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
            apelp = admin.get('apellidoPAd')
            apelp = encriptar.decrypt(apelp)
            apelp = apelp.decode()
            
            # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
            apelm = admin.get('apellidoMAd')
            apelm = encriptar.decrypt(apelm)
            apelm = apelm.decode()

            # SELECCIONA Y DECODIFICA EL CORREO
            corre = admin.get('correoAd')
            corre = encriptar.decrypt(corre)
            corre = corre.decode()

            # SE AGREGA A UN DICCIONARIO
            noAd = {'nombreAd': nombr, 'apellidoPAd': apelp, 'apellidoMAd': apelm, 'correoAd': corre}

            # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
            admin.update(noAd)

            # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
            datosAd.append(admin)
        
        # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
        datosAd = tuple(datosAd)

        print(datosAd)
        
        msg                 = Message("CODIGO DE VERIFICACION", sender=PSApp.config['MAIL_USERNAME'], recipients=[correoAd.decode()] )
        msg.html            = render_template('codigoVerificacion.html', datosAd = datosAd)

        print(type(correoAd))
        mail.send(msg)

        flash('Cuenta creada con exito.')

        #MANDAR A UNA VENTANA PARA QUE META EL CODIGO DE VERFICIACION
        return redirect(url_for('verAdministrador'))
    else:
        flash('No se que poner')
        return render_template('index.html')



#~~~~~~~~~~~~~~~~~~~ Ver Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PSApp.route('/VerAdministrador', methods=['GET', 'POST'])
def verAdministrador():

    # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
    encriptar = encriptado()

    # SE SELECCIONA TODOS LOS DATOS DE LA BD
    selecAdmin      =   mysql.connection.cursor()
    selecAdmin.execute("SELECT * FROM admin WHERE activoAd IS NOT NULL")
    ad              =   selecAdmin.fetchall()

    # SE CREA UNA LISTA
    datosAd = []

    # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 

    for admin in ad:
        # SELECCIONA Y DECODIFICA EL NOMBRE
        nombr = admin.get('nombreAd')
        nombr = encriptar.decrypt(nombr)
        nombr = nombr.decode()

        # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
        apelp = admin.get('apellidoPAd')
        apelp = encriptar.decrypt(apelp)
        apelp = apelp.decode()
        
        # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
        apelm = admin.get('apellidoMAd')
        apelm = encriptar.decrypt(apelm)
        apelm = apelm.decode()

        # SELECCIONA Y DECODIFICA EL CORREO
        corre = admin.get('correoAd')
        corre = encriptar.decrypt(corre)
        corre = corre.decode()

        # SE AGREGA A UN DICCIONARIO
        noAd = {'nombreAd': nombr, 'apellidoPAd': apelp, 'apellidoMAd': apelm, 'correoAd': corre}

        # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
        admin.update(noAd)

        # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
        datosAd.append(admin)
    
    # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
    datosAd = tuple(datosAd)

    return render_template('verAdministrador.html', admin = ad, datosAd = datosAd)
    


#~~~~~~~~~~~~~~~~~~~ Editar Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PSApp.route('/EditarCuentaAdmin', methods=["GET", "POST"])
def editarCuentaAdmin():
    idAd            = request.form['idAd']
    nombreAd        = request.form['nombreAd']
    apellidoPAd     = request.form['apellidoPAd']
    apellidoMAd     = request.form['apellidoMAd']
    correoAd        = request.form['correoAd']
    editarAdmin     = mysql.connection.cursor()
    editarAdmin.execute("UPDATE admin set nombreAd=%s, apellidoPAd=%s, apellidoMAd=%s, correoAd=%s WHERE idAd=%s",
                        (nombreAd, apellidoPAd, apellidoMAd, correoAd, idAd,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verAdministrador'))



#~~~~~~~~~~~~~~~~~~~ Eliminar Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PSApp.route('/EliminarCuentaAdmin', methods=["GET", "POST"])
def eliminarCuentaAdmin():
    idAd            = request.form['idAd']
    activoAd        = None
    regPaciente = mysql.connection.cursor()
    regPaciente.execute("UPDATE admin set activoAd=%s WHERE idAd=%s",
                        (activoAd, idAd,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verAdministrador'))




if __name__ == '__main__':
    PSApp.secret_key = '123'
    PSApp.register_error_handler(401, status_401)
    PSApp.register_error_handler(404, status_404)
    PSApp.run(port=3000, debug=True)
