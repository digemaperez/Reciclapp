# -*- coding: utf-8 -*-
### Decidimos por una cuestión de tiempos, enfocarnos en la funcionalidad del sistema,
### y no en separar en distintos paquetes las clases, como indican las buenas prácticas.

import psycopg2
from psycopg2 import Error    
from nltk import word_tokenize, Text, FreqDist
from nltk.chat.util import Chat, reflections
import re
import random
from datetime import datetime
import smtplib, ssl
from email.message import EmailMessage




mensaje_uno = "Hola, soy Recibot, aquí podrás aprender e informarte sobre todo lo que tenga que ver con el Reciclado en Origen"
mensaje_dos = """¿Querés información sobre que es reciclable o no (Ingresa: "Info")
Sobre los Puntos Limpio (Ingresa "Punto Limpio")
Querés mandar una Orden para que retiren tus reciclados (Ingresa: "Retirar")
Para finalizar ingresá: quit"""        





    
def loguear_usuario(match):
    dni = match.string
    
    while not es_valido(dni):
        dni = input("Ingrese un dni válido: ")
    
    inicio.login(dni)
    print("Hola", inicio.usuario_actual.nombre, " " )
    

def es_valido( dni):
        if dni.isnumeric() and (len(dni) > 6) and (len(dni) < 9):
            return True
        return False


def retirar_carton(match):
    
    ### en esta función se espera que en la BBDD la ong de carton sea la de id = 1
    
    usuario = inicio.usuario_actual
    ong = 1
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño (en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "carton", estado)
    inicio.ordenes.append(orden)
    




def retirar_plastico(match):
    
    ### en esta función se espera que en la BBDD la ong de plástico sea la de id = 2
    
    usuario = inicio.usuario_actual
    ong = 2
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "plastico", estado)
    inicio.ordenes.append(orden)
    



def retirar_vidrio(match):
    
    
    ### en esta función se espera que en la BBDD la ong de vidrio sea la de id = 3

    usuario = inicio.usuario_actual
    ong = 3
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "vidrio", estado)
    inicio.ordenes.append(orden)
    
    # enviar mails para la ong con la orden
    
    
def retirar_telgopor(match):
    
    ### en esta función se espera que en la BBDD la ong de telgopor sea la de id = 4


    usuario = inicio.usuario_actual
    ong = 4
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "telgopor", estado)
    inicio.ordenes.append(orden)
    


def retirar_organico(match):
    
    ### en esta función se espera que en la BBDD la ong de orgánicos sea la de id = 5


    usuario = inicio.usuario_actual
    ong = 5
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "organico", estado)
    inicio.ordenes.append(orden)

def retirar_tetrabrik(match):
    
    ### en esta función se espera que en la BBDD la ong de tetrabrik sea la de id = 6


    usuario = inicio.usuario_actual
    ong = 6
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "tetrabrik", estado)
    inicio.ordenes.append(orden)
    

def retirar_papel(match):

    ### en esta función se espera que en la BBDD la ong de papel sea la de id = 7
    
    usuario = inicio.usuario_actual
    ong = 7
    fecha_alta = datetime.now()
    tamaño = input("Ingrese el tamaño(en kg): ")
    fecha_retiro = input("Ingrese la fecha de retiro: ")
    estado = "En espera"
    orden = usuario.crear_orden(tamaño, fecha_alta, fecha_retiro, ong, "papel", estado)
    inicio.ordenes.append(orden)

