from selenium.webdriver.common.by import By
from project.helper import parse_award_info
from project.pages.base_page import BasePage


class AwardsPage(BasePage):
    AWARD_BLOCK = By.XPATH, "//div[@class='ipc-metadata-list-summary-item__tc']"

    def get_awards(self):

        award_blocks = self.find_elements(self.AWARD_BLOCK)
        awards = []

        for block in award_blocks:
            try:
                nomination_text = block.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t").text
            except Exception:
                nomination_text = "N/A"
            try:
                award_category = block.find_element(By.CLASS_NAME, "awardCategoryName").text
            except Exception:
                award_category = "N/A"

            year, award_status, award_name = parse_award_info(nomination_text)

            award_data = {
                "award_name": award_name,
                "award_status": award_status,
                "year": year,
                "category": award_category
            }

            awards.append(award_data)

        return awards
