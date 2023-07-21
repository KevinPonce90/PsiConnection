from __future__ import print_function

from ast                    import If
from threading              import activeCount
from time                   import time
from flask                  import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mysqldb          import MySQL, MySQLdb
from flask_mail             import Mail, Message
from flask_bcrypt           import bcrypt,Bcrypt
from flask_login            import LoginManager, login_user, logout_user, login_required, login_manager
from flask_wtf.csrf         import CSRFProtect
from functools              import wraps
from werkzeug.utils         import secure_filename
from datetime               import date, datetime, timedelta
from cryptography.fernet    import Fernet

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import cryptography
import base64
import pdfkit
import os
import random
import secrets
import re
import math
import random
import datetime
import os.path

PCapp                                   = Flask(__name__)
mysql                                   = MySQL(PCapp)
csrf=CSRFProtect()
PCapp.config['MYSQL_HOST']              = 'localhost'
PCapp.config['MYSQL_USER']              = 'root'
PCapp.config['MYSQL_PASSWORD']          = 'mysql'
PCapp.config['MYSQL_DB']                = 'psiconnection'
PCapp.config['MYSQL_CURSORCLASS']       = 'DictCursor'
PCapp.config['UPLOAD_FOLDER']           = './static/img/'
PCapp.config['UPLOAD_FOLDER_PDF']       = './static/pdf/'


PCapp.config['MAIL_SERVER']='smtp.gmail.com'
PCapp.config['MAIL_PORT'] = 465
PCapp.config['MAIL_USERNAME'] = 'psi.connection09@gmail.com'
PCapp.config['MAIL_PASSWORD'] = 'PASSWORD'
PCapp.config['MAIL_USE_TLS'] = False
PCapp.config['MAIL_USE_SSL'] = True
mail = Mail(PCapp)

bcryptObj = Bcrypt(PCapp)

# GOOGLE
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

def verified_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Asumiendo que el estado de verificación se guarda en la sesión del usuario
        if 'verificado' not in session or not session['verificado']:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
        return f(*args, **kwargs)
    return decorated_function

#El Def auth controla si inicia sesion o es nuevo usuario

