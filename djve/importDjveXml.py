
import time
import datetime
import sys
from pprint import pprint
import os
import traceback

sys.path.append(os.getcwd() + '\\varios')


import db
import smtp

# firefox_services = Service(executable_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe", port=2828, service_args=['--marionette-port', '2828', '--connect-existing'])
# driver = webdriver.Firefox(service=firefox_services).get('https://youtube.com')
# driver.get('https://youtube.com')



# driver = webdriver.Firefox( )

# driver.get('http://srv-duxweb02/dux/XZS001P001.aspx')


# print(driver.page_source)



class OperacionNoEncontrada(Exception):
    
    def __init__(self, mensaje):
        self.message = mensaje
        self.message_code = 100



    
print('Buscando Tareas Solicitud DJVE Pendientes..')
dt_inicio = datetime.datetime.now()
print("INICIANDO:", dt_inicio.strftime('%Y-%m-%d %H:%M:%S'))
tareas_pendientes = db.db.getTareasPendientesProc('solicitud_djve')
current_task=""
print('tareas =>', tareas_pendientes)

if len(tareas_pendientes) > 0:
    import dux 
    dux.dux.Login()
    for task in tareas_pendientes:
        try:
            numop=0
            current_task = task[0]
            db.db.setEstadoTarea( current_task, 1)
            archivo = "{nro_solicitud}.xml".format(nro_solicitud=task[2])
            print(archivo)
            dux.dux.OpenGestionDjve()
            dux.dux.newDjve(archivo)
            
            imagename=dux.dux.SaveImage(current_task)
            
            time.sleep(5)
            numop = db.db.getOperacion(task[2])
            print ("Operacion: ", numop)
            if numop > 0:
                dux.dux.AcceptSolDjve()
                
                time.sleep(2)              
                
                                
                dux.dux.generoTxtSIM(numop)
                imagename=dux.dux.SaveImage(current_task)
                time.sleep(1)
                archivo = dux.dux.getTxtFile(numop)

                if archivo:
                    print(f"Archivo encontrado {archivo}")
                    dux.dux.MoveTxtToSIMDirectory(archivo)
                else:
                    raise ("No se encontro el archivo {archivo}".format(archivo=archivo))
                smtp.smtp.SendMail('asagula@vaclog.com', 'RPA_Solicitud_DJVE -> Sol. Djve {nro_solicitud} -> Operación {numop} Confirmada'.format(nro_solicitud=task[2], numop=numop), "OK", "OK", imagename)
                db.db.setEstadoTarea( current_task, 2)
                if os.path.isfile(imagename):
                    os.remove(imagename)
                time.sleep(2)
            else:
                raise OperacionNoEncontrada("No se dio de alta la solicitud {nro_solicitud}".format(nro_solicitud=task[2]))
            
            dux.dux.backMainMenu()
        # except OperacionNoEncontrada:
        #     db.db.setEstadoTarea(current_task, 3, error_description)
        #     smtp.smtp.SendMail('asagula@vaclog.com', 'RPA_Solicitud_Djve -> Error solicitud nro: {nro_solicitud} y en tarea {tarea} '.format(tarea=current_task, nro_solicitud=task[2]), error_description, error_description, imagename)
        #     continue
        
        # except dux.dux.TimeoutException:
        #     db.db.setEstadoTarea(current_task, 3, error_description)
        #     smtp.smtp.SendMail('asagula@vaclog.com', 'RPA_Solicitud_Djve -> Error solicitud nro: {nro_solicitud} y en tarea {tarea} '.format(tarea=current_task, nro_solicitud=task[2]), error_description, error_description, imagename)
        #     continue
            
        except Exception as inst :
            error_description = traceback.format_exc()
            imagename=dux.dux.SaveImage(current_task)
            print("INST:" , inst)
            print("TAREA: ", task[3])
            if numop <= 0:
                
                if not ( str(inst) == task[3]):
                    db.db.setEstadoTarea(current_task, 3, error_description, str(inst))
                    print("distintos")
                    print(f"X{inst}X")
                    print(f"X{task[3]}X")
                    smtp.smtp.SendMail('asagula@vaclog.com', 'RPA_Solicitud_Djve -> Error solicitud nro: {nro_solicitud} y en tarea {tarea} '.format(tarea=current_task, nro_solicitud=task[2]), error_description, error_description, imagename)
            else:
                db.db.setEstadoTarea(current_task, 4, error_description, numop)
                smtp.smtp.SendMail('asagula@vaclog.com', 'RPA_Solicitud_Djve -> Error en operacion {numop} DEBE CORREGIR EN DUX'.format(numop=numop), 
                                   error_description, error_description, imagename)
            numop = 0
            
            
            if os.path.isfile(imagename):
                os.remove(imagename)
            dux.dux.backMainMenu()
            time.sleep(2)
            continue

    dux.dux.Close()
dt_fin = datetime.datetime.now()
print(f"FINALIZADO: {dt_fin.strftime('%Y-%m-%d %H:%M:%S')} tomo { (dt_fin - dt_inicio).total_seconds()} segundos", )

    
    
  