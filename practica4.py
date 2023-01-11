#!/usr/bin/python3
import os

opcion = 0
USER = "rcp"
PASSWORD = "rcp"

def limpiar_pantalla():
    """ Limpiamos la terminal """
    os.system("clear")
    
def desplegar_menu():
    """ Mostramos el menú al usuario """
    limpiar_pantalla()
    print("1. Generar startup-config")
    print("2. Transferir archivos")
    print("3. Salir\n")

    return int(input("\nOPCION: "))


""" Programa principal """
while opcion != 3:
    opcion = desplegar_menu()
    
limpiar_pantalla()