class MyChat(Chat):
    etiquetas = {}

    def __init__(self, pairs, reflections={}):

        # add `z` because now items in pairs have three elements
        self._pairs = [(re.compile(x, re.IGNORECASE), y, z) for (x, y, z) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()
        
        
    def respond(self, str):

        """
        Redefinimos el método que genera la respuesta.
        El objetivo es poder hacer el análisis de palabras.
        :type str: str
        :param str: Cadena a ser mapeada para dar respuesta
        :rtype: str
        """

        flag_match = True
        if(flag_match):
            # desarma una cadena en tokens (palabras o  etiquetas) y uso un diccionario para
            # contar ocurrencias.
            tokens = word_tokenize(str)
            for tok in tokens:
                if tok not in self.etiquetas:
                    self.etiquetas[tok] = 1
                else:
                    self.etiquetas[tok] += 1

            flag_match = False

        # Bucle que verifica si el parámetro hace match con alguna de las reglas.
        # En base a esto elabora la respuesta y llama a una función si aplica.

        for (pattern, response, callback) in self._pairs:
            match = pattern.match(str)

            if match:

                resp = random.choice(response)
                resp = self._wildcards(resp, match)

                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'

                # run `callback` if exists
                if callback: # eventually: if callable(callback):
                    callback(match)

                return resp
            
mis_reflexions = {
    "ir": "fui",
    "hola": "hey"
    }

        
pares = [
        [
            r"INFO",
            ["""Los siguientes artículos son reciclables: PAPEL, CARTÓN, PLÁSTICO, TELGOPOR, TETRA BRIK, VIDRIO, ORGÁNICO
Recordá, que se guardan todos separados, y después los podés llevar al Punto Limpio o solicitar su retiro del domicilio""" + mensaje_dos,],
            None
        ],
        [
            r"PUNTO LIMPIO",
            ["""Podes llevar los residuos reciclables a: 
    Punto Limpio Estación Centro: Santamarina 460 
    Punto Limpio Estación Norte: Darragueira y Jurado
    Punto Limpio Estación Oeste: Almafuerte e Iraola
    Para más información podés ingresar al facebook: https://www.facebook.com/puntolimpiotandil/""", ],
            None
        ],
        [
            r"que(.*)reciclar(.*)",
            ["""Los siguientes artículos son reciclables: PAPEL, CARTÓN, PLÁSTICO, TELGOPOR, TETRA BRIK, VIDRIO, ORGÁNICO
Recordá, que se guardan todos separados, y después los podés llevar al Punto Limpio o solicitar su retiro del domicilio/n""" + mensaje_dos,],
            None
        ],
        [
            r"0",
            ["Muchas gracias por comunicarse con nosotros cualquier consulta escribanos al mail: recibot@tandil.com.ar", ],
            None
        ],
        [
            r"(.*)RETIRAR(.*)",
            ["Ingrese su número de dni", ],
            None
        ],
        [
            r"(.*)1|2|3|4|5|8|6|7(.*)",
            ["Indicanos el producto que querés que vayamos a buscar: PAPEL, CARTÓN, PLÁSTICO, TELGOPOR, TETRA BRIK, VIDRIO, ORGÁNICO", ],
            loguear_usuario
        ],
        
        [
            r"(.*)telgopor(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_telgopor
        ],
        [
            r"(.*)carton(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_carton
        ],
        [
            r"(.*)vidrio(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_vidrio
        ],
        [
            r"(.*)papel(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_papel
        ],
        [
            r"(.*)plastico(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_plastico
        ],
        [
            r"(.*)organico(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_organico
        ],
                        [
            r"(.*)tetra(.*)",
            ["Muchas gracias, ya enviamos el mail. En breve se comunicarán con Ud." + mensaje_dos,],
            retirar_tetrabrik
        ],
    ]
        
        

        



### A continuación se definen las clases que interactuan en el sistema

class Usuario():
  
  
    def __init__(self, dni, nombre, apellido, direccion, mail):
        self.dni = dni 
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.mail = mail
        
    
    def crear_orden(self, tamaño, fecha_alta, fecha_retiro,ong_id, ong_tipo, estado):
        orden = Orden(self.dni,tamaño, fecha_alta,fecha_retiro,  ong_id, ong_tipo, estado)
        return orden
    
        
    
    



class Orden():
    
### La clase orden no lleva id, porque al persistir las ordenes, se crea el id en la base de datos
### por ser de tipo autoincremental 
    
    def __init__ (self, usuario_dni, tamaño, fecha_alta, fecha_retiro,  ong_id, ong_tipo, estado):
        self.usuario_dni = usuario_dni
        self.tamaño = tamaño
        self.fecha_alta = fecha_alta
        self.fecha_retiro = fecha_retiro
        self.ong_id = ong_id
        self.ong_tipo = ong_tipo
        self.estado = estado


    

class ONG():

    def __init__(self, id, nombre, tipo_reciclaje, mail):
        self.id = id
        self.nombre = nombre
        self.tipo_reciclaje = tipo_reciclaje
        self.mail = mail
        
    


class DB():

    def __init__(self, parent=None):
        self.cursor = self.db_connect()

    def db_connect(self):
        try:
            # configurar su base de datos 
            connection = psycopg2.connect(user="postgres",
                                            password="postgres",
                                            host="localhost",
                                            port="5432",
                                            database="Reciclapp")

            # esto conecta y retorna el cursor
            self.connect = connection
            cursor = connection.cursor()
            return cursor

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)



