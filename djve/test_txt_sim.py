
import time
import datetime
import sys
from pprint import pprint
import os
import traceback

sys.path.append(os.getcwd() + '\\varios')


import db
import smtp





import dux 
dux.dux.Login()

while True:
    dux.dux.OpenGestionDjve()
    time.sleep(2)
    dux.dux.backMainMenu()
    time.sleep(2)
    
#dux.dux.generoTxtSIM(200476)
#try:
#     archivo = dux.dux.getTxtFile(200476)

#     if archivo:
#         print(archivo)
#         dux.dux.MoveTxtToSIMDirectory(archivo)
#     else:
#         raise ("Pucha")
# except Exception as inst :
#     error_description = traceback.format_exc()
    
#     print(error_description)
