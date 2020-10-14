# Flask
from flask import render_template, redirect, url_for, flash
from flask_pymongo import pymongo

# Local config
from app import create_app
from app.form import SignInForm, SignUpForm
import dbconfig, main
import hashlib, binascii, os, sys


class hasheo:

    """ Implementacion para hashear passwords """

    def __init__(self, password, username):
        self.password = password
        self.username = username

    def hash(self):
        #Generamos la sal a partir de urandom, el cual creara un objeto de bytes aleatorios
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        #Creamos el hash, especificando el tipo de algoritmo que se usara, la codificación, 
        # la sal y el número de iteraciones
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        #Cambiamos a una representación hexadecimal
        pwdhash = binascii.hexlify(pwdhash)
        # Concatenamos la sal y el hash y los codificamos en un formato para almacenar
        return (salt + pwdhash).decode('ascii')

    def verificar(self):

        #User es un diccionario con los datos con el mismo nombre del usuario ingresado
        user = dbconfig.db_users.users.find_one({'username':self.username})
        #Se asigna a una variable el password contenido en el diccionario
        pass_almacenado = user['password']
        #la sal es igual a los ultimos 64 caracteres
        salt = pass_almacenado[:64]
        #hasheamos el password que acaba de ingresar el usuario
        # con la sal que ya teniamos almacenada
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash


