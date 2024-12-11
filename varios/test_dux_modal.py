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
import dux

dux.dux.Login()
dux.dux.testbtn(193652)