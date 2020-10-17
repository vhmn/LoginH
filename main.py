#set FLASK_APP=main.py
#set FLASK_DEBUG=1
#set FLASK_ENV=development
import Crypto 
import binascii
from Crypto.PublicKey import RSA 

# Flask
from flask import render_template, redirect, url_for, flash
from flask_pymongo import pymongo

# Local config
from app import create_app
from app.form import SignInForm, SignUpForm
from app.keygen import keygenerator
import dbconfig
import hashlib, binascii, os, sys

#importamos la clase en la que se realiza el hasheo y la verificación
from custom_hash import hasheo


app = create_app()

@app.route('/', methods=['GET','POST'])
def signin():
    data_form = SignInForm()
    context = {
        'title':'Inicio de Sesión',
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

        #Creamos un objeto de la clase hasheo, se envia password y nombre de usuario
        p1 = hasheo(pass_ingresado, username) 
        #Se utiliza el método creado para verificar que sea el mismo pass
        pwdhash = p1.verificar()

        if pass_almacenado == pwdhash:
            #Si se comprueba que el password es igual al guardado, se redirige a inicio exitoso
            keys = keygenerator()
            return render_template('success.html', **keys)
        else:
            #Si el password no coincide se envia un mensaje de error
            flash('Contraseña incorrecta')
    return render_template('signin.html', **context)

@app.route('/signup', methods=['GET','POST'])
def signup():
    data_form = SignUpForm()
    context={
        'title':'Crear cuenta',
        'data_form': data_form,
    }
    #En caso de validar los datos, se almacenan en la variable designada
    if data_form.validate_on_submit():
        username = data_form.username.data
        email = data_form.email.data
        name = data_form.name.data
        password = data_form.password.data
        c_password = data_form.retry_password.data
        # Se verifica que el pass y su confirmación coincidan
        if password == c_password:

            p = hasheo(password, username) 
            hash_ = p.hash()
                        
            #insertamos los datos en la colección de MongoDB
            dbconfig.db_users.users.insert_one({
                'username': username,
                'email': email,
                'name' : name,
                'password' : hash_,
            })
            return redirect('/')
        else:
            #Si no coinciden los pass se redirige y muestra mensaje de error
            flash('Las contraseñas no coinciden')

    return render_template('signup.html', **context)

#Ruta para inicio de sesión exitoso
@app.route('/success')
def success():
    keys = keygenerator()
    return render_template('success.html', **keys)