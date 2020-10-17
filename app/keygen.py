"""Importa las librerias de Crypto y Binascii, que serviran para encripytar y 
convertir una cadena a binario"""
import Crypto 
import binascii 
 
#Importa la funcion RSA de la libreria PublicKey de Crypto
from Crypto.PublicKey import RSA 

"""Se crea una funcion para generar llaves aleatorias cada vez
que se acceda a ella"""
def keygenerator(): 

#Se crea un objeto de generador random 
    random_generator = Crypto.Random.new().read 

"""#Se genera una llave privada de 1024 bytes con el objeto de generador 
random, la cual no se almacena en una variable directamente, si no
que es almacena en una direccion de memoria de la PC, y luego 
genera una llave publica ligada a la llave privada que guarda
en una direccion de memoria de la PC"""
    private_key = RSA.generate(1024, random_generator) 
    public_key = private_key.publickey() 

"""Exportan las llaves a una variable en formato DER para que sean
visibles en terminal"""
    private_key = private_key.exportKey(format='DER') 
    public_key = public_key.exportKey(format='DER') 

"""Convierte las llaves de formato DER a binario, y de binario
a UTF-8""" 
    private_key = binascii.hexlify(private_key).decode('utf-8') 
    public_key = binascii.hexlify(public_key).decode('utf-8') 

"""Se guardan las llaves en formato UTF-8 en un directorio para
ser enviadas más facilmente"""
    keys = {
                'public': public_key ,
                'private': private_key
            }
#Se manda el directorio con las llaves a la pagina donde se van a mostrar            
    return(keys)
