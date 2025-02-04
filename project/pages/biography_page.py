from selenium.webdriver.common.by import By
from project.pages.base_page import BasePage


class BiographyPage(BasePage):
    BIOGRAPHY = By.XPATH, "(//li[@id='mini_bio_0']//div[ @class='ipc-html-content-inner-div'])[1]"

    def get_biography(self):
        bio = self.find_element(self.BIOGRAPHY)
        return bio.text
