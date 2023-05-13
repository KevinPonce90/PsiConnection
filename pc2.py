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
PCapp.config['MYSQL_DB']                = 'rm'
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



#El Def auth controla si inicia sesion o es nuevo usuario

@PCapp.route('/pythonlogin/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'login':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM user WHERE correoAd=%s ", [email])
            if result > 0:
                data = cur.fetchone()
                if bcrypt.checkpw(password, data['passAd'].encode('utf-8')):
                    if data['verificado'] == 1:
                        #Falta agregar sessions ( los adecuados )
                        
                        session["login"] = True
                        session['name'] = data['nombreAd']
                        flash("Inicio de Sesión exitoso", 'success')
                        cur.close()
                        return redirect(url_for('home'))
                    else:
                        # El usuario no está verificado, mostrar mensaje de error
                        flash("Debes verificar tu cuenta antes de iniciar sesión", 'warning')
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
            
            email = request.form['email']
             # Validar el correo electrónico
            if len(email.strip()) == 0:
                flash("Por favor ingrese su correo electrónico", 'danger')
                return redirect(url_for('auth'))
            
            if not re.match(r'^[^\s@]+@(udg\.com\.mx|alumnos\.udg\.mx|academicos\.udg\.mx)$', email):
                # Si el correo electrónico no es válido, mostrar un mensaje de error
                flash("Por favor ingrese un correo electrónico válido con uno de los dominios permitidos", 'danger')
                return redirect(url_for('auth'))
            

            tel = request.form['phone']
          
            
            password = request.form['password']
            if len(password.strip()) < 8:
                flash("Por favor ingrese una contraseña de al menos 8 caracteres", 'danger')
                return redirect(url_for('auth'))
            
            hashed_password = bcryptObj.generate_password_hash(password).decode('utf-8')
            
            # Verificar si el correo ya está registrado en la base de datos
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM user WHERE correoAd=%s", [email])
            if result > 0:
                # Si el correo ya está registrado, mostrar un mensaje de error
                flash("El correo ya está registrado", 'danger')
                cur.close()
                return redirect(url_for('auth'))
            
            # Generar un código de verificación aleatorio
            verification_code = secrets.token_hex(3)
            cur = mysql.connection.cursor()
            
            # Guardar el usuario y el código de verificación en la base de datos
            cur.execute("INSERT INTO user(nombreAd, correoAd, telCelAd, passAd, verification_code) VALUES(%s, %s, %s, %s, %s)", (name, email, tel, hashed_password, verification_code))
            mysql.connection.commit()
            cur.close()
            
            # Enviar el código de verificación por correo electrónico
            msg = Message('Código de verificación', sender=PCapp.config['MAIL_USERNAME'], recipients=[email])
            msg.body = render_template('layoutmail.html', name=name ,  verification_code=verification_code)
            msg.html = render_template('layoutmail.html', name=name ,verification_code=verification_code)
            mail.send(msg)
            
            # Redirigir al usuario a la página de verificación
            flash("Revisa tu correo electrónico para obtener tu código de verificación", 'success')
            return redirect(url_for('verify'))

    return render_template('login.html')


@PCapp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        # Obtener el código ingresado por el usuario
        user_code = request.form['code']
        
        # Verificar si el código es correcto
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE verification_code=%s", [user_code])
        if result > 0:
            # Si el código es correcto, actualizar el campo "verificado" a 1
            cur.execute("UPDATE user SET verificado = %s WHERE verification_code = %s", (1, user_code))
            mysql.connection.commit()
            flash("Registro completado con éxito", 'success')
            cur.close()
            return redirect(url_for('home'))
        else:
            flash("Código de verificación incorrecto", 'danger')
            cur.close()
        
    return render_template('verify.html')



@PCapp.route('/')
def home():
    # Check if user is loggedin
    if 'login' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['name'])
    
    # User is not loggedin redirect to login page
    return redirect(url_for('auth'))


@PCapp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('login', None)
   session.pop('userid', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('auth'))

@PCapp.route('/protected')
@login_required
def protected ():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada </h1>", 404

if __name__ == '__main__':
    PCapp.secret_key = '123'
    csrf.init_app(PCapp)
    PCapp.register_error_handler(401,status_401)
    PCapp.register_error_handler(404,status_404)
    PCapp.run(port=3000,debug=True)