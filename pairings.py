#!/bin/python3

import xlrd
import sys
from tabulate import tabulate

# Check if file is provided
if len(sys.argv) != 2:
    print("[*] Usage: python3 pairings.py <path_to_xls_file_with_pairings>")
    print ("[!] You must specify xls file as an argument")
    exit()
else:
    file = sys.argv[1]

# Global variables
generar_blacklist_times_run = 0
blacklisted_destinations = []
generar_whitelist_times_run = 0
whitelisted_destinations = []
lista_destinos_interesantes_detectados = [] # soft blacklist

# First of all, generate an array called "all_pairings" where all pairings are stored for easy processing
all_pairings = []
sheetfile = xlrd.open_workbook(file)
sh = sheetfile.sheet_by_index(0)
for rownum in range(sh.nrows):
    raw_pairing=sh.cell(rownum,0),sh.cell(rownum,1)
    all_pairings.append(str(raw_pairing).replace('text:', ''))

for pairing in all_pairings:
    print(pairing + "\r\n")


def showHelpPanel():
    firstRow = ["Opción", "Función"]
    opciones = [    
        [1, "Filtrar líneas tengn algún destino distinto a los especificados (soft blacklist)"],
        [2, "Filtrar líneas que sólo tengan destinos destinos a los especificados (hard blacklist)"],
        [3, "Filtrar líneas que pasen por destinos concretos (soft whitelist)"],
        [4, "Filtrar líneas que sólo pasen por destinos concretos (hard whitelist)"],
        [0, "Salir"]
    ]
    print(tabulate(opciones, headers=firstRow, tablefmt="grid"))
    user_option = int(input("Escriba su número de opción: "))
    if user_option == 1:
        soft_blacklist()
    elif user_option == 2:   
        hard_blacklist()
    elif user_option == 3:
        soft_whitelist()
    elif user_option == 4:
        hard_whitelist()
    else:
        exit()

def generar_blacklist():
    global blacklisted_destinations
    global generar_blacklist_times_run
    blacklisted_destinations_by_default = ["MAD", "BCN", "SCQ", "OVD", "LCG", "BIO", "VGO", "ORY", "BRU", "ARN", "HEL", "LHR", "GVA", "ZRH", "VCE", "FCO", "VIE", "LIS", "OPO", "OSL", "MXP", "LIN", "DUS", "HAM", "MUC", "RAK", "DSS"]
    if generar_blacklist_times_run == 0:
        print("\r\n[*] Por defecto, la lista de aeropuertos a ignorar es: " + str(blacklisted_destinations_by_default))
        print("[!] Para generar tu propia lista, introduce uno a uno el IATA de cada aeropuerto que quieres ignorar.")
        print("[!] Para aceptar los aeropuertos por defecto, pulsa intro.\r\n")
    user_input = input("[->] Añade un aeropuerto o pulsa intro para aceptar: ")
    generar_blacklist_times_run = generar_blacklist_times_run + 1
    if user_input:
        blacklisted_destinations.append(user_input.upper())
        print ("\t [-] Lista de aeropuertos a ignorar: " + str(blacklisted_destinations))
        generar_blacklist()
    else:
        # Si hemos definido aeropuertos a evitar, cerrar la lista
        if blacklisted_destinations:
            print("\r\n La lista de aeropuertos ignorados: " + str(blacklisted_destinations))
            return
        # Si no hay input ni se ha hecho anteriormente, usar la lista default                
        else:
            blacklisted_destinations = blacklisted_destinations_by_default
            print("\r\n La lista de aeropuertos ignorados: " + str(blacklisted_destinations))
    return(blacklisted_destinations)

