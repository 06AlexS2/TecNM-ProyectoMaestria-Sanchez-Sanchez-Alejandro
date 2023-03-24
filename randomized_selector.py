#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 13:12:40 2022

@author: alexs2
"""

##ARCHIVO PARA GENERAR LA ASIGNACION DE PARTICIPANTES DE MANERA ALEATORIA EN LOS GRUPOS DESIGNADOS PARA EL PROTOCOLO

#SE IMPORTAN LAS LIBRERIAS NECESARIAS, RANDOM PARA GENERAR ALEATORIZACION, CSV PARA MANEJO DE ARCHIVOS CSV Y OS PARA MANEJO DE CARPETAS

import random
import csv
import os

#SE VERIFICA SI EXISTE EL ARCHIVO 
file_exists = os.path.isfile("student_list.csv")

#VARIABLES PARA EL CICLO:
#FLAG ES PARA INDICAR CUANDO GUARDAR Y CERRAR EL ARCHIVO
flag = True
#NUMERO DE ESTUDIANTES REGISTRADOS (2)
n = 0
#NOMBRES DE LOS ESTUDIANTES
student_names = []
#NOMBRES DE LAS COLUMNAS
headers = ["Nombre", "Apellido", "Activo", "Control"]

print("FAVOR DE INGRESAR LOS NOMBRES EN MAYUSCULAS, GRACIAS.")

#ABRIR UN ARCHIVO CSV
with open("student_list.csv", "a") as file:
    #VERIFICAR SI ESTA VACIO, DE SER ASI AÑADIR LOS NOMBRES DE COLUMNAS
    file_is_empty = os.stat('student_list.csv').st_size == 0
    myFile = csv.writer(file)
    if file_is_empty:
            myFile.writerow(headers)
    
    #MIENTRAS LA BANDERA SIGA SIENDO TRUE
    while flag:
        #INGRESAR NOMBRES Y APELLIDOS
        name = str(input("Ingresa el nombre del estudiante: "))
        last_name = str(input("Ingresa los apellidos del estudiante: "))
        #GUARDARLOS EN UNA SOLA VARIABLE
        complete_name = name + " " + last_name
        student_names.append(complete_name)
        n += 1
        #SI YA SE INGRESARON LOS NOMBRES DE LOS DOS ALUMNOS POR SESION
        if n == 2:
            #LA BANDERA CAMBIA A FALSE, INDICANDO QUE SE VA A TERMINAR EL PROCESO DE REGISTRO
            flag = False
        #SELECTED ES EL ALUMNO QUE UTILIZARÁ ACTIVAMENTE EL VIDEOJUEGO Y EL CONTROL
        selected = random.choice(student_names)
        #ESCRIBIR EN EL CSV LOS NOMBRES DE CADA ALUMNO EN SU RESPECTIVA COLUMNA, INDICANDO SI FUERON DE UN GRUPO U OTRO
        if selected == complete_name:
            myFile.writerow([name, last_name, "y", "n"])
        else:
            myFile.writerow([name, last_name, "n", "y"])
#FINALMENTE, IMPRIMIR EN CONSOLA EL RESULTADO
print("El alumno que usará el software ludico será " + selected + ", mientras que el alumno restante será el de control")

# n = 2
# student_names = []
# fields = ['Nombre', 'Activo', 'De control']

# for i in range(0,n):
#     names = str(input("Ingresa el nombre completo del estudiante: "))
#     student_names.append(names)
# selected_student = random.choice(student_names)