#### Clase main del sistema

class Sistema():
    
    usuarios = {}
    usuarios_nuevos = {}
    ongs = {}
    usuario_actual = None
    ordenes = []
    
    def __init__(self):
        usuarios = self.cargar_usuarios()
        ongs = self.cargar_ongs()


    def cargar_ongs(self):
        db = DB()
        db.cursor.execute("SELECT * FROM ONG;")
        # Fetch result
        records = db.cursor.fetchall()
        for row in records:
            ong = ONG(row[0],row[1], row[2], row[3])
            self.ongs[ong.id] = (ong)

   

    def cargar_usuarios(self):
        db = DB()
        db.cursor.execute("SELECT * FROM Usuario;")
        # Fetch result
        records = db.cursor.fetchall()
        for row in records:
            if not(row[0]):
                next
            else:
                usuario = Usuario(row[0],row[1],row[2], row[3], row[4])
                self.usuarios[usuario.dni] = (usuario)

          
            
    def leer_usuario(self, dni):
        if (es_usuario(dni)):
            print(usuario.dni)
        else:
            print("El usuario no esta ingresado aun.")
       
  
    def es_usuario(self, dni):

        if  dni in self.usuarios.keys():
            return True
        else:
            return False
        
    
  
    def login(self, dni):
        
        if self.es_usuario(int(dni)):
            self.usuario_actual = self.usuarios[int(dni)]
            
        else:
            self.crear_usuario(int(dni))
            self.usuario_actual = self.usuarios_nuevos[int(dni)]
        
    
    def crear_usuario(self, dni):
        
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese su apellido: ")
        direccion  = input("Ingrese la direccion: ")
        mail = input ("Ingrese su mail: ")
        usuario = Usuario(dni, nombre, apellido, direccion, mail)
        self.usuarios_nuevos [dni] = usuario
    
    
    def persistir_usuarios(self):
        
        db = DB()
        
        # Fetch result
        records = self.usuarios_nuevos
        for row in records:
            nombre = (self.usuarios_nuevos[row].nombre)
            apellido = (self.usuarios_nuevos[row].apellido)
            direccion = (self.usuarios_nuevos[row].direccion)
            mail = (self.usuarios_nuevos[row].mail)
            db.cursor.execute("INSERT INTO usuario VALUES ('{}', '{}', '{}', '{}', '{}')".format(row, nombre, apellido, direccion, mail))
            db.connect.commit()
    
    def persistir_ordenes(self):
         
        db = DB()
        records = self.ordenes
        for row in records:
       
            db.cursor.execute("INSERT INTO orden (usuario_dni, tamaño, fecha_alta, fecha_retiro, ong_id, ong_tipo_reciclaje, estado)VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(row.usuario_dni,row.tamaño,row.fecha_alta,row.fecha_retiro,row.ong_id,row.ong_tipo, row.estado))
            db.connect.commit()
            
    def enviar_correo(self):

        
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login('reciclatandil@gmail.com', 'mariapilar')


        for row in self.ordenes:
            contador = 1
            if row.usuario_dni in self.usuarios:
                direccion = self.usuarios[row.usuario_dni].direccion
            else:
                direccion = self.usuarios_nuevos[row.usuario_dni].direccion
            mensaje = EmailMessage()
            mensaje['subject'] = 'Ordenes de retiro'

            mensaje.set_content("Orden {}: Usuario: {}, Direccion: {}, Tamaño: {}, Fecha de Alta: {}, Fecha de Retiro: {}, Reciclado: {}, Estado: {} ".format(contador, row.usuario_dni, direccion, row.tamaño,row.fecha_alta,row.fecha_retiro,row.ong_tipo, row.estado))
            contador += 1
            reciever_email = self.ongs[row.ong_id].mail
            smtpserver.sendmail('reciclatandil@gmail.com', reciever_email, mensaje.as_string())
            

            
                




def chatear(mensaje_uno, mensaje_dos):
    
    
    print(mensaje_uno)
    print(mensaje_dos)
    chat = MyChat(pares, mis_reflexions)
    chat.converse()



if __name__ == "__main__":
  inicio = Sistema()
  chatear(mensaje_uno, mensaje_dos)
  inicio.persistir_usuarios()
  inicio.persistir_ordenes()
  inicio.enviar_correo()
  