@PCapp.route('/pythonlogin/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        encriptar = encriptado()
        action = request.form['action']
        if action == 'login':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM paciente WHERE correoPaci=%s AND (activoPaci = %s OR veriPaci = %s) AND activoPaci IS NOT NULL", [email, 1, 0,])
            if result > 0:
                data = cur.fetchone()
                if bcrypt.checkpw(password, data['contraPaci'].encode('utf-8')):
                        #Falta agregar sessions ( los adecuados )
                        #FALTA AGREGAR QUE SI NO ESTA ACTIVO NO PUEDE ENTRAR
                        session["login"] = True
                        session['loginPaci'] = True                  
                        session['idPaci'] = data['idPaci']
                        nombre = data.get('nombrePaci')
                        name = nombre.encode()
                        name = encriptar.decrypt(name)
                        name = name.decode()                           
                        session['name'] = name
                        session['correoPaci'] = data['correoPaci']
                        session['verificado'] = data['veriPaci']
                        flash("Inicio de Sesión exitoso", 'success')
                        cur.close()
                        return redirect(url_for('indexPacientes'))
                else:
                    flash("Contraseña incorrecta", 'danger')
            else:
                
                result = cur.execute("SELECT * FROM practicante WHERE correoPrac=%s AND (activoPrac = %s OR veriPrac = %s) AND activoPrac IS NOT NULL", [email, 1, 1,])
                if result > 0:
                    data = cur.fetchone()
                    if bcrypt.checkpw(password, data['contraPrac'].encode('utf-8')):
                            #Falta agregar sessions ( los adecuados )
                            session["login"] = True
                            session['loginPrac'] = True 
                            session['idPrac'] = data['idPrac']
                            session['correoPrac'] = data['correoPrac']
                            nombre = data.get('nombrePrac')
                            name = nombre.encode()
                            name = encriptar.decrypt(name)
                            name = name.decode()                           
                            session['name'] = name
                            
                            
                            session['verificado'] = data['veriPrac']
                            flash("Inicio de Sesión exitoso", 'success')
                            cur.close()
                            return redirect(url_for('indexPracticantes'))
                    else:
                        flash("Contraseña incorrecta", 'danger')
                else:
                    result = cur.execute("SELECT * FROM supervisor WHERE correoSup=%s AND (activoSup = %s OR veriSup = %s) AND activoSup IS NOT NULL", [email, 1, 1,])
                    if result > 0:
                        data = cur.fetchone()
                        if bcrypt.checkpw(password, data['contraSup'].encode('utf-8')):
                                #Falta agregar sessions ( los adecuados )                                
                                session["login"] = True
                                session['loginSup'] = True 
                                session['idSup'] = data['idSup']
                                session['correoSup'] = data['correoSup']
                                nombre = data.get('nombreSup')
                                name = nombre.encode()
                                name = encriptar.decrypt(name)
                                name = name.decode()                           
                                session['name'] = name
                                
                                
                                session['verificado'] = data['veriSup']
                                flash("Inicio de Sesión exitoso", 'success')
                                cur.close()
                                return redirect(url_for('verPracticantesSupervisor'))
                        else:
                            flash("Contraseña incorrecta", 'danger')
                    else:
                        result = cur.execute("SELECT * FROM admin WHERE correoAd=%s AND (activoAd = %s OR veriAd = %s) AND activoAd IS NOT NULL", [email, 1, 1,])
                        if result > 0:
                            data = cur.fetchone()
                            if bcrypt.checkpw(password, data['contraAd'].encode('utf-8')):
                                    #Falta agregar sessions ( los adecuados )                                    
                                    session["login"] = True
                                    session['loginAdmin'] = True 
                                    session['idAd'] = data['idAd']
                                    nombre = data.get('nombreAd')
                                    name = nombre.encode()
                                    name = encriptar.decrypt(name)
                                    name = name.decode()                           
                                    session['name'] = name
                                    
                                    session['correoAd'] = data['correoAd']
                                    print(session['correoAd'])
                                    print(session)
                                    session['verificado'] = data['veriAd']
                                    flash("Inicio de Sesión exitoso", 'success')
                                    cur.close()
                                    return redirect(url_for('indexAdministrador'))
                            else:
                                flash("Contraseña incorrecta", 'danger')
                        else:
                           flash("Email no registrado", 'danger')
                
        #Registro
        elif action == 'register':
            #Falta Hacer HASH a toda la informacion personal del usuario
            #Validar el nombre
            name = request.form['name']
            if len(name.strip()) == 0:
                flash("Por favor ingrese su nombre completo", 'danger')
                return redirect(url_for('auth'))
            
            
            apellidop = request.form['apellidop']
            #Validar el apellido paterno
            if len(apellidop.strip()) == 0:
                flash("Porfavor ingrese su Apellido Paterno", 'danger')
                return redirect(url_for('auth'))
            
            
            apellidom = request.form['apellidom']
            #validar el apellido materno
            if len(apellidom.strip()) == 0:
                flash("Porfavor ingrese su Apellido Materno", 'danger')
                return redirect(url_for('auth'))   
                  
                      
            genero = request.form['gender']
            #Validar el genero
            if len(genero.strip()) == 0:
                flash("Porfavor ingrese su genero", 'danger')
                return redirect(url_for('auth'))
            
            fechaNacPaci = request.form['fecha_nacimiento']
            #Validar la edad
            if len(fechaNacPaci.strip()) == 0:
                flash("Porfavor ingrese su edad", 'danger')
                return redirect(url_for('auth'))
            
            email = request.form['email']
             # Validar el correo electrónico
            if len(email.strip()) == 0:
                flash("Por favor ingrese su correo electrónico", 'danger')
                return redirect(url_for('auth'))
            
            if not re.match(r'^[^\s@]+@(udg\.com\.mx|alumnos\.udg\.mx|academicos\.udg\.mx)$', email):
                # Si el correo electrónico no es válido, mostrar un mensaje de error
                flash("Por favor ingrese un correo electrónico válido con uno de los dominios permitidos", 'danger')
                return redirect(url_for('auth'))
            
            
            
            fechaActual     = date.today()
            fechaNacimiento = datetime.datetime.strptime(fechaNacPaci, '%Y-%m-%d')
            fechaNac = fechaNacimiento.date()
            edad = fechaActual - fechaNac

            edad = edad.days
            edad = edad/365
            edad = math.floor(edad)
            
            password = request.form['password']
            passwordCon = request.form['passwordCon']

            if password != passwordCon:
                flash("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.", 'danger')
                return redirect(url_for('auth'))

            if not re.search(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+|}{":?><,./;\'\[\]])[A-Za-z\d!@#$%^&*()_+|}{":?><,./;\'\[\]]{8,}$', password):
                flash("La contraseña debe tener al menos 8 caracteres, una mayúscula y un carácter especial (. ? { } [ ] ; , ! # $ @ % ” ’)", 'danger')
                return redirect(url_for('auth'))

            hashed_password = bcryptObj.generate_password_hash(password).decode('utf-8')

            # Verificar si el correo ya está registrado en la base de datos
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM paciente WHERE correoPaci=%s AND activoPaci IS NOT NULL", [email,])
            if result > 0:
                # Si el correo ya está registrado, mostrar un mensaje de error
                flash("El correo ya está registrado", 'danger')
                cur.close()
                return redirect(url_for('auth'))
            
            
            # Generar un código de verificación aleatorio
            #verification_code = secrets.token_hex(3)
            
            # FUNCION QUE CREA EL CODIGO DE SGURIDAD // CREAR FUNCION APARTE
            let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            num = "0123456789"

            gen = f"{let}{num}"
            lon = 8
            ran = random.sample(gen, lon)
            cod = "".join(ran)
            verification_code = cod
            
            name = name.encode('utf-8')
            name = encriptar.encrypt(name)
            
            apellidop = apellidop.encode('utf-8')
            apellidop = encriptar.encrypt(apellidop)
            
            apellidom = apellidom.encode('utf-8')
            apellidom = encriptar.encrypt(apellidom)
                        
            
            
            cur = mysql.connection.cursor()            
            # Guardar el usuario y el código de verificación en la base de datos
            cur.execute("INSERT INTO paciente(fechaNacPaci, nombrePaci, apellidoPPaci , apellidoMPaci, correoPaci, sexoPaci, contraPaci, codVeriPaci, activoPaci, veriPaci, edadPaci) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (fechaNacPaci, name, apellidop, apellidom, email, genero, hashed_password, verification_code, 0, 0, edad))
            
            
            mysql.connection.commit()

            
            # MANDAR CORREO CON CODIGO DE VERIRIFICACION
            idPaci                = cur.lastrowid
            print(idPaci)
            selPaci               = mysql.connection.cursor()
            selPaci.execute("SELECT nombrePaci FROM paciente WHERE idPaci=%s",(idPaci,))
            ad                  = selPaci.fetchone()
            
            
            nombre = ad.get('nombrePaci')
            name = nombre.encode()
            name = encriptar.decrypt(name)
            name = name.decode()            
            
            # Enviar el código de verificación por correo electrónico
            msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[email])
            msg.body = render_template('layoutmail.html', name=name ,  verification_code=verification_code)
            msg.html = render_template('layoutmail.html', name=name ,  verification_code=verification_code)
            mail.send(msg)
            
            flash("Revisa tu correo electrónico para ver los pasos para completar tu registro!", 'success')
            return redirect(url_for('verify'))

    return render_template('login.html')

@PCapp.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'login' in session:
        if session['verificado'] == 2:
            return redirect(url_for('home'))
        else:
            if request.method == 'POST':
                flash("Revisa tu correo electrónico para obtener tu código de verificación", 'success')
                # Obtener el código ingresado por el usuario
                user_code = request.form['code']
                
                # Verificar si el código es correcto
                cur = mysql.connection.cursor()
                result = cur.execute("SELECT * FROM paciente WHERE codVeriPaci=%s", [user_code])
                if result > 0:
                    
                    # Si el código es correcto, actualizar el campo "verificado" a 1
                    cur.execute("UPDATE paciente SET veriPaci = %s, activoPaci = %s WHERE codVeriPaci = %s", (2, 1, user_code))
                    mysql.connection.commit()
                    flash("Registro completado con éxito", 'success')
                    cur.close()
                    session.clear()
                    return redirect(url_for('auth'))
                else:
                    result = cur.execute("SELECT * FROM practicante WHERE codVeriPrac=%s", [user_code])
                    if result > 0:                    
                        # Si el código es correcto, actualizar el campo "verificado" a 2
                        cur.execute("UPDATE practicante SET veriPrac = %s, activoPrac = %s WHERE codVeriPrac = %s", (2, 1, user_code))
                        mysql.connection.commit()
                        cur.close()
                        session.clear()
                        flash("Registro completado con éxito", 'success')
                        return redirect(url_for('auth'))
                    else:
                        result = cur.execute("SELECT * FROM supervisor WHERE codVeriSup=%s", [user_code])
                        if result > 0:
                        
                            # Si el código es correcto, actualizar el campo "verificado" a 2
                            cur.execute("UPDATE supervisor SET veriSup = %s, activoSup = %s WHERE codVeriSup = %s", (2, 1, user_code))
                            mysql.connection.commit()
                            flash("Registro completado con éxito", 'success')
                            cur.close()
                            session.clear()
                            return redirect(url_for('auth'))
                        else:
                            result = cur.execute("SELECT * FROM admin WHERE codVeriAd=%s", [user_code])
                            if result > 0:
                            
                                # Si el código es correcto, actualizar el campo "verificado" a 2
                                cur.execute("UPDATE admin SET veriAd = %s, activoAd = %s WHERE codVeriAd = %s", (2, 1, user_code))
                                mysql.connection.commit()
                                flash("Registro completado con éxito", 'success')
                                cur.close()
                                session.clear()
                                return redirect(url_for('auth'))
                            else:
                                flash("Código de verificación incorrecto", 'danger')
                                cur.close()        
            return render_template('verify.html')  
    else:
        return redirect(url_for('auth'))  


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


################### - Crear Cuenta administradores - ###########################
@PCapp.route('/CrearCuentaAdmin', methods=["GET", "POST"])
def crearCuentaAdmin():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:
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
                    correoAd        = request.form['correoAd']

                    contraAd        = request.form['contraAd']
                    
                    hashed_password = bcryptObj.generate_password_hash(contraAd).decode('utf-8')

                    # FUNCION QUE CREA EL CODIGO DE SGURIDAD // CREAR FUNCION APARTE
                    let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    num = "0123456789"

                    gen = f"{let}{num}"
                    lon = 8
                    ran = random.sample(gen, lon)
                    cod = "".join(ran)

                    codVeriAd   = cod
                    activoAd    = 0
                    veriAd      = 1
                    priviAd     = 1
                    
                    # Verificar si el correo ya está registrado en la base de datos
                    cur = mysql.connection.cursor()
                    result = cur.execute("SELECT * FROM admin WHERE correoAd=%s AND activoAd IS NOT NULL", [correoAd,])
                    if result > 0:
                        # Si el correo ya está registrado, mostrar un mensaje de error
                        flash("El correo ya está registrado", 'danger')
                        cur.close()
                        return redirect(url_for('verAdministrador'))

                    regAdmin = mysql.connection.cursor()
                    regAdmin.execute("INSERT INTO admin (nombreAd, apellidoPAd, apellidoMAd, correoAd, contraAd, codVeriAd, activoAd, veriAd, priviAd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                        (nombreAdCC, apellidoPAdCC, apellidoMAdCC, correoAd, hashed_password, codVeriAd, activoAd, veriAd, priviAd))
                    mysql.connection.commit()

                    # MANDAR CORREO CON CODIGO DE VERIRIFICACION
                    idAd                = regAdmin.lastrowid
                    
                    selAd               = mysql.connection.cursor()
                    selAd.execute("SELECT nombreAd FROM admin WHERE idAd=%s",(idAd,))
                    ad                  = selAd.fetchone()
                    


                    nombr = ad.get('nombreAd')
                    nombr = nombr.encode()
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()

                    
                    # SE MANDA EL CORREO
                    msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[correoAd])
                    msg.body = render_template('layoutmail.html', name=nombr, verification_code=codVeriAd)
                    msg.html = render_template('layoutmail.html', name=nombr, verification_code=codVeriAd)
                    mail.send(msg)
                    

                    flash("Revisa tu correo electrónico para ver los pasos para completar tu registro!", 'success')        
                    #MANDAR A UNA VENTANA PARA QUE META EL CODIGO DE VERFICIACION
                    return redirect(url_for('verAdministrador'))
                else:
                    flash("Error al crear la cuenta", 'danger')
                    return redirect(url_for('verAdministrador'))  
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))

    
#~~~~~~~~~~~~~~~~~~~ Ver Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerAdministrador', methods=['GET', 'POST'])
def verAdministrador():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:
                    
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

                        # SE AGREGA A UN DICCIONARIO
                        noAd = {'nombreAd': nombr, 'apellidoPAd': apelp, 'apellidoMAd': apelm}

                        # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                        admin.update(noAd)

                        # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                        datosAd.append(admin)
                    
                    # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                    datosAd = tuple(datosAd)

                    return render_template('adm_adm.html', admin = ad, datosAd = datosAd, username=session['name'], email=session['correoAd'])    
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


#~~~~~~~~~~~~~~~~~~~ Eliminar Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaAdmin', methods=["GET", "POST"])
def eliminarCuentaAdmin():
    idAd            = request.form['idAd']
    activoAd        = None
    regPaciente = mysql.connection.cursor()
    regPaciente.execute("UPDATE admin set activoAd=%s WHERE idAd=%s",
                        (activoAd, idAd,))
    mysql.connection.commit()
    flash('Cuenta eliminada con exito.')
    return redirect(url_for('verAdministrador'))


