#set FLASK_APP=main.py
#set FLASK_DEBUG=1
#set FLASK_ENV=development

# Flask
from flask import render_template, redirect, url_for, flash
from flask_pymongo import pymongo

# Local config
from app import create_app
from app.form import SignInForm, SignUpForm
import dbconfig
import hashlib, binascii, os, sys

#importamos la clase en la que se realiza el hasheo y la verificación
from custom_hash import hasheo


app = create_app()


@app.route('/', methods=['GET','POST'])
def signin():
    data_form = SignInForm()
    context = {
        'title':'Sign In',
        'data_form': data_form
    }
    if data_form.validate_on_submit():
        #Las variables de nombre de usuario y password toman los valores ingresados por el usuario en el formulario
        username= data_form.username.data
        pass_ingresado = data_form.password.data 
        
        #las variables de usuario y contraseña se obtienen de la base de datos
        user = dbconfig.db_users.users.find_one({'username':username})
        pass_almacenado = user['password']
        pass_almacenado = pass_almacenado[64:]

        #Creamos un objeto de la clase hasheo, para poder hacer uso de sus métodos
        p1 = hasheo(pass_ingresado, username) 
        pwdhash = p1.verificar()

        if pass_almacenado == pwdhash:
            #Si se comprueba que el password ingresado es igual al almacenado se redirige a inicio exitoso
            return redirect('/success')
        else:
            #Si el password no coincide se envia un mensaje de error
            flash('Incorrect Password')
    # Y se redirige a la pantalla de registro
    return render_template('signin.html', **context)

@app.route('/signup', methods=['GET','POST'])
def signup():
    data_form = SignUpForm()
    context={
        'title':'Sign Up',
        'data_form': data_form,
    }

    if data_form.validate_on_submit():
        username = data_form.username.data
        email = data_form.email.data
        name = data_form.name.data
        password = data_form.password.data
        c_password = data_form.retry_password.data

        if password == c_password:

            #Generamos la sal a partir de urandom, el cual creara un objeto de bytes aleatorios
            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            #Creamos el hash, especificando el tipo de algoritmo que se usara, la codificación, 
            # la sal y el número de iteraciones
            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
            #Cambiamos a una representación hexadecimal
            pwdhash = binascii.hexlify(pwdhash)
            # Concatenamos la sal y el hash y los codificamos en un formato para almacenar
            hash_ = (salt + pwdhash).decode('ascii')
            
            #insertamos los datos en la colección de MongoDB
            dbconfig.db_users.users.insert_one({
                'username': username,
                'email': email,
                'name' : name,
                'password' : hash_,
            })
            return redirect('/')
        else:
            flash('Passwords do not match')

    return render_template('signup.html', **context)


@app.route('/success')
def success():
    return render_template('success.html')