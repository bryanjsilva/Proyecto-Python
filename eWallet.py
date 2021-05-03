"""
Proyecto del curos Fundamentos de Programación en  Python - Next U

Billetera digital de Criptomonedas

Realizado por Bryan Silva
"""
"""
Vamos a crear una nueva rama de desarrollo y optimizar el código
Este código se entregó, es la primera versión
"""
"""IMPORTACIÓN DE MÓDULOS"""

import os
from IPython import get_ipython
import requests
import json
from datetime import datetime

"""DEFINICIÓN DE FUNCIONES"""

def limpiar():
    """Esta función permite limpiar las variables y la pantalla de ejecuciones anteriores"""
    #get_ipython().magic("reset -sf")
    os.system('cls')
    
def mostrarMenu():
    """Esta función muestra el menú principal y borra la pantalla"""
    print("*************************************")
    print("*           PEPE WALLET             *")
    print("*        BILLETERA DIGITAL          *")
    print("*************************************")
    print("*        ~~~~  MENÚ  ~~~~           *")
    print("*************************************")
    print("* 1. Recibir cantidad               *")
    print("* 2. Transferir monto               *")
    print("* 3. Mostrar balance de una moneda  *")
    print("* 4. Mostrar balance general        *")
    print("* 5. Historial de transacciones     *")
    print("* 6. Salir del programa             *")
    print("*************************************")
    print("*   Su código de usuario es: "+str(codigoUsuario)+"   *")
    print("*************************************")

def importarMonedas():
    """Esta función permite importar los nombres y precios de las monedas desde coinmarketcap"""
    monedasDict = {}
    monedasDict2 = {}
    simbolos = []
    precios = []
    nombres = []
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {'Accepts':'application/json','X-CMC_PRO_API_KEY':'a23aca54-d180-46af-8572-1350105903d2'}
    lista_criptos = requests.get(url,headers=headers).json()
    for moneda in lista_criptos["data"]:
        monedasDict[moneda["symbol"]]=moneda["quote"]["USD"]["price"]
        monedasDict2[moneda["name"]]=moneda["symbol"]
    simbolos = list(monedasDict.keys())
    precios = list(monedasDict.values())
    nombres = list(monedasDict2.keys())
    return simbolos, precios, nombres     # Se obtienen los datos de las monedas

def esEntero(entero):
    """Esta función valida los numeros ingresados en el menú del sistema"""
    return entero.replace(".","",0 ).isdigit()

def esMoneda(cripto):
    """Esta función valida las cantidades ingresadas"""
    return cripto in simbolos

def esNumero(cantidad):
    """Esta función valida los numeros ingresados en el menú del sistema"""
    return cantidad.replace(".","",1 ).isdigit()

def esCodigo(codigo):
    """Esta función valida los códigos de usuario"""
    if len(str(codigo)) < 5 and len(str(codigo)) > 3 and str(codigo) != str(codigoUsuario):
        return codigo.replace(".","",0 ).isdigit()
    else:
        return False

""" PROGRAMA PRINCIPAL """

limpiar()     # Se limpian las variables y la pantalla  
global codigoUsuario, historial    
codigoUsuario = 1709          # Se le asigna un código de 4 dígitos al Usuario
historial = {} # json para manejar el historial
historial['monedas'] = []
simbolos, precios, nombres = importarMonedas()     # Se importan las monedas desde coinmarketcap

cantidad = [0]*len(simbolos)           # Se crean listas para manejar las cantidades y el saldo de las monedas
saldo = [0]*len(simbolos)