#~~~~~~~~~~~~~~~~~~~ Editar Adminsitradores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaAdmin', methods=["GET", "POST"])
def editarCuentaAdmin():

    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()

    # SE RECIBE LA INFORMACION
    nombreAd        = request.form['nombreAd'].encode('utf-8')
    nombreAdCC      = encriptar.encrypt(nombreAd)

    apellidoPAd     = request.form['apellidoPAd'].encode('utf-8')
    apellidoPAdCC   = encriptar.encrypt(apellidoPAd)

    apellidoMAd     = request.form['apellidoMAd'].encode('utf-8')
    apellidoMAdCC   = encriptar.encrypt(apellidoMAd)


    idAd            = request.form['idAd']
    editarAdmin     = mysql.connection.cursor()
    editarAdmin.execute("UPDATE admin set nombreAd=%s, apellidoPAd=%s, apellidoMAd=%s WHERE idAd=%s",
                        (nombreAdCC, apellidoPAdCC, apellidoMAdCC, idAd,))
    mysql.connection.commit()

    flash('Cuenta editada con exito.')
    return redirect(url_for('verAdministrador'))
    

#~~~~~~~~~~~~~~~~~~~ Index Pacientes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/indexPacientes', methods=['GET', 'POST'])
def indexPacientes():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginPaci' in session:
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # USAR EL SESSION PARA OBTENER EL ID DEL PACIENTE
                idPaci = session['idPaci']


                # FALTA PROBAR ESTO
                selecCita       =   mysql.connection.cursor()
                selecCita.execute("SELECT * FROM citas C INNER JOIN practicante PR ON C.idCitaPrac = PR.idPrac INNER JOIN paciente PA ON C.idCitaPaci = PA.idPaci WHERE idCitaPaci=%s AND estatusCita=%s",(idPaci,1))
                cit              =   selecCita.fetchone()

                if cit is not None:
                    fechaCita = cit.get('fechaCita')
                    horaCita = cit.get('horaCita')
                    # Formatear la fecha como una cadena
                    fechaCita = fechaCita.strftime('%Y-%m-%d')
                    # Crear un objeto datetime arbitrario para usar como referencia
                    ref = datetime.datetime(2000, 1, 1)
                    # Sumar el timedelta al datetime para obtener otro datetime
                    horaCita = ref + horaCita
                    # Formatear la hora como una cadena
                    horaCita = horaCita.strftime('%H:%M:%S')
                    fechaCita = datetime.datetime.strptime(fechaCita, '%Y-%m-%d').date()

                    # Convertir la cadena de hora a objeto datetime
                    horaCita = datetime.datetime.strptime(horaCita, '%H:%M:%S').time()
                    # Obtener la fecha y hora actual
                    fecha_actual = datetime.datetime.now().date()
                    hora_actual = datetime.datetime.now().time()

                    # Sumar una hora a la hora de la cita
                    horaCita_fin = (datetime.datetime.combine(datetime.date.today(), horaCita) +
                                    datetime.timedelta(hours=1)).time()

                    # Combinar la fecha actual con la hora actual
                    fecha_hora_actual = datetime.datetime.combine(fecha_actual, hora_actual)

                    # Combinar la fecha de la cita con la hora de finalización de la cita
                    fecha_hora_fin_cita = datetime.datetime.combine(fechaCita, horaCita_fin)
                    # Comparar la fecha y hora actual con la fecha y hora de finalización de la cita
                    if fecha_hora_actual >= fecha_hora_fin_cita:
                        citaRealizada = 1
                        print("La cita ya ha pasado.")
                    else:
                        citaRealizada = 2
                        print("La cita aún no ha pasado.")
                
                else:
                    citaRealizada = 1

                # FALTA PROBAR ESTO
                selecCita       =   mysql.connection.cursor()
                selecCita.execute("SELECT * FROM citas C INNER JOIN practicante PR ON C.idCitaPrac = PR.idPrac INNER JOIN paciente PA ON C.idCitaPaci = PA.idPaci WHERE idCitaPaci= %s",(idPaci,))
                hc              =   selecCita.fetchall()

                # SE CREA UNA LISTA
                datosCitas      =   []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 
                for cita in hc:
                    
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrPA = cita.get('nombrePaci')
                    nombrPA = encriptar.decrypt(nombrPA)
                    nombrPA = nombrPA.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPA = cita.get('apellidoPPaci')
                    apelpPA = encriptar.decrypt(apelpPA)
                    apelpPA = apelpPA.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPA = cita.get('apellidoMPaci')
                    apelmPA = encriptar.decrypt(apelmPA)
                    apelmPA = apelmPA.decode()


                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrPR = cita.get('nombrePrac')
                    nombrPR = encriptar.decrypt(nombrPR)
                    nombrPR = nombrPR.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPR = cita.get('apellidoPPrac')
                    apelpPR = encriptar.decrypt(apelpPR)
                    apelpPR = apelpPR.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPR = cita.get('apellidoMPrac')
                    apelmPR = encriptar.decrypt(apelmPR)
                    apelmPR = apelmPR.decode()


                    # SE AGREGA A UN DICCIONARIO
                    noCita = {'nombrePaci': nombrPA, 'apellidoPPaci': apelpPA, 'apellidoMPaci': apelmPA,  'nombrePrac': nombrPR, 'apellidoPPrac': apelpPR, 'apellidoMPrac': apelmPR}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    cita.update(noCita)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosCitas.append(cita)
                
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosCitas = tuple(datosCitas)

                return render_template('index_pacientes.html', hc = hc, datosCitas = datosCitas, cit = cit, citaRealizada = citaRealizada, username=session['name'], email=session['correoPaci'])
            
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Verifica tu correo electrónico para poder iniciar sesión", 'danger')
            return redirect(url_for('verify'))
    else:
        flash("Inicia sesión para continuar", 'danger')
        return redirect(url_for('auth'))


# ~~~~~~~~~~~~~~~~~~~ Ver Pacientes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerPacientes', methods=['GET', 'POST'])
def verPacientes():
    # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
    encriptar = encriptado()


    # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
    selecPaci       =   mysql.connection.cursor()
    selecPaci.execute("SELECT * FROM paciente WHERE activoPaci IS NOT NULL")
    pac             =   selecPaci.fetchall()


    # SE CREA UNA LISTA
    datosPaci = []


    # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
    for paci in pac:
    
        # SELECCIONA Y DECODIFICA EL NOMBRE
        nombr = paci.get('nombrePaci')
        nombr = encriptar.decrypt(nombr)
        nombr = nombr.decode()


        # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
        apelp = paci.get('apellidoPPaci')
        apelp = encriptar.decrypt(apelp)
        apelp = apelp.decode()
    
        # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
        apelm = paci.get('apellidoMPaci')
        apelm = encriptar.decrypt(apelm)
        apelm = apelm.decode()



        # SE AGREGA A UN DICCIONARIO
        noPaci = {'nombrePaci': nombr, 'apellidoPPaci': apelp, 'apellidoMPaci': apelm}


        # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
        paci.update(noPaci)


        # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
        datosPaci.append(paci)

    # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
    datosPaci = tuple(datosPaci)


    return render_template('verPaciente.html', paci = pac, datosPaci = datosPaci)



@PCapp.route('/VerPacientesAdm', methods=['GET', 'POST'])
def verPacientesAdm():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecPaci       =   mysql.connection.cursor()
                selecPaci.execute("SELECT * FROM paciente WHERE activoPaci IS NOT NULL")
                pac             =   selecPaci.fetchall()

                # SE CREA UNA LISTA
                datosPaci = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
                for paci in pac:
                
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = paci.get('nombrePaci')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = paci.get('apellidoPPaci')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = paci.get('apellidoMPaci')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()

                    # SE AGREGA A UN DICCIONARIO
                    noPaci = {'nombrePaci': nombr, 'apellidoPPaci': apelp, 'apellidoMPaci': apelm}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    paci.update(noPaci)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPaci.append(paci)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPaci = tuple(datosPaci)


                return render_template('adm_pacie.html', paci = pac, datosPaci = datosPaci, username=session['name'], email=session['correoAd'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))

