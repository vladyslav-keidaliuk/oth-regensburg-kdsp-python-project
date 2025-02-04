import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from project.pages.base_page import BasePage


class ActorsListPage(BasePage):
    TITLE = (By.XPATH, "//a/h3[@class='ipc-title__text']")

    def title_with_index(self, index):
        return By.XPATH, f"//a/h3[@class='ipc-title__text'][{index}]"

    def title_with_text(self, text):
        return By.XPATH, f"//a/h3[@class='ipc-title__text' and contains(text(), '{text}')]"

    def cookies_accept_btn(self):
        return By.XPATH, "//button[text()='Accept']"

    def get_actors(self):
        """Returns a list of actors with their names and URLs."""
        actor_elements = self.find_elements(self.TITLE)
        return [{"name": re.sub(r'^\d+\.\s', '', actor.text)} for actor in actor_elements]

    def click_by_title(self, text):
        self.find_element(self.title_with_text(text)).click()

    def click_by_index(self, index):
        self.find_element(self.title_with_index(index)).click()

    def click_accept_cookies(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cookies_accept_btn())
        ).click()
