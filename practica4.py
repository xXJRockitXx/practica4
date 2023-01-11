#!/usr/bin/python3
import os
from telnetlib import Telnet
import time
from ftplib import FTP

USER = "rcp"
PASSWORD = "rcp"

def limpiar_pantalla():
    """ Limpiamos la terminal """
    os.system("clear")
    
def pausar():
    """ Esperamos a que se presione ENTER para continuar
    con el programa """
    input("\nPRESIONE ENTER PARA CONTINUAR...")
    
def desplegar_menu():
    """ Mostramos el menú al usuario """
    limpiar_pantalla()
    print("Seleccione una opción: \n")
    print("1. Generar startup-config")
    print("2. Transferir archivos")
    print("3. Salir")

    return int(input("\nOPCION: "))

def generar_startup_config(host):
    limpiar_pantalla()
    
    with Telnet(host, 23) as tn:
        tn.read_until(b'User: ', float(10))
        print(tn.read_eager().decode('ascii') + "-----")
        print(tn.read_eager().decode('ascii'))
        tn.write(USER.encode("ascii") + b'\n')
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")

        tn.read_until(b'Password: ', float(10))
        tn.write(PASSWORD.encode("ascii") + b'\n')
        print(tn.read_eager().decode('ascii'))
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")

        tn.write(b'en\n')
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")
        tn.write(b'config\n')
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")

        tn.write(b'service ftp\n')
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")

        tn.write(b'copy run start\n')
        time.sleep(10)
        print(tn.read_eager().decode('ascii') + "-----")
        
    print("\nstartup-config generado...")
    pausar()

def solicitar_host():
    limpiar_pantalla()
    print("Ingresa la ip del host: \n")
    return input("IP: ")

def conectar_ftp(host ):
    ftp = FTP(host)
    ftp.login(user = USER, passwd = PASSWORD)
    print("\n" + ftp.getwelcome())
    return ftp

def ftp_enviar():
    host = solicitar_host()
    limpiar_pantalla()
    
    print("ENVIO DE ARCHIVOS POR FTP\n")
    
    archivoLocal = input("Archivo local: ")
    archivoRemoto = input("Archivo remoto: ")
    
    """ ftp = conectar_ftp(host) """
    ftp = FTP(host)
    ftp.login(user = USER, passwd = PASSWORD)
    print("\n" + ftp.getwelcome())
    
    with open(archivoLocal, "rb") as archivo:
        ftp.storbinary("STOR " + archivoRemoto, archivo)
    
    print("\nArchivo enviado...")
    ftp.quit()
    pausar()
    
def ftp_recibir():
    host = solicitar_host()
    limpiar_pantalla()
    
    print("RECIBIR DE ARCHIVOS POR FTP\n")
    
    archivoRemoto = input("Archivo remoto: ")
    archivoLocal = input("Archivo local: ")
    
    ftp = FTP(host)
    ftp.login(user = USER, passwd = PASSWORD)
    print("\n" + ftp.getwelcome())
    
    with open(archivoLocal, "wb") as archivo:
        ftp.retrbinary("RETR " + archivoRemoto, archivo.write, 1024)
    
    print("\nArchivo recibido...")
    ftp.quit()
    pausar()

def trasferir_archivos():
    limpiar_pantalla()
    print("Transmision de archivos por protocolo FTP. Qué quieres hacer?\n")
    print("1. Enviar")
    print("2. Recibir\n")
    opc = int(input("OPCION: "))
    
    if opc == 1:
        ftp_enviar()
    else:
        ftp_recibir()

""" Programa principal """
opcion = 0

while opcion != 3:
    opcion = desplegar_menu()
    
    if opcion == 1:
        """ Con TELNET generamos de manera remota el archivo de configuracion """
        host = solicitar_host()
        generar_startup_config(host)

    elif opcion == 2:
        """ Transferimos archivos por protoclo ftp """
        trasferir_archivos()
        
        
limpiar_pantalla()