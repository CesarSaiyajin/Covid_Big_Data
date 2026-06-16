import time
import pandas as pd
import csv
import os
from datetime import datetime 

# SE SOLICITA EL NOMBRE DEL ARCHIVO A REVISAR 
#nombreArch = input("Nombre de archivo CSV: ")
nombreArch = "220720COVID19MEXICO"
print("GUARDANDO DATOS LIMPIOS")

ini = time.time_ns()
#df = pd.read_csv(nombreArch+".csv")
# LECTURA DE LOS METADATOS
contador = 1
erroneos = 0
variables = []
borrar = [16734297, 16736952, 16743964, 16747188, 16753065,
          16756285, 16759504, 16759957, 16762725, 16762775,
          16765945]

salida = open("2limpiados.txt", "w")
#archLimpio = open("2limpios.csv", "w", newline='', encoding="latin1")
aLimpios = open("primerlimpieza.csv", "w", encoding="UTF-8")
with open(nombreArch+".csv", encoding="UTF-8", newline='') as File:  
    archivo = csv.reader(File)
#    limpios = csv.writer(archLimpio)
    for registro in archivo:
        if contador == 1:
            ct = 0
            for metadato in registro:
                variables.append(metadato)
                if ct == 0:
                    aLimpios.write(metadato)    
                else:
                    aLimpios.write(","+metadato)
                ct += 1
            aLimpios.write("\n")
            contador += 1
            continue

        if contador in borrar:
            erroneos += 1
            print(str(erroneos)+" "+str(contador)+" ELIMINADO por irrecuperabilidad")
            salida.write(str(erroneos)+" "+str(contador)+" ELIMINADO por irrecuperabilidad "+str(len(registro))+" "+str(registro)+"\n\n")
            contador += 1
            continue
                
        if contador == 16734185 or contador == 16749845:
             erroneos += 1
             salida.write(str(erroneos)+" "+str(contador)+" CORREGIR antes "+str(len(registro))+" "+str(registro)+"\n")
             buena = registro[:37] 
             buena.append('México')
             buena.append('97')
             buena.append('97')
             registro = buena
             print(str(erroneos)+" "+str(contador)+" CORREGIDO "+str(registro))
             salida.write(str(contador)+" después "+str(len(registro))+" "+str(registro)+"\n\n")             

        if contador == 16740173:
             erroneos += 1
             salida.write(str(erroneos)+" "+str(contador)+" CORREGIDO antes "+str(len(registro))+" "+str(registro)+"\n")
             buena = registro[10:] 
             registro = buena
             print(str(erroneos)+" "+str(contador)+" CORREGIDO "+str(registro))
             salida.write(str(contador)+" después "+str(len(registro))+" "+str(registro)+"\n\n")

        if contador == 16759956:
             erroneos += 1
             salida.write(str(erroneos)+" "+str(contador)+" CORREGIDO antes "+str(len(registro))+" "+str(registro)+"\n")
             buena = ['2022-07-20']
             buena = buena + registro[27:]
             registro = buena
             print(str(erroneos)+" "+str(contador)+" CORREGIDO "+str(registro))
             salida.write(str(contador)+" después "+str(len(registro))+" "+str(registro)+"\n\n")
                        
        if len(registro) != 40:
            erroneos += 1            
            salida.write(str(erroneos)+" "+str(contador)+" "+str(len(registro))+" ")
            if len(registro) < 40:
                print(str(erroneos)+" "+str(contador)+" faltan datos "+str(len(registro)))
                salida.write("faltan datos ")
            else:                
                print(str(erroneos)+" "+str(contador)+" sobran datos "+str(len(registro)))
                salida.write("sobran datos ")
            salida.write(str(registro)+'\n')
            
            for i in range(len(registro)):
                if i < 40:
                    salida.write(str(i+1)+" "+variables[i])
                else:
                    salida.write('SIN NOMBRE')
                salida.write(": "+str(registro[i])+"\n")
            salida.write('\n')
        else:
            #print('['+str(registro)+']')
            aLimpios.write("'"+registro[0] +"','"+registro[1] +"',"+registro[2] +","+registro[3] +","+registro[4]+
                             ","+registro[5] +","+registro[6] +","+registro[7] +","+registro[8] +","+registro[9]+
                             ",'"+registro[10]+"','"+registro[11]+"','"+registro[12]+"',"+registro[13]+","+registro[14]+
                             ","+registro[15]+","+registro[16]+","+registro[17]+","+registro[18]+","+registro[19]+
                             ","+registro[20]+","+registro[21]+","+registro[22]+","+registro[23]+","+registro[24]+
                             ","+registro[25]+","+registro[26]+","+registro[27]+","+registro[28]+","+registro[29]+
                             ","+registro[30]+","+registro[31]+","+registro[32]+","+registro[33]+","+registro[34]+
                             ","+registro[35]+","+registro[36]+",'"+registro[37]+"','"+registro[38]+"',"+registro[39]+"\n");

        contador += 1
#        if contador == 10:
#            break
        if contador % 1000000 == 0: 
            fin = time.time_ns()
            print(str((fin-ini)/1e9) ,contador)
fin = time.time_ns()
duracion = (fin-ini)/1e9

print()
print("Duración de la limpieza y guardado: ", duracion, " segundos")
print("Se limpiaron "+str(erroneos)+" registros") 
print("Se guardaron "+str(contador)+" registros") 
salida.close()
#archLimpio.close()
aLimpios.close()

# Guardar el tiempo de ejecución en archivo
if not os.path.exists("Tiempos"):
    os.makedirs("Tiempos")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_tiempo = os.path.join("Tiempos", f"tiempo_ejecucion_{timestamp}.txt")

with open(archivo_tiempo, "w") as f:
    f.write(f"Tiempo de ejecución del limpiador1.py\n")
    f.write(f"=====================================\n")
    f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Duración: {duracion:.2f} segundos\n")
    f.write(f"Registros limpios: {erroneos}\n")
    f.write(f"Registros guardados: {contador}\n")

print(f"Tiempo de ejecución guardado en: {archivo_tiempo}")