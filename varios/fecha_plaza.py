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
        #dux.dux.backMainMenu()
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

def procesa_parametros(proceso, parametros):

    y = json.loads(parametros)

    if proceso == 'doc_puerto_proceso' or proceso == 'fecha_plaza_proceso':        
        print(y["numop"])
        fecha_temp = y["fecha_a_plaza"].split('-')
        fecha_a_plaza = fecha_temp[2]+"/"+fecha_temp[1]+"/"+fecha_temp[0]
        numop = y["numop"]
        tipo_op = y["tipo_op"]
        continua_manana=""
        if 'continua_manana' in y:
                    
            continua_manana = y["continua_manana"]
        return fecha_a_plaza, numop, tipo_op, continua_manana
    if proceso == 'certificado_origen':
        nro_factura = y["nro_factura"]
        return nro_factura
    pass
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
            
            
            proceso = tarea[4]
            user = tarea[2]
            fecha_alta = tarea[3]
            if proceso == 'doc_puerto_proceso':
                db.db.setEstadoTarea( current_task, 1)
                fecha_a_plaza, numop, tipo_op, continua_manana = procesa_parametros(proceso, tarea[1])
                imagename = setDocPuerto( numop, fecha_a_plaza, user, fecha_alta)
                db.db.setEstadoTarea( current_task, 2)
                
                smtp.smtp.SendMail(tos.split(','), 'RPA_doc_en_puerto -> Operación {operacion} Confirmada fecha {fecha_a_plaza}'.format(operacion=numop, fecha_a_plaza=fecha_a_plaza), "OK", "OK", imagename)
                if os.path.isfile(imagename):
                    os.remove(imagename)
            elif proceso== 'fecha_plaza_proceso':
                db.db.setEstadoTarea( current_task, 1)
                fecha_a_plaza, numop, tipo_op, continua_manana = procesa_parametros(proceso, tarea[1])
                skip_process = False
                
                if "SI" in continua_manana:
                    skip_process = True
                
                if not skip_process:
                    imagename = setFechaPlaza( numop, tipo_op, fecha_a_plaza)
                    db.db.setEstadoTarea( current_task, 2)
                    #imagename=dux.dux.SaveImage(current_task)
                    
                    smtp.smtp.SendMail(tos.split(','), 'RPA_fecha_a_plaza -> Operación {operacion} Confirmada fecha {fecha_a_plaza}'.format(operacion=numop, fecha_a_plaza=fecha_a_plaza), "OK", "OK", imagename)
                    if os.path.isfile(imagename):
                        os.remove(imagename)
                else:
                    db.db.setEstadoTarea( current_task, 2, 'Salteado')
            elif proceso == 'certificado_origen':
                
                tos='asagula@vaclog.com'
                nro_factura = procesa_parametros(proceso, tarea[1])
                matriz_op_remitos = db.db.getOperacionesRemitos(nro_factura)
                db.db.setEstadoTarea( current_task, 1)
                
                if len(matriz_op_remitos) > 0:
                    fecha_factura = matriz_op_remitos[0]['fecha_factura']
                    archivo_factura = matriz_op_remitos[0]['archivo_factura']
                    importe_no_gravado = matriz_op_remitos[0]['total_factura']
                    imagename= dux.dux.ingresarFactura(nro_factura, fecha_factura.strftime("%d/%m/%Y"), matriz_op_remitos, archivo_factura, importe_no_gravado)
                    db.db.setEstadoTarea( current_task, 2)
                    smtp.smtp.SendMail(tos.split(','), f"RPA_factura_proveedores -> Factura {nro_factura} ", "OK", "OK", imagename)
                    db.db.setSubidoADux(nro_factura)
                    if os.path.isfile(imagename):
                         os.remove(imagename)
            elif proceso== 'instruccion_embarque':
                tos='Celula4@vaclog.com,asagula@vaclog.com'

                db.db.setEstadoTarea( current_task, 1)
                numop = tarea[5]
                values = db.db.getInstruccionEmbarque(numop)
                if values and 'numop' in values and numop == values['numop']: # a veces cargan a mano la instruccion en dux y no figura en la tabla de instruciones 
                    imagename = dux.dux.setInstruccionEmbarque(numop, values)
                    print("esperando proxima tarea DUX")
                    time.sleep(1)
                    smtp.smtp.SendMail(tos.split(','), 'RPA_instruccion_embarque -> Operación {operacion} '.format(operacion=numop), "OK", "OK", imagename)
                db.db.setEstadoTarea( current_task, 2)
                dux.dux.backMainMenu()
                
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
    
    
    
    




