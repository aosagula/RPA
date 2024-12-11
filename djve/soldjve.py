
import datetime
import sys
from pprint import pprint
import os


sys.path.append(os.getcwd() + '\\varios')

pprint(sys.path)
import db as DB


print('Buscando DJVE Pendientes..')
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
djves = DB.db.searchDjvesPendientes()
pprint(djves)
tareas_pendientes = DB.db.getTareasPendientesProc('solicitud_djve')
pprint(tareas_pendientes)

print("-------------------------------")
InsertTaskList = []
for djve in djves:
    existe = False
    for tarea in tareas_pendientes:
        #print(djve[0], tarea[2])
        if( str(djve[0]) == tarea[2]):
            print("existe", djve[0], tarea[2])
            existe = True
            break
    if existe == False:
        #print("{'solicitud_djve': {djve}}".format(djve=djve[0]))
        InsertTaskList.append ( ["", djve[0]])
pprint(InsertTaskList)

for item in InsertTaskList:
    pprint(item)
    DB.db.insertTarea('solicitud_djve', item[1], item[0])

