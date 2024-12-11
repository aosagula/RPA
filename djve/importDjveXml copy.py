from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import config

import db



driver = webdriver.Firefox()


driver.get('http://srv-duxweb02/dux/XZS001P001.aspx')


def Login ():

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('Autenticando ....')
    wait = WebDriverWait(driver, 10) 
    login_btn=    wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_cmdAceptar')))

    user = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_txUsuario')
    user.clear()
    user.send_keys(config.config.dux_username)
    user.send_keys(Keys.TAB)

    password = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txPassword")
    password.clear()
    password.send_keys(config.config.dux_password)
    password.send_keys(Keys.ENTER)

    #login_btn = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_cmdAceptar')

    login_btn.click()

    print('Login')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def OpenGestionDjve():
    wait = WebDriverWait(driver, 10)
    espera_carga = wait.until (EC.presence_of_all_elements_located( (By.CLASS_NAME, 'ctl00_Menu1_MenuLeft_Menu1_6')))


    gestion_djve = driver.find_element(By.XPATH, '/html/body/form/div[5]/nav/div[4]/div/div/div[1]/div[15]/table/tbody/tr[1]/td/table/tbody/tr/td/a')
    print(gestion_djve.get_attribute('href'))
    gestion_djve.location_once_scrolled_into_view
    driver.execute_script("arguments[0].click();", gestion_djve)

    print('Ingreando a gestion DJVE')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    new_djve = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_btnNuevo')))

    new_djve.click()



Login()

OpenGestionDjve()


print('Buscando DJVE Pendientes..')
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
djves = db.db.searchDjvesPendientes()

print('DJVES =>', djves)
wait = WebDriverWait(driver, 10)
for djve in djves:

    upload_btn = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_cmdFileUpDoc')))

    select_file = wait.until (EC.element_to_be_clickable( (By.ID, 'ctl00_ContentPlaceHolder1_FileUpDoc')))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('Procesando XML: ' + config.config.djve_xml_path + '\\' + djve )
    select_file.send_keys(config.config.djve_xml_path + '\\' + djve)