while True:    # Lazo para indicar el menú luego de elegir la opción y ejecutar una acción
    mostrarMenu()
    opcion = input("->> Elija una opción: ")
    while not esEntero(opcion):
        print("->> La opción elegida es incorrecta")
        opcion = input("->> Elija una opción: ")
    else:
        opcion = int(opcion)
        if opcion == 1:
            print("->> Opción correcta")
            print("->> 1. Recibir cantidad")
            simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            while not esMoneda(simboloMoneda):
                print("Moneda inválida")
                simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            else: 
                index = simbolos.index(simboloMoneda)    # Se obtiene la posición de la moneda en la lista
                cantidadMoneda = input("->>> Ingrese el monto a recibir:  ")
                while not esNumero(cantidadMoneda):
                    print("Cantidad inválida")
                    cantidadMoneda = input("->>> Ingrese el monto a recibir: ")
                else:
                    codigoEmisor = input("->>> Ingrese el código del emisor: ")
                    while not esCodigo(codigoEmisor):
                            print("Código inválido")
                            codigoEmisor = input("->>> Ingrese el código del emisor: ")
                    else:
                        cantidad[index] += abs(float(cantidadMoneda))   # Se añade la cantidad recibida
                        saldo[index] += cantidad[index]*precios[index]  # Se calcula el nuevo saldo 
                        print("->>> Ud. ha recibido "+cantidadMoneda+" "+simboloMoneda+" del usuario "+codigoEmisor)
                        fecha = datetime.now() # Se obtiene la fecha y se registra la transacción
                        historial['monedas'].append({
                            'transaccion': 'Recibido',
                            'codigo' : codigoEmisor,
                            'movimiento' : cantidadMoneda,
                            'fecha' : fecha.strftime("%A %d %B %Y %I:%M:%S %p"),
                            'nombre' : nombres[index],
                            'cantidad' : cantidad[index],
                            'saldo' : saldo[index]})
                        with open('historial.json','w') as file:
                            json.dump(historial, file, indent = 4)
                           
        elif opcion == 2:
            print("->> Opción correcta")
            print("->> 2. Transferir monto")
            simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            while not esMoneda(simboloMoneda):
                print("Moneda inválida")
                simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            else: 
                index = simbolos.index(simboloMoneda) # Se obtiene la posición de la moneda en la lista
                cantidadMoneda = input("->>> Ingrese el monto a enviar:  ")
                while not esNumero(cantidadMoneda):
                    print("Cantidad inválida")
                    cantidadMoneda = input("->>> Ingrese el monto a enviar: ")
                else:
                    codigoReceptor = input("->>> Ingrese el código del destinatario: ")
                    while not esCodigo(codigoReceptor):
                        print("Código inválido")
                        codigoReceptor = input("->>> Ingrese el código del destinatario: ")
                    else:
                        if cantidad[index] <= 0:
                            print(" *** Saldo insuficiente ***")  # No permite realizar transacciones si no cuenta con la moneda
                        else:
                            cantidad[index] -= abs(float(cantidadMoneda))  # Se resta la cantidad enviada
                            saldo[index] -= cantidad[index]*precios[index] # Se calcula el nuevo saldo
                            print("->>> Ud. ha enviado "+cantidadMoneda+" "+simboloMoneda+" al usuario "+codigoReceptor)
                            fecha = datetime.now()   # Se registra la transacción
                            historial['monedas'].append({
                                'transaccion': 'Enviado',
                                'codigo' : codigoReceptor,
                                'movimiento' : cantidadMoneda,
                                'fecha' : fecha.strftime("%A %d %B %Y %I:%M:%S %p"),
                                'nombre' : nombres[index],
                                'cantidad' : cantidad[index],
                                'saldo' : saldo[index]})
                            with open('historial.json','w') as file:
                                json.dump(historial, file, indent = 4)            
        elif opcion == 3:
            print("->> Opción correcta")
            print("->> 3. Balance moneda")
            simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            while not esMoneda(simboloMoneda):
                print("Moneda inválida")
                simboloMoneda = input("->>> Ingrese el símbolo de la moneda: ").upper()
            else: 
                index = simbolos.index(simboloMoneda)
                if saldo[index] <= 0:
                    print(" *** No posee ninguna cantidad de esa moneda *** ") # Si no posee la moneda no aparece el saldo
                else:
                    print("Moneda: "+nombres[index]+"\nCantidad: ",cantidad[index],"\nMonto en USD: %.2f"%saldo[index])
                    # Si posee alguna cantidad de la moneda ingresada imprime los valores respectivos
        elif opcion == 4:
            print("->> Opción correcta")
            print("->> 4. Balance general")
            saldoTotal = 0
            for i in range(0,len(simbolos)): # Se buscan las monedas con saldo mayor a 0 para indicarlas
                if cantidad[i] > 0:
                    print("Moneda: "+nombres[i]+" Cantidad: ",cantidad[i],"Monto en USD: %.2f"%saldo[i])
                    saldoTotal += saldo[i] 
            print("->>> Saldo total: %.2f"%saldoTotal)
                
        elif opcion == 5:
            print("->> Opción correcta")
            print("->> 5. Historial de transacciones\n") # Se maneja un archivo json para guardar el historial
            with open('historial.json') as file:
                history = json.load(file)
            for i in range(0,len(history['monedas'])):
                print("  ->>>> ",history['monedas'][i],"\n") # Se muestran todos los datos de las transacciones
            
        elif opcion == 6:
            print("~~ Ha salido del programa ~~")    
            print("~~~~~ ¡VUELVA PRONTO! ~~~~~~")
            break # Se asegura la salida del lazo while que muestra el menú del programa
        else:
            print("->> La opción elegida es incorrecta")          
            
                  
            
        
    