def generar_whitelist():
    global whitelisted_destinations
    global generar_whitelist_times_run
    whitelisted_destinations_by_default = ["NCE", "FNC", "PDL", "XRY", "CFU"]
    if generar_whitelist_times_run == 0:
        print("\r\n[*] Por defecto, la lista de aeropuertos a incluir es: " + str(whitelisted_destinations_by_default))
        print("[!] Para generar tu propia lista, introduce uno a uno el IATA de cada aeropuerto que quieres incluir en la lista blanca.")
        print("[!] Para aceptar los aeropuertos por defecto, pulsa intro.\r\n")
    user_input = input("[->] Añade un aeropuerto o pulsa intro para aceptar: ")
    generar_whitelist_times_run = generar_whitelist_times_run + 1
    if user_input:
        whitelisted_destinations.append(user_input.upper())
        print ("\t [-] Lista de aeropuertos a incluir: " + str(whitelisted_destinations))
        generar_whitelist()
    else:
        # Si hemos definido aeropuertos a evitar, cerrar la lista
        if whitelisted_destinations:
            print("\r\n La lista de aeropuertos a incluir: " + str(whitelisted_destinations))
            return
        # Si no hay input ni se ha hecho anteriormente, usar la lista default                
        else:
            whitelisted_destinations = whitelisted_destinations_by_default
            print("\r\n La lista de aeropuertos a incluir: " + str(whitelisted_destinations))
    return(whitelisted_destinations)

def soft_blacklist():
    # Si no se ha generado la blacklist, hacerlo
    if not blacklisted_destinations:
        generar_blacklist()
    for line in all_pairings:
        destinos_de_la_linea = []
        destinos_interesantes_de_la_linea = []
        for word in line.split():
            if len(word) == 3 and "*" not in word:
                destinos_de_la_linea.append(word)
    #     #print("Linea original: " + linea_raw)
    #     #print ("Destinos detectados: " + str(destinos_de_la_linea))
        for destino in destinos_de_la_linea:
            if destino not in blacklisted_destinations and destino not in destinos_interesantes_de_la_linea:
                destinos_interesantes_de_la_linea.append(destino)
                if destino not in lista_destinos_interesantes_detectados:
                    lista_destinos_interesantes_detectados.append(destino)
            else:
                continue
        if len(destinos_interesantes_de_la_linea) == 1:
            print("[*] Linea buena detectada!! ---> " + line + " (Destino detectado: " + str(destinos_interesantes_de_la_linea) + ")\r\n")
        elif len(destinos_interesantes_de_la_linea) >= 2:
            print("[*] Linea buena detectada!! ---> " + line + " (Destinos detectados: " + str(destinos_interesantes_de_la_linea) + ")\r\n")
    print("Lista de destinos interesantes detectados: " + str(lista_destinos_interesantes_detectados))
    return(lista_destinos_interesantes_detectados)

def hard_blacklist():
    # Si no se ha generado la blacklist, hacerlo
    if not blacklisted_destinations:
        generar_blacklist()
    # Eliminar MAD de la blacklist, ya que, si hard blacklisteamos Madrid, ninguna línea es válida
    if "MAD" in blacklisted_destinations:
        blacklisted_destinations.remove("MAD")
    for line in all_pairings:
        destinos_de_la_linea = []
        for word in line.split():
            if len(word) == 3 and "*" not in word:
                destinos_de_la_linea.append(word)
        matches = list(set(blacklisted_destinations) & set(destinos_de_la_linea))
        if matches: 
            continue
        else:
            print("Esta línea no tiene ningún destino blacklisteado: " + line)

def soft_whitelist():
    if not whitelisted_destinations:
        generar_whitelist()
    if "MAD" in whitelisted_destinations:
        whitelisted_destinations.remove("MAD")
    for line in all_pairings:
        destinos_de_la_linea = []
        for word in line.split():
            if len(word) == 3 and "*" not in word:
                destinos_de_la_linea.append(word)
    #print(str(destinos_de_la_linea))
        for destino in destinos_de_la_linea:
            if destino in whitelisted_destinations:
                print("Línea: " + line + " (Destino coincidente: " + destino + ")")
                break
            else:
                continue

def hard_whitelist():
    matching_lineas = 0
    if not whitelisted_destinations:
        generar_whitelist()
    for line in all_pairings:
        destinos_de_la_linea = []
        for word in line.split():
            if len(word) == 3 and "*" not in word:
                destinos_de_la_linea.append(word)
    #print(str(destinos_de_la_linea))
        if set(destinos_de_la_linea).issubset(set(whitelisted_destinations)):
            print("Línea: " + line)
            matching_lineas += 1
        else:
            continue
        if matching_lineas == 1:
            print("No hay ninguna línea que pase exclusivamente por los destinos especificados")

showHelpPanel()

# destinos_de_la_linea = ["MAD", "LCG", "MAD", "VIE", "VIE"]
# whitelisted_destinations = ["VCE", "CFU", "FNC", "PDL"]