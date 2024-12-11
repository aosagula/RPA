import sys
import config
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
import traceback
import os
import time

import tempfile
class ImportXmlFail(Exception):
        def __init__(self, message):
            self.message = message
            self.message_code = 100
class Dux:
    
    

    def __init__ (self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        filename = "{tempdir}\{file}".format(tempdir=tempfile.gettempdir(), file='geckodriver.log')
        firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

        options = Options()
        options.binary_location = firefox_binary_path
        self.driver = webdriver.Firefox(options=options,service_log_path=filename  )
        self.driver.get(url)
        
        wait = WebDriverWait(self.driver, 10) 
        #EC.element_to_be_selected
        
        body = wait.until(EC.element_to_be_clickable(( By.CSS_SELECTOR, 'body')))
        action = ActionChains(self.driver).move_to_element_with_offset(body, (body.rect['width']/ 2) - 10, 0)
        action.click()
        action.perform()
        time.sleep(4)
    def Login (self):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('Autenticando ....')
        wait = WebDriverWait(self.driver, 10) 
        #EC.element_to_be_selected
        
        
        
        
        
        login_btn=    wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_cmdAceptar')))

        
        
        user = self.driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_txUsuario')
        user.clear()
        user.send_keys(config.config.dux_username)
        user.send_keys(Keys.TAB)

        password = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txPassword")

        
        password.clear()
        password.send_keys(config.config.dux_password)
        password.send_keys(Keys.ENTER)


        #login_btn = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_cmdAceptar')

        login_btn.click()

        print('Login')
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def SaveImage(self, current_task):
        filename = "{tempdir}\{current_task}.png".format(tempdir=tempfile.gettempdir(), current_task=current_task)
        self.driver.save_full_page_screenshot(filename)
        print(filename)
        return  filename
        
        
    def setInExpo(self, numop, fecha_a_plaza):

        wait = WebDriverWait(self.driver, 15)
        time.sleep(5)
        espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))
        

        wait = WebDriverWait(self.driver, 15)
        
        otros_datos = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[16]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
        
        otros_datos.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", otros_datos)

        espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")))

        buscar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")
        operacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txOperacionSeteable_AutoSuggestBox")
        operacion.clear()
        operacion.send_keys(numop)
        buscar_op.click()

        solapa_carga = self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label3"]')

        solapa_carga.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", solapa_carga)

        espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ayuFechaPreCumplido_Fecha")))
        fecha_pre_cumplido = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ayuFechaPreCumplido_Fecha")

        
        fecha_pre_cumplido_value = fecha_pre_cumplido.get_attribute('value')
        print('ya existe fecha_pre_cumplido: ', fecha_pre_cumplido_value)

        btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
        imagename = self.SaveImage(numop)
        if( len(fecha_pre_cumplido_value) == 0 ):
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnModificar")))
            modificar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnModificar")
            modificar_op.click()
            espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnCancelar")))
            fecha_pre_cumplido = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ayuFechaPreCumplido_Fecha")

            fecha_pre_cumplido.clear()
            fecha_pre_cumplido.send_keys(fecha_a_plaza)
            print(fecha_a_plaza)
            btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnGuardar")))
            btn_guardar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnGuardar')
            time.sleep(3)
            imagename = self.SaveImage(numop)
            #btn_cancelar.click()
            btn_guardar.click()
            
        return imagename
    
    def setDocPuerto(self, numop, fecha_a_plaza, user, fecha_alta):

            wait = WebDriverWait(self.driver, 15)
            time.sleep(5)
            espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))
            

            wait = WebDriverWait(self.driver, 15)
            
            otros_datos = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[16]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
            
            otros_datos.location_once_scrolled_into_view
            self.driver.execute_script("arguments[0].click();", otros_datos)

            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")))

            buscar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")
            operacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txOperacionSeteable_AutoSuggestBox")
            operacion.clear()
            operacion.send_keys(numop)
            buscar_op.click()

            solapa_carga = self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label13"]')

            solapa_carga.location_once_scrolled_into_view
            self.driver.execute_script("arguments[0].click();", solapa_carga)

            #espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ayuFechaPreCumplido_Fecha")))
            #fecha_pre_cumplido = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ayuFechaPreCumplido_Fecha")

            
            #fecha_pre_cumplido_value = fecha_pre_cumplido.get_attribute('value')
            #print('ya existe fecha_pre_cumplido: ', fecha_pre_cumplido_value)

            btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
            
            
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnModificar")))
            modificar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnModificar")
            modificar_op.click()
            
            
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_CmdAlta")))
            agregar_comentario_boton = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_CmdAlta")
            agregar_comentario_boton.click()
            
            comentario = f"{fecha_a_plaza} CARPETA EN PUERTO ingresada por: {user} registrado a las: {fecha_alta}"
            
            txt_object = "ctl00_ContentPlaceHolder1_TextComentario_TextBox1"
            
            comentario_texto = self.driver.find_element(By.ID, txt_object)
            comentario_texto.clear()
            comentario_texto.send_keys(comentario)
            
            comentario_guardar = "ctl00_ContentPlaceHolder1_CmdGuardar_A"
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, comentario_guardar)))
            comentario_guardar_boton = self.driver.find_element(By.ID, comentario_guardar)
            comentario_guardar_boton.click()
            
            
            espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnCancelar")))
            
            print(comentario)
            btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnGuardar")))
            btn_guardar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnGuardar')
            time.sleep(3)
            imagename = self.SaveImage(numop)
            #btn_cancelar.click()
            btn_guardar.click()
            return imagename

    def backMainMenu(self):
        wait = WebDriverWait(self.driver, 15)
        back="/html/body/form/div[4]/table[1]/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/a"
       
        back_btn = wait.until (EC.presence_of_all_elements_located( (By.XPATH, back)))
        
        link = self.driver.find_element(By.XPATH, back)
        
        link.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", link)

        
        
    def setInImpo(self, numop, fecha_a_plaza):

        wait = WebDriverWait(self.driver, 15)
        time.sleep(5)
        espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))
        

        wait = WebDriverWait(self.driver, 15)
        
        otros_datos = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[6]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
        
        otros_datos.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", otros_datos)

        espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")))

        buscar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")
        operacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txOperacionSeteable_AutoSuggestBox")
        operacion.clear()
        operacion.send_keys(numop)
        buscar_op.click()

        solapa_carga = self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label24"]')

        solapa_carga.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", solapa_carga)

        espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_cfeFechaPlaza_Fecha")))
        fecha_cumplido = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cfeFechaPlaza_Fecha")

        
        fecha_aplaza_value = fecha_cumplido.get_attribute('value')
        print('fecha_a_plaza: ', fecha_aplaza_value)

        #btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
        imagename = self.SaveImage(numop)
        if( len(fecha_aplaza_value) == 0 ):
            time.sleep(3)
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnModificar")))
            modificar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnModificar")
            modificar_op.click()
            time.sleep(3)
            espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnCancelar")))
            fecha_aplaza = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cfeFechaPlaza_Fecha")
            print(fecha_aplaza.get_attribute("InnerHTML"))
            fecha_aplaza.clear()
            fecha_aplaza.send_keys(fecha_a_plaza)
            print(fecha_a_plaza)
            btn_cancelar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnCancelar')
            espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnGuardar")))
            btn_guardar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnGuardar')
            time.sleep(3)
            #btn_cancelar.click()
            imagename = self.SaveImage(numop)
            btn_guardar.click()
        return imagename
            
    def testbtn(self, numop):
        wait = WebDriverWait(self.driver, 15)
        time.sleep(5)
        espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))
        

        # gestion_djve = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[15]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
        # print(gestion_djve.get_attribute('href'))
        # gestion_djve.location_once_scrolled_into_view
        # self.driver.execute_script("arguments[0].click();", gestion_djve)


        wait = WebDriverWait(self.driver, 15)
        
        otros_datos = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[16]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
        # otros_datos.click()
        #gestion_djve = driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[15]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
    #print(gestion_djve.get_attribute('href'))
        otros_datos.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", otros_datos)

        espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")))

        buscar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")
        operacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txOperacionSeteable_AutoSuggestBox")
        
        operacion.send_keys(numop)
        buscar_op.click()

        solapa_carga = self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label3"]')

        solapa_carga.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", solapa_carga)

        espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnModificar")))

        btn_modificar = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnModificar')

        btn_modificar.click()


        espero_carga = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnGuardar")))


        btn_save = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnGuardar')

        btn_save.click()


        espero_carga = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/span[2]")))

        element = self.driver.find_element(By.XPATH , '/html/body/div[1]/div[2]/span[2]')

        print(element.get_attribute('InnerHTML'))


    def Close (self):
        self.driver.close()

    def OpenGestionDjve(self):
        wait = WebDriverWait(self.driver, 10)
        driver = self.driver
        time.sleep(2)
        espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))
        

        gestion_djve = driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[15]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
        print(gestion_djve.get_attribute('href'))
        gestion_djve.location_once_scrolled_into_view
        driver.execute_script("arguments[0].click();", gestion_djve)

        print('Ingreando a gestion DJVE')
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        
    def newDjve(self, archivo):
        wait = WebDriverWait(self.driver, 10)
        driver = self.driver
        new_djve = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_btnNuevo')))
        new_djve.click()
        
        time.sleep(2)
        self.importXml(archivo)
        
    def importXml(self, archivo):
        wait = WebDriverWait(self.driver, 10)
        upload_btn = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_cmdFileUpDoc')))

        select_file = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_FileUpDoc')))
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        xmlfile = config.config.djve_xml_path + '\\' + archivo 
        
        select_file.send_keys(xmlfile)
        #select_file.send_keys("J:\\SOLICITUD DJVE\\test.xml")
        if os.path.isfile(xmlfile):
            print('Procesando XML: ' + xmlfile)
            upload_btn.click()
            resultado = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.duxmsgboxbody')))
            print ("Resultado:", resultado)
            
            print(resultado.get_attribute('innerHTML'))  
            if "*" in resultado.get_attribute("innerHTML"):
                raise ImportXmlFail(resultado.get_attribute("innerHTML"))
            
        
        time.sleep(2)
        
    def AcceptSolDjve(self):
        wait = WebDriverWait(self.driver, 10)
                                             
        accept_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui-button-text-only')))
        accept_btn.click()
        
    def generoTxtSIM(self, numop):
        wait = WebDriverWait(self.driver, 10)
        driver = self.driver
        espero_carga = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")))

        buscar_op = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnBuscar")
        
        
        operacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txOperacionSeteable_AutoSuggestBox")
        operacion.clear()
        operacion.send_keys(numop)
        buscar_op.click()
        
       
        time.sleep(2)
        print("PANTALLA INICIAL", driver.current_window_handle)
        paso_siguiente = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_btnPasoSiguiente")))

        paso_siguiente = self.driver.find_element(By.ID, "ctl00_btnPasoSiguiente")
        
        paso_siguiente.click()
        
        
        
        time.sleep(2)
        print("PRORRATEO", driver.current_window_handle)
        prorrateo = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_aceptar")))

        prorrateo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_aceptar")
        
        prorrateo.click()
        self.AcceptProrrateo()
        paso_siguiente = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_btnPasoSiguiente")))

        paso_siguiente = self.driver.find_element(By.ID, "ctl00_btnPasoSiguiente")
        
        paso_siguiente.click()
        
    
        time.sleep(2)
        
        print("VALORIZACION", driver.current_window_handle)
        valorizacion = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Aceptar")))
        self.driver.save_full_page_screenshot('valorizacio.png')
        print("aceptar valorizacion", valorizacion)
        #valorizacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_aceptar")
        
        valorizacion.click()
        
        #"ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close"
        
        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui-dialog-titlebar-close')))
        #close_btn = self.driver.find_element(By.CSS_SELECTOR, '.ui-dialog-titlebar-close')
        close_btn.click()
        time.sleep(2)
        paso_siguiente = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_btnPasoSiguiente")))

        paso_siguiente = self.driver.find_element(By.ID, "ctl00_btnPasoSiguiente")
        
        paso_siguiente.click()
        
        print("INTERFAZ SIM", driver.current_window_handle)
        interfaz_sim_btn = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Aceptar")))
        self.driver.save_full_page_screenshot('Interfaz_SIM.png')
        print("aceptar valorizacion", interfaz_sim_btn)
        #valorizacion = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_aceptar")
        
        interfaz_sim_btn.click()
        time.sleep(1)
        download_btn = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Aceptar")))
        self.driver.save_full_page_screenshot('Interfaz_SIM.png')
        print("aceptar valorizacion", download_btn)
        download_btn.click()
        
        #"ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close"
        
        
        time.sleep(2)
        
        
        
    def AcceptProrrateo(self):
        wait = WebDriverWait(self.driver, 10)
                                             
        accept_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui-button-text-only')))
        accept_btn.click()
        
    def getTxtFile(self, numop):
        import os
        import datetime

        # Set the directory path and filename pattern
        directory = config.config.download_path
        filename_pattern = '00{numop}*.txt'.format(numop=numop)
        filename_pattern = '00{numop}'.format(numop=numop)

        # Get all files in the directory that match the filename pattern
        files = [file for file in os.listdir(directory) if file.endswith('.txt') and file.startswith(filename_pattern)]

        # Get the most recent file by comparing the modified time of each file
        latest_file = None
        latest_mod_time = datetime.datetime.min
        for file in files:
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, file)))
            if mod_time > latest_mod_time:
                latest_file = file
                latest_mod_time = mod_time

        # Print the name of the latest file
        #print(latest_file)
        return latest_file
    
    def MoveTxtToSIMDirectory(seft, filename):
        import shutil

        # Set the source and destination directories
        source_dir = config.config.download_path
        destination_dir = config.config.dux_txt_to_sim

        

        # Move the file to the destination directory
        shutil.move(f"{source_dir}/{filename}", f"{destination_dir}/{filename}")

dux = Dux( config.config.dux_url, config.config.dux_username, config.config.dux_password )