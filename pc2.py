from ast                import If
from threading          import activeCount
from time               import time
from flask              import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mysqldb      import MySQL, MySQLdb
from flask_mail         import Mail, Message
from flask_bcrypt       import bcrypt,Bcrypt
from flask_login        import LoginManager, login_user, logout_user, login_required, login_manager
from flask_wtf.csrf     import CSRFProtect
from functools          import wraps
from werkzeug.utils     import secure_filename
from datetime           import date, datetime
import base64
import pdfkit
import os
import random
import secrets
import re

PCapp                                   = Flask(__name__)
mysql                                   = MySQL(PCapp)
csrf=CSRFProtect()
PCapp.config['MYSQL_HOST']              = 'localhost'
PCapp.config['MYSQL_USER']              = 'root'
PCapp.config['MYSQL_PASSWORD']          = 'antolin1'
PCapp.config['MYSQL_DB']                = 'psiconnection'
PCapp.config['MYSQL_CURSORCLASS']       = 'DictCursor'
PCapp.config['UPLOAD_FOLDER']           = './static/img/'
PCapp.config['UPLOAD_FOLDER_PDF']       = './static/pdf/'


PCapp.config['MAIL_SERVER']='smtp.gmail.com'
PCapp.config['MAIL_PORT'] = 465
PCapp.config['MAIL_USERNAME'] = 'psi.connection09@gmail.com'
PCapp.config['MAIL_PASSWORD'] = 'togieyicxqyzseil'
PCapp.config['MAIL_USE_TLS'] = False
PCapp.config['MAIL_USE_SSL'] = True
mail = Mail(PCapp)

bcryptObj = Bcrypt(PCapp)

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
        action = request.form['action']
        if action == 'login':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM paciente WHERE correoPaci=%s ", [email])
            if result > 0:
                data = cur.fetchone()
                if bcrypt.checkpw(password, data['contraPaci'].encode('utf-8')):
                        #Falta agregar sessions ( los adecuados )
                        session["login"] = True
                        session['name'] = data['nombrePaci']
                        session['verificado'] = data['veriPaci']
                        flash("Inicio de Sesión exitoso", 'success')
                        cur.close()
                        return redirect(url_for('home'))
                else:
                    flash("Contraseña incorrecta", 'danger')
            else:
                
                result = cur.execute("SELECT * FROM practicante WHERE correoPrac=%s ", [email])
                if result > 0:
                    data = cur.fetchone()
                    if bcrypt.checkpw(password, data['contraPrac'].encode('utf-8')):
                            #Falta agregar sessions ( los adecuados )
                            session["login"] = True
                            session['name'] = data['nombrePrac']
                            session['verificado'] = data['veriPrac']
                            flash("Inicio de Sesión exitoso", 'success')
                            cur.close()
                            return redirect(url_for('home'))
                    else:
                        flash("Contraseña incorrecta", 'danger')
                else:
                    result = cur.execute("SELECT * FROM supervisor WHERE correoSup=%s ", [email])
                    if result > 0:
                        data = cur.fetchone()
                        if bcrypt.checkpw(password, data['contraSup'].encode('utf-8')):
                                #Falta agregar sessions ( los adecuados )                                
                                session["login"] = True
                                session['name'] = data['nombreSup']
                                session['verificado'] = data['veriSup']
                                flash("Inicio de Sesión exitoso", 'success')
                                cur.close()
                                return redirect(url_for('home'))
                        else:
                            flash("Contraseña incorrecta", 'danger')
                    else:
                        result = cur.execute("SELECT * FROM admin WHERE correoAd=%s ", [email])
                        if result > 0:
                            data = cur.fetchone()
                            if bcrypt.checkpw(password, data['contraAd'].encode('utf-8')):
                                    #Falta agregar sessions ( los adecuados )                                    
                                    session["login"] = True
                                    session['name'] = data['nombreAd']
                                    session['verificado'] = data['veriAd']
                                    flash("Inicio de Sesión exitoso", 'success')
                                    cur.close()
                                    return redirect(url_for('home'))
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
            
            edad = request.form['fecha_nacimiento']
            #Validar la edad
            if len(edad.strip()) == 0:
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
            result = cur.execute("SELECT * FROM paciente WHERE correoPaci=%s", [email])
            if result > 0:
                # Si el correo ya está registrado, mostrar un mensaje de error
                flash("El correo ya está registrado", 'danger')
                cur.close()
                return redirect(url_for('auth'))
            
            # Generar un código de verificación aleatorio
            verification_code = secrets.token_hex(3)
            cur = mysql.connection.cursor()
            
            # Guardar el usuario y el código de verificación en la base de datos
            cur.execute("INSERT INTO paciente(fechaNacPaci, nombrePaci, apellidoPPaci , apellidoMPaci, correoPaci, sexoPaci, contraPaci, codVeriPaci, activoPaci, veriPaci) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (edad, name, apellidop, apellidom, email, genero, hashed_password, verification_code, 0, 0))
            mysql.connection.commit()
            cur.close()
            
            # Enviar el código de verificación por correo electrónico
            msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[email])
            msg.body = render_template('layoutmail.html', name=name ,  verification_code=verification_code)
            msg.html = render_template('layoutmail.html', name=name ,verification_code=verification_code)
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
                        flash("Registro completado con éxito", 'success')
                        cur.close()
                        session.clear()
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
    

@PCapp.route('/')
@login_required
@verified_required
def home():
    return render_template('index.html', username=session['name'])

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