@PCapp.route('/CrearCita', methods=["GET", "POST"])
def crearCita():

        let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"

        gen = f"{let}{num}"
        lon = 8
        ran = random.sample(gen, lon)
        cod = "".join(ran)
        requestCOD = cod

        # USO SESION PARA OBTENER LOS DATOS DEL PACIENTE
        idPaci      = session['idPaci']
        correoPaci  = session['correoPaci']
        
        # RECUPERAR DATOS
        idPrac      = request.form['idPrac']
        correoPrac  = request.form['correoPrac']
        tipoCita    = request.form['tipoCita']
        fechaCita   = request.form['fechaCita']
        horaCita    = request.form['horaCita']

        # HACER FORMATO ESPECIFICO FECHAS
        fecha_hora = datetime.datetime.strptime(f'{fechaCita} {horaCita}', '%Y-%m-%d %H:%M')

        if tipoCita == "Presencial":
            direCita = "Modulo X"
        else:
            direCita = "Virtual"
        
        estatusCita = 1

        if direCita == "Modulo X":

            """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                service = build('calendar', 'v3', credentials=creds)

                event = {
                    'summary': 'Cita - Psiconnection',
                    'location': direCita+' - Tipo: '+tipoCita,
                    'description': 'Cita con un psicologo de Psiconnection',
                    'status': 'confirmed',
                    'sendUpdates': 'all',
                    'start': {
                        'dateTime': fecha_hora.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'end': {
                        'dateTime': (fecha_hora + datetime.timedelta(hours=1)).isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=1'
                    ],
                    'attendees': [
                        {'email': correoPrac},
                        {'email': correoPaci}
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }

                event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
                print("Event created: %s" % (event.get('htmlLink')))
                eventoId = event["id"]

                print(eventoId)

                editarPaciente      = mysql.connection.cursor()
                editarPaciente.execute("UPDATE paciente SET citaActPaci=%s WHERE idPaci=%s",
                            (estatusCita, idPaci,))
                mysql.connection.commit()

                editarPracticante   = mysql.connection.cursor()
                editarPracticante.execute("UPDATE practicante SET estatusCitaPrac=%s WHERE idPrac=%s",
                            (estatusCita, idPrac,))
                mysql.connection.commit()

                regCita = mysql.connection.cursor()
                regCita.execute("INSERT INTO citas (tipo, correoCitaPra, correoCitaPac, direCita, fechaCita, horaCita, estatusCita, eventoId, idCitaPrac, idCitaPaci) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (tipoCita, correoPrac, correoPaci, direCita, fechaCita, horaCita, estatusCita, eventoId, idPrac, idPaci))
                mysql.connection.commit()
                


                flash('Cita editada con exito.')
                return redirect(url_for('indexPacientes'))


            except HttpError as error:
                print('An error occurred: %s' % error)
        else:

            """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                service = build('calendar', 'v3', credentials=creds)

                event = {
                    'summary': 'Cita - Psiconnection',
                    'location': direCita+' - Tipo: '+tipoCita,
                    'description': 'Cita con un psicologo de Psiconnection',
                    'status': 'confirmed',
                    'sendUpdates': 'all',
                    'start': {
                        'dateTime': fecha_hora.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'end': {
                        'dateTime': (fecha_hora + datetime.timedelta(hours=1)).isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'conferenceData':{
                        'createRequest':{
                            'requestId':requestCOD,
                            'conferenceSolutionKey': {
                                'type': 'hangoutsMeet'
                            }
                        }
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=1'
                    ],
                    'attendees': [
                        {'email': correoPrac},
                        {'email': correoPaci}
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }

                event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, sendNotifications=True).execute()
                print("Event created: %s" % (event.get('htmlLink')))
                eventoId = event["id"]

                print(eventoId)

                editarPaciente      = mysql.connection.cursor()
                editarPaciente.execute("UPDATE paciente SET citaActPaci=%s WHERE idPaci=%s",
                            (estatusCita, idPaci,))
                mysql.connection.commit()

                editarPracticante   = mysql.connection.cursor()
                editarPracticante.execute("UPDATE practicante SET estatusCitaPrac=%s WHERE idPrac=%s",
                            (estatusCita, idPrac,))
                mysql.connection.commit()

                regCita = mysql.connection.cursor()
                regCita.execute("INSERT INTO citas (tipo, correoCitaPra, correoCitaPac, direCita, fechaCita, horaCita, estatusCita, eventoId, idCitaPrac, idCitaPaci) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (tipoCita, correoPrac, correoPaci, direCita, fechaCita, horaCita, estatusCita, eventoId, idPrac, idPaci))
                mysql.connection.commit()
                


                flash('Cita agendada con exito.')
                return redirect(url_for('indexPacientes'))


            except HttpError as error:
                print('An error occurred: %s' % error)

#~~~~~~~~~~~~~~~~~~~ Contestar Encuesta ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EncuestaPaciente')
def encuestaPaciente():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginPaci' in session:
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # USAR EL SESSION PARA OBTENER EL ID DEL PACIENTE
                idPaci = session['idPaci']
                datosCitas      =   []

                # FALTA PROBAR ESTO
                selecCita       =   mysql.connection.cursor()
                selecCita.execute("SELECT * FROM citas C INNER JOIN practicante PR ON C.idCitaPrac = PR.idPrac INNER JOIN paciente PA ON C.idCitaPaci = PA.idPaci WHERE idCitaPaci=%s AND estatusCita=%s",(idPaci,1))
                cit              =   selecCita.fetchone()

                nombrPA = cit.get('nombrePaci')
                nombrPA = encriptar.decrypt(nombrPA)
                nombrPA = nombrPA.decode()

                # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                apelpPA = cit.get('apellidoPPaci')
                apelpPA = encriptar.decrypt(apelpPA)
                apelpPA = apelpPA.decode()
                
                # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                apelmPA = cit.get('apellidoMPaci')
                apelmPA = encriptar.decrypt(apelmPA)
                apelmPA = apelmPA.decode()


                # SELECCIONA Y DECODIFICA EL NOMBRE
                nombrPR = cit.get('nombrePrac')
                nombrPR = encriptar.decrypt(nombrPR)
                nombrPR = nombrPR.decode()

                # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                apelpPR = cit.get('apellidoPPrac')
                apelpPR = encriptar.decrypt(apelpPR)
                apelpPR = apelpPR.decode()

                idCita = cit.get('idCita')
                idPrac = cit.get('idPrac')

                # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                apelmPR = cit.get('apellidoMPrac')
                apelmPR = encriptar.decrypt(apelmPR)
                apelmPR = apelmPR.decode()


                # SE AGREGA A UN DICCIONARIO
                noCita = {'nombrePaci': nombrPA, 'apellidoPPaci': apelpPA, 'apellidoMPaci': apelmPA,  'nombrePrac': nombrPR, 'apellidoPPrac': apelpPR, 'apellidoMPrac': apelmPR}

                # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                cit.update(noCita)

                # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                datosCitas.append(cit)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosCitas = tuple(datosCitas)

                

                return render_template('encuesta_paciente.html', nombrePrac = nombrPR, apellidoPPrac =apelpPR, apellidoMPrac = apelmPR, idCita = idCita, idPrac = idPrac, username=session['name'], email=session['correoPaci'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify')) 
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


#~~~~~~~~~~~~~~~~~~~ Respuestas Encuesta ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/ContestarEncuesta', methods=["GET", "POST"])
def contestarEncuesta():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginPaci' in session:
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                #encriptar = encriptado()

                # USAR EL SESSION PARA OBTENER EL ID DEL PACIENTE
                idPaci = session['idPaci']
                idPrac = request.form['idPrac']
                idCita = request.form['idCita']
                pregunta1 = request.form['calificacion-1']
                pregunta2 = request.form['calificacion-2']
                pregunta3 = request.form['calificacion-3']
                pregunta4 = request.form['calificacion-4']
                pregunta5 = request.form['calificacion-5']
                pregunta6 = request.form['calificacion-6']
                pregunta7 = request.form['calificacion-7']
                pregunta8 = request.form['calificacion-8']

                
                regEncuesta = mysql.connection.cursor()
                regEncuesta.execute("INSERT INTO encuesta (pregunta1Encu, pregunta2Encu, pregunta3Encu, pregunta4Encu, pregunta5Encu, pregunta6Encu, pregunta7Encu, pregunta8Encu, idEncuPaci, idEncuPrac) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, pregunta7, pregunta8, idPaci, idPrac,))
                mysql.connection.commit()

                idEncuesta = regEncuesta.lastrowid

                regEncuestaCita = mysql.connection.cursor()
                regEncuestaCita.execute("UPDATE citas SET idEncuestaCita=%s, estatusCita=%s WHERE idCita=%s", (idEncuesta, 4, idCita,))
                            
                mysql.connection.commit()

                flash('Encuesta contestada con exito.')
                return redirect(url_for('indexPacientes'))
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify')) 
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


# ~~~~~~~~~~~~~~~~~~~ Ver Encuestas de Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerEncuestasPracticante/<string:idPrac>', methods=['GET', 'POST'])
def verEncuestasPracticante(idPrac):
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginSup' in session:

                # USAR SESSION PARA OBTENER EL ID DE SUPERVISOR
                idSup = session['idSup']
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecEncuesta    =   mysql.connection.cursor()
                selecEncuesta.execute("SELECT * FROM encuesta E INNER JOIN practicante PR ON E.idEncuPrac = PR.idPrac INNER JOIN paciente PA ON E.idEncuPaci = PA.idPaci WHERE idEncuPrac=%s",(idPrac,))
                encu              =   selecEncuesta.fetchall()

                # SE CREA UNA LISTA
                datosEncu = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 
                for sup in encu:
                    
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrPr = sup.get('nombrePrac')
                    nombrPr = encriptar.decrypt(nombrPr)
                    nombrPr = nombrPr.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPr = sup.get('apellidoPPrac')
                    apelpPr = encriptar.decrypt(apelpPr)
                    apelpPr = apelpPr.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPr = sup.get('apellidoMPrac')
                    apelmPr = encriptar.decrypt(apelmPr)
                    apelmPr = apelmPr.decode()

                    nombrPa = sup.get('nombrePaci')
                    nombrPa = encriptar.decrypt(nombrPa)
                    nombrPa = nombrPa.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPa = sup.get('apellidoPPaci')
                    apelpPa = encriptar.decrypt(apelpPa)
                    apelpPa = apelpPa.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPa = sup.get('apellidoMPaci')
                    apelmPa = encriptar.decrypt(apelmPa)
                    apelmPa = apelmPa.decode()

                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombrePrac': nombrPr, 'apellidoPPrac': apelpPr, 'apellidoMPrac': apelmPr, 'nombrePaci': nombrPa, 'apellidoPPaci': apelpPa, 'apellidoMPaci': apelmPa}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    sup.update(noPrac)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosEncu.append(sup)
                
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosEncu = tuple(datosEncu)

                

                return render_template('encuesta_practicante.html', datosEncu = datosEncu, username=session['name'], email=session['correoSup'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


# ~~~~~~~~~~~~~~~~~~~ Ver Resultados de Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerResultadosEncuesta/<string:idEncu>', methods=['GET', 'POST'])
def verResultadosEncuesta(idEncu):
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginSup' in session:

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecEncuesta    =   mysql.connection.cursor()
                selecEncuesta.execute("SELECT * FROM encuesta WHERE idEncu=%s",(idEncu,))
                encu              =   selecEncuesta.fetchone()

                print(encu)

                return render_template('resultados_encuestas.html', resu = encu, username=session['name'], email=session['correoSup'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))

#~~~~~~~~~~~~~~~~~~~ Eliminar Cita Paciente ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCitaPaciente', methods=["GET", "POST"])
def eliminarCitaPaciente():

        # USO SESION PARA OBTENER LOS DATOS DEL PACIENTE
        
        # RECUPERAR DATOS
        idCita      = request.form['idCita']
        fechaCita   = request.form['fechaCita']
        horaCita    = request.form['horaCita']
        eventoIdCita    = request.form['eventoCita']
        
        estatusCita = 2

        # Convertir la cadena de fecha a objeto datetime
        fechaCita = datetime.datetime.strptime(fechaCita, '%Y-%m-%d').date()

        # Convertir la cadena de hora a objeto datetime
        horaCita = datetime.datetime.strptime(horaCita, '%H:%M:%S').time()

        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().date()
        hora_actual = datetime.datetime.now().time()

        # Combinar la fecha actual con la hora actual
        fecha_hora_actual = datetime.datetime.combine(fecha_actual, hora_actual)

        # Calcular la diferencia entre la fecha y hora de la cita y la fecha y hora actual
        diferencia = datetime.datetime.combine(fechaCita, horaCita) - fecha_hora_actual

        # Verificar si todavía hay más de 24 horas de diferencia antes de la cita
        if diferencia.total_seconds() > 24 * 3600:
            print("Todavía hay más de 24 horas antes de la cita. Puedes cancelarla.")

            """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                service = build('calendar', 'v3', credentials=creds)

                service.events().delete(calendarId='primary', eventId=eventoIdCita, sendNotifications=True).execute()

                editarCita      = mysql.connection.cursor()
                editarCita.execute("UPDATE citas SET estatusCita=%s WHERE idCita=%s",
                            (estatusCita, idCita,))
                mysql.connection.commit()

                flash('Cita eliminada con exito.')
                return redirect(url_for('indexPacientes'))


            except HttpError as error:
                print('An error occurred: %s' % error)
        
        else:
            print("Ya no puedes cancelar la cita. Ya pasaron menos de 24 horas.")
            flash("No se puede cancelar la cita, faltan menos de 24 horas")
            return redirect(url_for('indexPacientes'))


#~~~~~~~~~~~~~~~~~~~ Eliminar Cita Supervisor ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCitaSupervisor', methods=["GET", "POST"])
def eliminarCitaSupervisor():

        # USO SESION PARA OBTENER LOS DATOS DEL PACIENTE
        
        # RECUPERAR DATOS
        idCita          = request.form['idCita']
        eventoIdCita    = request.form['eventoCita']
        cancelacion     = request.form['cancelacion']

        # Verificar si todavía hay más de 24 horas de diferencia antes de la cita
        if cancelacion == 'Si':
            print("Como no pa, ahi te va tu cancelacion.")

            """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                service = build('calendar', 'v3', credentials=creds)

                service.events().delete(calendarId='primary', eventId=eventoIdCita, sendNotifications=True).execute()

                estatusCita = 2
                editarCita      = mysql.connection.cursor()
                editarCita.execute("UPDATE citas SET estatusCita=%s WHERE idCita=%s",
                            (estatusCita, idCita,))
                mysql.connection.commit()

                flash('Cita eliminada con exito.')
                return redirect(url_for('verPracticantesSupervisor'))


            except HttpError as error:
                print('An error occurred: %s' % error)
        
        else:
            estatusCita = 1
            editarCita      = mysql.connection.cursor()
            editarCita.execute("UPDATE citas SET estatusCita=%s WHERE idCita=%s",
                        (estatusCita, idCita,))
            mysql.connection.commit()
            print("Nel padrino, ahuevo ahora la bebes o la derramas")
            flash("No se puede cancelar la cita, faltan menos de 24 horas")
            return redirect(url_for('verPracticantesSupervisor'))


# ~~~~~~~~~~~~~~~~~~~ Crear Cita ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/AgendarCita', methods=['GET', 'POST'])
def agendarCita():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginPaci' in session:
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # USAR EL SESSION PARA OBTENER EL ID DEL PACIENTE
                idPaci = session['idPaci']

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecPrac        =   mysql.connection.cursor()
                selecPrac.execute("SELECT * FROM practicante WHERE activoPrac IS NOT NULL ORDER BY RAND() LIMIT 10")
                pra              =   selecPrac.fetchall()

                # SE CREA UNA LISTA
                datosPrac = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 
                for pract in pra:
                    
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = pract.get('nombrePrac')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = pract.get('apellidoPPrac')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = pract.get('apellidoMPrac')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()

                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombrePrac': nombr, 'apellidoPPrac': apelp, 'apellidoMPrac': apelm}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    pract.update(noPrac)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPrac.append(pract)
                
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPrac = tuple(datosPrac)
                print(datosPrac)

                return render_template('agenda_cita.html', datosPrac = datosPrac, username=session['name'], email=session['correoPaci'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


#~~~~~~~~~~~~~~~~~~~ Eliminar Cita Pracicante ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCitaPracticante', methods=["GET", "POST"])
def eliminarCitaPracticante():
        
    idCita      = request.form['idCita']
    fechaCita   = request.form['fechaCita']
    horaCita    = request.form['horaCita']
    # Tipos de estatus: 1 = ACTIVA | 2 = CANCELADA | 3 = PENDIENTE POR CANCELAR | 4 = TERMINADA
    estatusCita = 3

    # Convertir la cadena de fecha a objeto datetime
    fechaCita = datetime.datetime.strptime(fechaCita, '%Y-%m-%d').date()

    # Convertir la cadena de hora a objeto datetime
    horaCita = datetime.datetime.strptime(horaCita, '%H:%M:%S').time()

    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().date()
    hora_actual = datetime.datetime.now().time()

    # Combinar la fecha actual con la hora actual
    fecha_hora_actual = datetime.datetime.combine(fecha_actual, hora_actual)

    # Calcular la diferencia entre la fecha y hora de la cita y la fecha y hora actual
    diferencia = datetime.datetime.combine(fechaCita, horaCita) - fecha_hora_actual

    # Verificar si todavía hay más de 2 horas de diferencia antes de la cita
    if diferencia.total_seconds() > 2 * 3600:
        editarCita      = mysql.connection.cursor()
        editarCita.execute("UPDATE citas SET estatusCita=%s WHERE idCita=%s",
                    (estatusCita, idCita,))
        mysql.connection.commit()

        flash('Cita eliminada con exito.')
        print("Todavía hay más de 2 horas antes de la cita. Puedes cancelarla.")
        return redirect(url_for('indexPracticantes'))

    else:
        print("Ya no puedes cancelar la cita, han pasado menos de 2 horas.")
        flash("No se puede cancelar la cita, faltan menos de 2 horas")
        return redirect(url_for('indexPracticantes'))


# VER PRACTICANTES SUPERVISOR
@PCapp.route('/VerPracticantesSupervisor', methods=['GET', 'POST'])
def verPracticantesSupervisor():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginSup' in session:

                # USAR SESSION PARA OBTENER EL ID DE SUPERVISOR
                idSup = session['idSup']
                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecPrac        =   mysql.connection.cursor()
                selecPrac.execute("SELECT * FROM supervisor S INNER JOIN practicante P ON P.idSupPrac = S.idSup WHERE S.idSup=%s AND activoSup IS NOT NULL AND P.activoPrac IS NOT NULL",(idSup,))
                pra              =   selecPrac.fetchall()

                # SE CREA UNA LISTA
                datosPrac = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 
                for sup in pra:
                    
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrPr = sup.get('nombrePrac')
                    nombrPr = encriptar.decrypt(nombrPr)
                    nombrPr = nombrPr.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPr = sup.get('apellidoPPrac')
                    apelpPr = encriptar.decrypt(apelpPr)
                    apelpPr = apelpPr.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPr = sup.get('apellidoMPrac')
                    apelmPr = encriptar.decrypt(apelmPr)
                    apelmPr = apelmPr.decode()


                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrSU = sup.get('nombreSup')
                    nombrSU = encriptar.decrypt(nombrSU)
                    nombrSU = nombrSU.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpSU = sup.get('apellidoPSup')
                    apelpSU = encriptar.decrypt(apelpSU)
                    apelpSU = apelpSU.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmSU = sup.get('apellidoMSup')
                    apelmSU = encriptar.decrypt(apelmSU)
                    apelmSU = apelmSU.decode()


                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombrePrac': nombrPr, 'apellidoPPrac': apelpPr, 'apellidoMPrac': apelmPr, 'nombreSup': nombrSU, 'apellidoPSup': apelpSU, 'apellidoMSup': apelmSU}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    sup.update(noPrac)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPrac.append(sup)
                
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPrac = tuple(datosPrac)

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecCitas        =   mysql.connection.cursor()
                selecCitas.execute("SELECT * FROM supervisor S INNER JOIN practicante P ON P.idSupPrac = S.idSup INNER JOIN citas C ON C.idCitaPrac = P.idPrac WHERE P.idSupPrac=%s AND activoSup IS NOT NULL AND C.estatusCita = %s AND P.activoPrac IS NOT NULL",(idSup, 3))
                cita              =   selecCitas.fetchall()

                # SE CREA UNA LISTA
                datosCitas = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS 
                for cit in cita:
                    
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrPr = cit.get('nombrePrac')
                    nombrPr = encriptar.decrypt(nombrPr)
                    nombrPr = nombrPr.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPr = cit.get('apellidoPPrac')
                    apelpPr = encriptar.decrypt(apelpPr)
                    apelpPr = apelpPr.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPr = cit.get('apellidoMPrac')
                    apelmPr = encriptar.decrypt(apelmPr)
                    apelmPr = apelmPr.decode()

                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombrSU = cit.get('nombreSup')
                    nombrSU = encriptar.decrypt(nombrSU)
                    nombrSU = nombrSU.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpSU = cit.get('apellidoPSup')
                    apelpSU = encriptar.decrypt(apelpSU)
                    apelpSU = apelpSU.decode()
                    
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmSU = cit.get('apellidoMSup')
                    apelmSU = encriptar.decrypt(apelmSU)
                    apelmSU = apelmSU.decode()

                    # SE AGREGA A UN DICCIONARIO
                    noCita = {'nombrePrac': nombrPr, 'apellidoPPrac': apelpPr, 'apellidoMPrac': apelmPr, 'nombreSup': nombrSU, 'apellidoPSup': apelpSU, 'apellidoMSup': apelmSU}

                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    cit.update(noCita)

                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosCitas.append(cit)
                
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosCitas = tuple(datosCitas)


                return render_template('index_supervisor.html', pract = pra, datosPrac = datosPrac, datosCitas = datosCitas, username=session['name'], email=session['correoSup'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))


#~~~~~~~~~~~~~~~~~~~ Ver Practicantes ADMINISTRADOR ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerPracticantesAdm', methods=['GET', 'POST'])
def verPracticantesAdm():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:

                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()


                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecPrac        =   mysql.connection.cursor()
                selecPrac.execute("SELECT * FROM practicante WHERE activoPrac IS NOT NULL")
                pra              =   selecPrac.fetchall()


                # SE CREA UNA LISTA
                datosPrac = []


                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
                for pract in pra:
                
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = pract.get('nombrePrac')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = pract.get('apellidoPPrac')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = pract.get('apellidoMPrac')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()



                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombrePrac': nombr, 'apellidoPPrac': apelp, 'apellidoMPrac': apelm}


                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    pract.update(noPrac)


                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPrac.append(pract)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPrac = tuple(datosPrac)


                return render_template('adm_pract.html', pract = pra, datosPrac = datosPrac, username=session['name'], email=session['correoAd'])
            
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))
    

#~~~~~~~~~~~~~~~~~~~ Eliminar Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaPracticantesAdm', methods=["GET", "POST"])
def eliminarCuentaPracticantesAdm():
    idPrac               = request.form['idPrac']
    activoPrac           = None
    eliminarPracticante  = mysql.connection.cursor()
    eliminarPracticante.execute("UPDATE practicante set activoPrac=%s WHERE idPrac=%s",
                        (activoPrac, idPrac,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPracticantesAdm'))

    #~~~~~~~~~~~~~~~~~~~ Eliminar Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaPracticantesSup', methods=["GET", "POST"])
def eliminarCuentaPracticantesSup():
    idPrac               = request.form['idPrac']
    activoPrac           = None
    eliminarPracticante  = mysql.connection.cursor()
    eliminarPracticante.execute("UPDATE practicante set activoPrac=%s WHERE idPrac=%s",
                        (activoPrac, idPrac,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPracticantesSupervisor'))

#~~~~~~~~~~~~~~~~~~~ Editar Practicantes ADMIN ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaPracticantesAdm', methods=["GET", "POST"])
def editarCuentaPracticantesAdm():


    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()


    # SE RECIBE LA INFORMACION
    idPrac               = request.form['idPrac']


    nombrePrac        = request.form['nombrePrac'].encode('utf-8')
    nombrePracCC      = encriptar.encrypt(nombrePrac)


    apellidoPPrac     = request.form['apellidoPPrac'].encode('utf-8')
    apellidoPPracCC   = encriptar.encrypt(apellidoPPrac)


    apellidoMPrac     = request.form['apellidoMPrac'].encode('utf-8')
    apellidoMPracCC   = encriptar.encrypt(apellidoMPrac)
    editarPracticante    = mysql.connection.cursor()
    editarPracticante.execute("UPDATE practicante SET nombrePrac=%s, apellidoPPrac=%s, apellidoMPrac=%s WHERE idPrac=%s",
                        (nombrePracCC, apellidoPPracCC, apellidoMPracCC, idPrac,))
    mysql.connection.commit()


    # PARA SUBIR LA FOTO
    if request.files.get('foto'):
        foto                =   request.files['foto']
        fotoActual          =   secure_filename(foto.filename)
        foto.save(os.path.join(PCapp.config['UPLOAD_FOLDER'], fotoActual))
        picture             =   mysql.connection.cursor()
        picture.execute("UPDATE practicante SET fotoPrac=%s WHERE idPrac=%s", (fotoActual, idPrac,))
        mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPracticantesAdm'))

#~~~~~~~~~~~~~~~~~~~ Editar Practicantes Supervisores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaPracticantesSup', methods=["GET", "POST"])
def editarCuentaPracticantesSup():
    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()

    # SE RECIBE LA INFORMACION
    idPrac               = request.form['idPrac']

    nombrePrac        = request.form['nombrePrac'].encode('utf-8')
    nombrePracCC      = encriptar.encrypt(nombrePrac)


    apellidoPPrac     = request.form['apellidoPPrac'].encode('utf-8')
    apellidoPPracCC   = encriptar.encrypt(apellidoPPrac)


    apellidoMPrac     = request.form['apellidoMPrac'].encode('utf-8')
    apellidoMPracCC   = encriptar.encrypt(apellidoMPrac)
    editarPracticante    = mysql.connection.cursor()
    editarPracticante.execute("UPDATE practicante SET nombrePrac=%s, apellidoPPrac=%s, apellidoMPrac=%s WHERE idPrac=%s",
                        (nombrePracCC, apellidoPPracCC, apellidoMPracCC, idPrac,))
    mysql.connection.commit()


    # PARA SUBIR LA FOTO
    if request.files.get('foto'):
        foto                =   request.files['foto']
        fotoActual          =   secure_filename(foto.filename)
        foto.save(os.path.join(PCapp.config['UPLOAD_FOLDER'], fotoActual))
        picture             =   mysql.connection.cursor()
        picture.execute("UPDATE practicante SET fotoPrac=%s WHERE idPrac=%s", (fotoActual, idPrac,))
        mysql.connection.commit()

    flash('Cuenta editada con exito.')
    return redirect(url_for('verPracticantesSupervisor'))


#~~~~~~~~~~~~~~~~~~~ Crear Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/CrearCuentaPracticantes', methods=["GET", "POST"])
def crearCuentaPracticantes():
    if request.method == 'POST':
       
        #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
        encriptar = encriptado()

        # SE RECIBE LA INFORMACION
        nombrePrac        = request.form['nombrePrac'].encode('utf-8')
        nombrePracCC      = encriptar.encrypt(nombrePrac)
        apellidoPPrac     = request.form['apellidoPPrac'].encode('utf-8')
        apellidoPPracCC   = encriptar.encrypt(apellidoPPrac)
        apellidoMPrac     = request.form['apellidoMPrac'].encode('utf-8')
        apellidoMPracCC   = encriptar.encrypt(apellidoMPrac)
        sexoPrac          = request.form['sexoPrac']
        fechaNacPrac      = request.form['fechaNacPrac']
        celPrac           = request.form['celPrac']
        codigoUPrac       = request.form['codigoUPrac']
        idSupPrac         = session['idSup']
        
        # CONFIRMAR CORREO CON LA BD
        correoPrac        = request.form['correoPrac']

        # CAMBIAR EL HASH DE LA CONTRA POR BCRYPT
        contraPrac        = request.form['contraPrac']
        hashed_password = bcryptObj.generate_password_hash(contraPrac).decode('utf-8')
        fechaActual     = date.today()
        fechaNacimiento = datetime.datetime.strptime(fechaNacPrac, '%Y-%m-%d')
        fechaNac = fechaNacimiento.date()
        edad = fechaActual - fechaNac
        edad = edad.days
        edad = edad/365
        edad = math.floor(edad)
       
        # FUNCION QUE CREA EL CODIGO DE SGURIDAD // CREAR FUNCION APARTE
        let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"


        gen = f"{let}{num}"
        lon = 8
        ran = random.sample(gen, lon)
        cod = "".join(ran)
        codVeriPrac  = cod
        activoPrac   = 0
        veriPrac     = 1

        
         # Verificar si el correo ya está registrado en la base de datos
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM practicante WHERE correoPrac=%s AND activoPrac IS NOT NULL", [correoPrac,])
        
        if result > 0:
            # Si el correo ya está registrado, mostrar un mensaje de error
            flash("El correo ya está registrado", 'danger')
            cur.close()
            return redirect(url_for('verPracticantesSupervisor'))        
        
        regPracticante = mysql.connection.cursor()
        regPracticante.execute("INSERT INTO practicante (nombrePrac, apellidoPPrac, apellidoMPrac, contraPrac, sexoPrac, codVeriPrac, correoPrac, fechaNacPrac, activoPrac, veriPrac, edadPrac, celPrac, codigoUPrac, idSupPrac) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (nombrePracCC, apellidoPPracCC, apellidoMPracCC, hashed_password, sexoPrac, codVeriPrac, correoPrac, fechaNacPrac, activoPrac, veriPrac, edad, celPrac, codigoUPrac, idSupPrac,))
        mysql.connection.commit()

        # PARA SUBIR LA FOTO
        if request.files.get('foto'):
            idPrac              =   regPracticante.lastrowid
            foto                =   request.files['foto']
            fotoActual          =   secure_filename(foto.filename)
            foto.save(os.path.join(PCapp.config['UPLOAD_FOLDER'], fotoActual))
            picture             =   mysql.connection.cursor()
            picture.execute("UPDATE practicante SET fotoPrac=%s WHERE idPrac=%s", (fotoActual, idPrac,))
            mysql.connection.commit()


        # MANDAR CORREO CON CODIGO DE VERIRIFICACION
        idPrac              = regPracticante.lastrowid
        selPrac             = mysql.connection.cursor()
        selPrac.execute("SELECT * FROM practicante WHERE idPrac=%s",(idPrac,))
        pra                 = selPrac.fetchone()

        nombr = pra.get('nombrePrac')
        nombr = nombr.encode()
        nombr = encriptar.decrypt(nombr)
        nombr = nombr.decode()

        # SE MANDA EL CORREO
        msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[correoPrac])
        msg.body = render_template('layoutmail.html', name=nombr, verification_code=codVeriPrac)
        msg.html = render_template('layoutmail.html', name=nombr, verification_code=codVeriPrac)
        mail.send(msg)       
    
        flash('Cuenta creada con exito.')

        #MANDAR A UNA VENTANA PARA QUE META EL CODIGO DE VERFICIACION
        return redirect(url_for('verPracticantesSupervisor'))
    else:
        flash('No se pudo crear la cuenta.')
        return redirect(url_for('verPracticantesSupervisor'))


# ~~~~~~~~~~~~~~~~~~~ Editar Pacientes Admin ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaPacienteAdm', methods=["GET", "POST"])
def editarCuentaPacienteAdm():
    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()

    # SE RECIBE LA INFORMACION
    idPaci          = request.form['idPaci']


    nombrePaci          = request.form['nombrePaci'].encode('utf-8')
    nombrePaciCC        = encriptar.encrypt(nombrePaci)

    apellidoPPaci       = request.form['apellidoPPaci'].encode('utf-8')
    apellidoPPaciCC     = encriptar.encrypt(apellidoPPaci)

    apellidoMPaci       = request.form['apellidoMPaci'].encode('utf-8')
    apellidoMPaciCC     = encriptar.encrypt(apellidoMPaci)

    editarPaciente    = mysql.connection.cursor()


    editarPaciente.execute("UPDATE paciente SET nombrePaci=%s, apellidoPPaci=%s, apellidoMPaci=%s WHERE idPaci=%s",
                        (nombrePaciCC, apellidoPPaciCC, apellidoMPaciCC,  idPaci,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPacientesAdm'))


# ~~~~~~~~~~~~~~~~~~~ Editar Pacientes Supervisor ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaPacienteSup', methods=["GET", "POST"])
def editarCuentaPacienteSup():


    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()


    # SE RECIBE LA INFORMACION


    idPaci          = request.form['idPaci']


    nombrePaci          = request.form['nombrePaci'].encode('utf-8')
    nombrePaciCC        = encriptar.encrypt(nombrePaci)


    apellidoPPaci       = request.form['apellidoPPaci'].encode('utf-8')
    apellidoPPaciCC     = encriptar.encrypt(apellidoPPaci)


    apellidoMPaci       = request.form['apellidoMPaci'].encode('utf-8')
    apellidoMPaciCC     = encriptar.encrypt(apellidoMPaci)



    editarPaciente    = mysql.connection.cursor()


    editarPaciente.execute("UPDATE paciente SET nombrePaci=%s, apellidoPPaci=%s, apellidoMPaci=%s WHERE idPaci=%s",
                        (nombrePaciCC, apellidoPPaciCC, apellidoMPaciCC,  idPaci,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPaciente'))

#~~~~~~~~~~~~~~~~~~~ Eliminar Pacientes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaPacienteAdm', methods=["GET", "POST"])
def eliminarCuentaPacienteAdm():
    idPaci              = request.form['idPaci']
    activoPaci          = None
    EliminarPaciente  = mysql.connection.cursor()
    EliminarPaciente.execute("UPDATE paciente set activoPaci=%s WHERE idPaci=%s",
                        (activoPaci, idPaci,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPacientesAdm'))

#~~~~~~~~~~~~~~~~~~~ Eliminar Pacientes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaPacienteSup', methods=["GET", "POST"])
def eliminarCuentaPacienteSup():
    idPaci              = request.form['idPaci']
    activoPaci          = None
    EliminarPaciente  = mysql.connection.cursor()
    EliminarPaciente.execute("UPDATE paciente set activoPaci=%s WHERE idPaci=%s",
                        (activoPaci, idPaci,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verPaciente'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~ CRUD Supervisores ~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


#~~~~~~~~~~~~~~~~~~~ Crear Supervisores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/CrearCuentaSupervisor', methods=["GET", "POST"])
def crearCuentaSupervisor():
    if request.method == 'POST':

        #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
        encriptar = encriptado()

        # SE RECIBE LA INFORMACION
        nombreSup        = request.form['nombreSup'].encode('utf-8')
        nombreSupCC      = encriptar.encrypt(nombreSup)


        apellidoPSup     = request.form['apellidoPSup'].encode('utf-8')
        apellidoPSupCC   = encriptar.encrypt(apellidoPSup)


        apellidoMSup     = request.form['apellidoMSup'].encode('utf-8')
        apellidoMSupCC   = encriptar.encrypt(apellidoMSup)

        # CONFIRMAR CORREO CON LA BD
        correoSup        = request.form['correoSup']

        contraSup        = request.form['contraSup']
        hashed_password = bcryptObj.generate_password_hash(contraSup).decode('utf-8')


        # FUNCION QUE CREA EL CODIGO DE SGURIDAD // CREAR FUNCION APARTE
        let = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"


        gen = f"{let}{num}"
        lon = 8
        ran = random.sample(gen, lon)
        cod = "".join(ran)

        codVeriSup  = cod
        activoSup   = 0
        veriSup     = 1
        priviSup    = 2
        
        # Verificar si el correo ya está registrado en la base de datos
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM supervisor WHERE correoSup=%s AND activoSup IS NOT NULL", [correoSup,])
        if result > 0:
            # Si el correo ya está registrado, mostrar un mensaje de error
            flash("El correo ya está registrado", 'danger')
            cur.close()
            return redirect(url_for('verSupervisor')) 

        regSupervisor = mysql.connection.cursor()
        regSupervisor.execute("INSERT INTO supervisor (nombreSup, apellidoPSup, apellidoMSup, correoSup, contraSup, codVeriSup, activoSup, veriSup, priviSup) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (nombreSupCC, apellidoPSupCC, apellidoMSupCC, correoSup, hashed_password, codVeriSup, activoSup, veriSup, priviSup))
        mysql.connection.commit()

        # MANDAR CORREO CON CODIGO DE VERIRIFICACION

        idSup               = regSupervisor.lastrowid
        selSup              = mysql.connection.cursor()
        selSup.execute("SELECT * FROM supervisor WHERE idSup=%s",(idSup,))
        sup                 = selSup.fetchone()
       


        nombr = sup.get('nombreSup')
        nombr = nombr.encode()
        nombr = encriptar.decrypt(nombr)
        nombr = nombr.decode()

        
        # SE MANDA EL CORREO
        msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[correoSup])
        msg.body = render_template('layoutmail.html', name=nombr, verification_code=codVeriSup)
        msg.html = render_template('layoutmail.html', name=nombr, verification_code=codVeriSup)
        mail.send(msg)       

        flash('Cuenta creada con exito.')

        #MANDAR A UNA VENTANA PARA QUE META EL CODIGO DE VERFICIACION
        return redirect(url_for('verSupervisor'))
    else:
        flash('Error al crear la cuenta.')
        return redirect(url_for('verSupervisor'))

#~~~~~~~~~~~~~~~~~~~ Ver Supervisores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/VerSupervisor', methods=['GET', 'POST'])
def verSupervisor():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:

                # SE MANDA A LLAMAR LA FUNCION PARA DESENCRIPTAR
                encriptar = encriptado()

                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecSup        =   mysql.connection.cursor()
                selecSup.execute("SELECT * FROM supervisor WHERE activoSup IS NOT NULL")
                sup             =   selecSup.fetchall()

                # SE CREA UNA LISTA
                datosSup = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
                for super in sup:
                
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = super.get('nombreSup')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()

                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = super.get('apellidoPSup')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = super.get('apellidoMSup')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()

                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombreSup': nombr, 'apellidoPSup': apelp, 'apellidoMSup': apelm}


                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    super.update(noPrac)


                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosSup.append(super)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosSup = tuple(datosSup)


                return render_template('adm_super.html', super = sup, datosSup = datosSup, username=session['name'], email=session['correoAd'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))

    
#~~~~~~~~~~~~~~~~~~~ Editar Supervisores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EditarCuentaSupervisor', methods=["GET", "POST"])
def editarCuentaSupervisor():


    #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
    encriptar = encriptado()


    # SE RECIBE LA INFORMACION
    nombreSup        = request.form['nombreSup'].encode('utf-8')
    nombreSupCC      = encriptar.encrypt(nombreSup)


    apellidoPSup     = request.form['apellidoPSup'].encode('utf-8')
    apellidoPSupCC   = encriptar.encrypt(apellidoPSup)


    apellidoMSup     = request.form['apellidoMSup'].encode('utf-8')
    apellidoMSupCC   = encriptar.encrypt(apellidoMSup)


    idSup               = request.form['idSup']
    editarSupervisor    = mysql.connection.cursor()


    editarSupervisor.execute("UPDATE supervisor SET nombreSup=%s, apellidoPSup=%s, apellidoMSup=%s WHERE idSup=%s",
                        (nombreSupCC, apellidoPSupCC, apellidoMSupCC, idSup,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verSupervisor'))


#~~~~~~~~~~~~~~~~~~~ Eliminar Supervisores ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/EliminarCuentaSupervisor', methods=["GET", "POST"])
def eliminarCuentaSupervisor():
    idSup               = request.form['idSup']
    activoSup           = None
    EliminarSupervisor  = mysql.connection.cursor()
    EliminarSupervisor.execute("UPDATE supervisor set activoSup=%s WHERE idSup=%s",
                        (activoSup, idSup,))
    mysql.connection.commit()
    flash('Cuenta editada con exito.')
    return redirect(url_for('verSupervisor'))


@PCapp.route('/IndexAdministrador', methods=['GET', 'POST'])
def indexAdministrador():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginAdmin' in session:
                return render_template('index_admin.html', username=session['name'], email=session['correoAd'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))
    

#~~~~~~~~~~~~~~~~~~~ Index Practicantes ~~~~~~~~~~~~~~~~~~~#
@PCapp.route('/IndexPracticantes', methods=["GET", "POST"])
def indexPracticantes():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginPrac' in session:

                #SE MANDA A LLAMRA LA FUNCION PARA ENCRIPTAR
                encriptar = encriptado()


                idPrac = session['idPrac']


                # SE SELECCIONA TODOS LOS DATOS DE LA BD POR SI SE LLEGA A NECESITAR
                selecPrac        =   mysql.connection.cursor()
                selecPrac.execute("SELECT * FROM citas C INNER JOIN practicante P ON P.idPrac = C.idCitaPrac INNER JOIN paciente PA ON PA.idPaci = C.idCitaPaci WHERE P.idPrac=%s AND activoPrac IS NOT NULL AND estatusCita=%s",(idPrac, 1))
                pra              =   selecPrac.fetchall()


                # SE CREA UNA LISTA
                datosPrac = []

                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
                for pract in pra:
                
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = pract.get('nombrePrac')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = pract.get('apellidoPPrac')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = pract.get('apellidoMPrac')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()


                    nombrPA = pract.get('nombrePaci')
                    nombrPA = encriptar.decrypt(nombrPA)
                    nombrPA = nombrPA.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPA = pract.get('apellidoPPaci')
                    apelpPA = encriptar.decrypt(apelpPA)
                    apelpPA = apelpPA.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPA = pract.get('apellidoMPaci')
                    apelmPA = encriptar.decrypt(apelmPA)
                    apelmPA = apelmPA.decode()


                    # SE AGREGA A UN DICCIONARIO
                    noPrac = {'nombrePrac': nombr, 'apellidoPPrac': apelp, 'apellidoMPrac': apelm, 'nombrePaci': nombrPA, 'apellidoPPaci': apelpPA, 'apellidoMPaci': apelmPA}


                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    pract.update(noPrac)


                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPrac.append(pract)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPrac = tuple(datosPrac)


                selecPracH        =   mysql.connection.cursor()
                selecPracH.execute("SELECT * FROM citas C INNER JOIN practicante P ON P.idPrac = C.idCitaPrac INNER JOIN paciente PA ON PA.idPaci = C.idCitaPaci WHERE P.idPrac=%s AND activoPrac IS NOT NULL AND estatusCita=%s",(idPrac, 4))
                praH              =   selecPracH.fetchall()


                # SE CREA UNA LISTA
                datosPracH = []


                # CON ESTE FOR, SE VAN OBTENIENDO LOS DATOS PARA POSTERIORMENTE DECODIFICARLOS
                for praHi in praH:
                
                    # SELECCIONA Y DECODIFICA EL NOMBRE
                    nombr = praHi.get('nombrePrac')
                    nombr = encriptar.decrypt(nombr)
                    nombr = nombr.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelp = praHi.get('apellidoPPrac')
                    apelp = encriptar.decrypt(apelp)
                    apelp = apelp.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelm = praHi.get('apellidoMPrac')
                    apelm = encriptar.decrypt(apelm)
                    apelm = apelm.decode()


                    nombrPA = praHi.get('nombrePaci')
                    nombrPA = encriptar.decrypt(nombrPA)
                    nombrPA = nombrPA.decode()


                    # SELECCIONA Y DECODIFICA EL APELLIDO PATERNO
                    apelpPA = praHi.get('apellidoPPaci')
                    apelpPA = encriptar.decrypt(apelpPA)
                    apelpPA = apelpPA.decode()
                
                    # SELECCIONA Y DECODIFICA EL APELLIDO MATERNO
                    apelmPA = praHi.get('apellidoMPaci')
                    apelmPA = encriptar.decrypt(apelmPA)
                    apelmPA = apelmPA.decode()


                    # SE AGREGA A UN DICCIONARIO
                    noPracH = {'nombrePrac': nombr, 'apellidoPPrac': apelp, 'apellidoMPrac': apelm, 'nombrePaci': nombrPA, 'apellidoPPaci': apelpPA, 'apellidoMPaci': apelmPA}


                    # SE ACTUALIZA EL DICCIONARIO QUE MANDA LA BD
                    praHi.update(noPracH)


                    # SE AGREGA A UNA LISTA ANTERIORMENTE CREADA
                    datosPracH.append(praHi)
            
                # LA LISTA LA CONVERTIMOS A TUPLE PARA PODER USARLA CON MAYOR COMODIDAD EN EL FRONT
                datosPracH = tuple(datosPracH)


                return render_template('index_practicante.html', pract = pra, datosPrac = datosPrac, datosPracH=datosPracH, username=session['name'], email=session['correoPrac'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify'))
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))
    


@PCapp.route('/')
@login_required
@verified_required
def home():
    if 'loginPaci' in session:
        return redirect(url_for('indexPacientes'))
    elif 'loginPrac' in session:
        return redirect(url_for('indexPracticantes'))
    elif 'loginSup' in session:
        return redirect(url_for('indexSupervisor'))
    elif 'loginAdmin' in session:
        return redirect(url_for('indexAdministrador'))
    else:
        return redirect(url_for('auth'))

@PCapp.route('/AgregarPracticante')
@login_required
@verified_required
def agregarPracticante():
    if 'login' in session:
        if session['verificado'] == 2:
            if 'loginSup' in session:
                return render_template('agregar_practicante.html', username=session['name'], email=session['correoSup'])
            else:
                flash("No tienes permiso para acceder a esta página", 'danger')
                return redirect(url_for('home'))
        else:
            flash("Por favor, verifica tu cuenta antes de continuar", 'warning')
            return redirect(url_for('verify')) 
    else:
        flash("Por favor, inicia sesión para continuar", 'warning')
        return redirect(url_for('auth'))

@PCapp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth'))

@PCapp.route('/protected')
@verified_required
def protected ():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    PCapp.secret_key = '123'
    csrf.init_app(PCapp)
    PCapp.register_error_handler(401,status_401)
    PCapp.register_error_handler(404,status_404)
    PCapp.run(port=3000,debug=True)
    
    
#E we, cuanto es 2 + 2?

# FALTA PROBAR CITAS EN PACIENTES
# ELIMINAR CITAS (PACIENTES Y PRACTICANTES)
# ALL EL SISTEMA DE ENCUESTAS ZZZZZZZ