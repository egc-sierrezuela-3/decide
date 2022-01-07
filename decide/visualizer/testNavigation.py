from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from http import HTTPStatus
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question, QuestionOption
from base import mods
from mixnet.models import Auth
from django.conf import settings
from selenium.webdriver.common.action_chains import ActionChains

class VisualizerTestSelenium(LiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        return v

    def test_visualizer_voting_in_progress_sin_comenzar(self):
         voting = self.create_voting()
         self.driver.get(f'{self.live_server_url}/visualizer/'+str(voting.pk))

         self.assertEquals(
             self.driver.find_element_by_tag_name('h5').text,
             'Estado: Votación no comenzada.'
        )        

    def test_visualizer_voting_in_progress_comenzada(self):

        voting = self.create_voting()
        self.driver.get(f'{self.live_server_url}/admin')
        self.driver.find_element_by_name('username').send_keys("adminprueba")
        self.driver.find_element_by_name('password').send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR,".submit-row > input").click()
        self.driver.implicitly_wait(10)
        self.driver.get(f'{self.live_server_url}/admin/voting/voting')
        self.driver.implicitly_wait(10)

        self.driver.find_element(By.XPATH, "(//input[@name=\'_selected_action\'])[1]").click()

        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
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
        
        self.driver.get(f'{self.live_server_url}/visualizer/'+str(voting.pk))
        self.driver.implicitly_wait(10)
        self.assertEquals(
            self.driver.find_element_by_tag_name('h5').text,
            'Estado: Votación en progreso.'
        )


    def test_visualizer_voting_in_progress_finalizada(self):
        voting = self.create_voting()
        self.driver.get(f'{self.live_server_url}/admin')
        self.driver.find_element_by_name('username').send_keys("adminprueba")
        self.driver.find_element_by_name('password').send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR,".submit-row > input").click()
        self.driver.implicitly_wait(10)
        self.driver.get(f'{self.live_server_url}/admin/voting/voting')
        self.driver.implicitly_wait(10)

        self.driver.find_element(By.XPATH, "(//input[@name=\'_selected_action\'])[1]").click()

        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
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
        self.driver.find_element(By.NAME, "_selected_action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Stop']").click()
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
        
        self.driver.get(f'{self.live_server_url}/visualizer/'+str(voting.pk))
        self.driver.implicitly_wait(10)
        self.assertEquals(
             self.driver.find_element_by_tag_name('h5').text,
             'Estado: Cerrada'
        )



