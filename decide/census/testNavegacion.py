import random
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework.test import APIClient
from census import admin
from authentication.models import Persona
from .models import Census
from base import mods
from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ImportCensus(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        # options.add_argument("--allow-file-access-from-files")
        # self.driver.desired_capabilities=options.to_capabilities()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        self.census=Census(voting_id=1,voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()


    #ESTE TEST DEBE CORRER EN EL SELENIUM IDE, el cual debe tener activada la opción "Allow access to file URLs"
    #SE HA DE ESPECIFICAR LA URL LOCAL DE UN CENSO CORRECTO, EL CUAL SE ENCUENTRA EN "./testFiles/censo.csv"

    # def test_import_census_positive(self):
    #     #1 | open | /admin/ | 
    #     self.driver.get(f'{self.live_server_url}/admin/')
    #     self.driver.find_element_by_id('id_username').send_keys("adminprueba")
    #     self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
    #     # 2 | setWindowSize | 821x694 | 
    #     self.driver.set_window_size(821, 694)
    #     # 3 | click | linkText=Censuss | 
    #     self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    #     # 4 | click | id=action-toggle | 
    #     self.driver.find_element(By.ID, "action-toggle").click()
    #      # 5 | select | name=action | label=Import census
    #     dropdown = self.driver.find_element(By.NAME, "action")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Import census']").click()

    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).click_and_hold().perform()
    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).perform()
    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).release().perform()
    #     self.driver.find_element(By.NAME, "index").click()

    #     #Seleccionar el censo y abrirlo
    #     self.driver.find_element(By.NAME, "nuevoCenso").click()
    #     self.driver.find_element(By.NAME, "nuevoCenso").send_keys("./testFiles/\censo.csv")
    #     self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()

    #    #Si la importación se ha realizado, debe aparecer un mensaje
    #     mensaje = self.driver.find_element_by_id("importTest").text

    #     self.assertEquals(mensaje, 'Los datos se han cargado correctamente')

        
    def test_import_census_negative(self):
        #1 | open | /admin/ | 
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("adminprueba")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)

        
        # 2 | setWindowSize | 821x694 | 
        self.driver.set_window_size(821, 694)

        # 3 | click | linkText=Censuss | 
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()

        # 4 | click | id=action-toggle | 
        self.driver.find_element(By.ID, "action-toggle").click()
         # 5 | select | name=action | label=Export census

        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Import census']").click()

        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.NAME, "index").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()

       #Si la importación no se ha realizado, debe aparecer un mensaje
        mensaje = self.driver.find_element_by_id("vacioTest").text

        self.assertEquals(mensaje, 'Selecciona un archivo csv con el formato indicado')


#ESTE TEST DEBE CORRER EN EL SELENIUM IDE, el cual debe tener activada la opción "Allow access to file URLs"
#SE HA DE ESPECIFICAR LA URL LOCAL DE UN CENSO INCORRECTO, EL CUAL SE ENCUENTRA EN "./testFiles/censoIncorrecto.csv"

    # def test_import_census_negative2(self):
    #     #1 | open | /admin/ | 
    #     self.driver.get(f'{self.live_server_url}/admin/')
    #     self.driver.find_element_by_id('id_username').send_keys("adminprueba")
    #     self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
    #     # 2 | setWindowSize | 821x694 | 
    #     self.driver.set_window_size(821, 694)
    #     # 3 | click | linkText=Censuss | 
    #     self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    #     # 4 | click | id=action-toggle | 
    #     self.driver.find_element(By.ID, "action-toggle").click()
    #      # 5 | select | name=action | label=Import census
    #     dropdown = self.driver.find_element(By.NAME, "action")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Import census']").click()

    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).click_and_hold().perform()
    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).perform()
    #     element = self.driver.find_element(By.NAME, "action")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(element).release().perform()
    #     self.driver.find_element(By.NAME, "index").click()

    #     #Seleccionar el censoIncorrecto y abrirlo
    #     self.driver.find_element(By.NAME, "nuevoCenso").click()
    #     self.driver.find_element(By.NAME, "nuevoCenso").send_keys("./testFiles/\censoIncorrecto.csv")
    #     self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()

    #    #Si la importación no se ha realizado, debe aparecer un mensaje
    #     mensaje = self.driver.find_element_by_id("vacioTest").text

    #     self.assertEquals(mensaje, 'Selecciona un archivo csv con el formato indicado')

class ExportCensus(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        self.census=Census(voting_id=1,voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_export_census_positive(self):
        #Test name: exportar_censo
        #Step # | name | target | value
        #1 | open | /admin/ | 
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("adminprueba")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)

        
        # 2 | setWindowSize | 821x694 | 
        self.driver.set_window_size(821, 694)

        # 3 | click | linkText=Censuss | 
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()

        # 4 | click | id=action-toggle | 
        self.driver.find_element(By.ID, "action-toggle").click()

        # 5 | select | name=action | label=Export census
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Export census']").click()

        
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()

        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()

        # 6 | click | name=index | 
        self.driver.find_element(By.NAME, "index").click()

        #Refrescamos la página
        self.driver.refresh()

        #Si la exportación se ha realizado, debe aparecer un mensaje
        mensaje = self.driver.find_element(By.CLASS_NAME, "success").text

        self.assertEquals(mensaje, 'Exportación realizada con éxito')

    def test_export_census_negative(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("adminprueba")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)

        
        # 2 | setWindowSize | 821x694 | 
        self.driver.set_window_size(821, 694)

        # 3 | click | linkText=Censuss | 
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()

        # 4 | click | id=action-toggle | 
        #self.driver.find_element(By.ID, "action-toggle").click()

        # 5 | select | name=action | label=Export census
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Export census']").click()

        
        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()

        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        element = self.driver.find_element(By.NAME, "action")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()

        # 6 | click | name=index | 
        self.driver.find_element(By.NAME, "index").click()

        #Si la exportación se ha realizado, debe aparecer un mensaje
        mensaje = self.driver.find_element(By.CLASS_NAME, "warning").text

        self.assertEquals(mensaje, 'Items must be selected in order to perform actions on them. No items have been changed.')

