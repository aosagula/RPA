from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import config
import json
import db
import traceback
import smtp
import sys
import os
import requests


def setDocPuerto( operacion, fecha_a_plaza, user, fecha_alta):
    try:
        print('Iniciando Doc en puerto')
        imagename = dux.dux.setDocPuerto(operacion, fecha_a_plaza, user, fecha_alta)
        dux.dux.backMainMenu()
        print("esperando proxima tarea DUX")
        time.sleep(1)
        return imagename
    except:
        raise

def setFechaPlaza(numop, tipo_op, fecha_a_plaza):

    try:
        
        print("iniciando DUX")
        if( tipo_op == 'E'):
            imagename = dux.dux.setInExpo(numop, fecha_a_plaza)
        else:
            imagename = dux.dux.setInImpo(numop, fecha_a_plaza)
            
        dux.dux.backMainMenu()
        print("esperando proxima tarea DUX")
        time.sleep(1)
        return imagename
    except:
        raise

try:
    print('Buscando TAREAS Pendientes..')
    print("INICIANDO",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    tareas = db.db.getTareasPendientes('tareas')
    
    if(len(tareas)>0):
        current_task=0
        import dux
        
        dux.dux.Login()
        tos='itrva@vaclog.com,hbariain@vaclog.com,asagula@vaclog.com'
        for tarea in tareas:
            current_task = tarea[0]
            db.db.setEstadoTarea( current_task, 1)
            y = json.loads(tarea[1])

            # the result is a Python dictionary:
            print(y["numop"])
            fecha_temp = y["fecha_a_plaza"].split('-')
            fecha_a_plaza = fecha_temp[2]+"/"+fecha_temp[1]+"/"+fecha_temp[0]
            proceso = tarea[4]
            user = tarea[2]
            fecha_alta = tarea[3]
            if proceso == 'doc_puerto_proceso':
                imagename = setDocPuerto( y["numop"], fecha_a_plaza, user, fecha_alta)
                db.db.setEstadoTarea( current_task, 2)
                
                smtp.smtp.SendMail(tos.split(','), 'RPA_doc_en_puerto -> Operación {operacion} Confirmada fecha {fecha_a_plaza}'.format(operacion=y["numop"], fecha_a_plaza=fecha_a_plaza), "OK", "OK", imagename)
                if os.path.isfile(imagename):
                    os.remove(imagename)
            else:
                skip_process = False
                if 'continua_manana' in y:
                    
                    continua_manana = y["continua_manana"]
                    if "SI" in continua_manana:
                        skip_process = True
                
                if not skip_process:
                    imagename = setFechaPlaza( y["numop"], y["tipo_op"], fecha_a_plaza)
                    db.db.setEstadoTarea( current_task, 2)
                    #imagename=dux.dux.SaveImage(current_task)
                    
                    smtp.smtp.SendMail(tos.split(','), 'RPA_fecha_a_plaza -> Operación {operacion} Confirmada fecha {fecha_a_plaza}'.format(operacion=y["numop"], fecha_a_plaza=fecha_a_plaza), "OK", "OK", imagename)
                    if os.path.isfile(imagename):
                        os.remove(imagename)
                else:
                    db.db.setEstadoTarea( current_task, 2, 'Salteado')
        dux.dux.Close()
    print("FINALIZADO", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
except Exception as inst :
    error_description = traceback.format_exc()
    base_url = base_url  = 'https://api.telegram.org/bot6884941709:AAFedvLx2DxTRtuQJ59BIO3AoB00VJVDE6E/sendMessage?chat_id=-4008612871&text="{}"'.format(error_description)
    requests.get(base_url)
    db.db.setEstadoTarea(current_task, 3, error_description)
    print(error_description)
    imagename=dux.dux.SaveImage(current_task)
    dux.dux.Close()
    smtp.smtp.SendMail('tickets@itservices.vaclog.com', 'RPA_fecha_a_plaza -> Error en tarea {tarea}'.format(tarea=current_task), error_description, error_description, imagename)
    if os.path.isfile(imagename):
        os.remove(imagename)
    
    
    
    




