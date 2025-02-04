from selenium.webdriver.common.by import By
from project.pages.base_page import BasePage


def actor_img(text):
    return By.XPATH, f"(//img[starts-with(@alt,'{text}')])[1]"


class ActorPage(BasePage):
    PHOTO = (By.XPATH,
             "//img[contains(@class, 'poster') or contains(@alt, 'Primary')]")
    ABOUT = (By.XPATH,
             "//div[@id='name-bio-text']//div[@class='inline']")
    MOVIES = (By.XPATH,
              "//div[contains(@class,'filmo-row')]")
    BIO_LINK_ELEMENT = (By.XPATH,
                        "//div[starts-with(@class,'ipc-html-content ipc-html-content--baseAlt')]")
    DATE_OF_BIRTH = (By.XPATH,
                     "(//div[@data-testid='birth-and-death-birthdate']/span)[4]")
    COUNT_OF_ACTOR_MOVIES = (By.XPATH,
                             "//*[@id='actor-previous-projects']/div[1]/label/span[1]/ul/li[2]")
    COUNT_OF_ACTRESS_MOVIES = (By.XPATH,
                               "//*[@id='actress-previous-projects']/div[1]/label/span[1]/ul/li[2]")
    ROLE_ACTOR_BLOCK = (By.XPATH,
                        "//h3[@class='ipc-title__text' and contains(text(),'Actor')]")
    PREVIOUS_PROJECTS_ACTOR = (By.XPATH,
                               "//label[@data-testid='accordion-item-actor-previous-projects']")
    PREVIOUS_PROJECTS_ACTRESS = (By.XPATH,
                                 "//label[@data-testid='accordion-item-actress-previous-projects']")
    ROLE_ACTRESS_BLOCK = (By.XPATH,
                          "//h3[@class='ipc-title__text' and contains(text(),'Actress')]")
    SEE_ALL_BTN_ACTOR = (By.XPATH,
                         "//button[@data-testid='nm-flmg-paginated-all-actor']")
    SEE_ALL_BTN_ACTRESS = (By.XPATH,
                           "//button[@data-testid='nm-flmg-paginated-all-actress']")
    MOVIE_TITLE = (By.XPATH,
                   "//h3[@class='ipc-title__text prompt-title-text']")
    CLOSE_MOVIE_BLOCK_BTN = (By.XPATH,
                             "//button[@title='Close Prompt']")
    RELEASE_YEAR = (By.XPATH,
                    "//ul[@data-testid='btp_ml']/li[1]")
    LIST_OF_GENRES = (By.XPATH,
                      "//ul[@data-testid='btp_gl']/li")
    RATING_OF_MOVIE = (By.XPATH,
                       "//div[@data-testid='btp_rt']//span[@class='ipc-rating-star--rating']")
    AWARDS_LINK_ELEMENT = (By.XPATH,
                           "//a[text()='Awards' and starts-with(@class,'ipc-link')]")

    def actor_movie_image_by_index(self, index):
        return (By.XPATH,
                f"(//div[@id='accordion-item-actor-previous-projects']//img[@class='ipc-image'])[{index}]")

    def actress_movie_image_by_index(self, index):
        return (By.XPATH,
                f"(//div[@id='accordion-item-actress-previous-projects']//img[@class='ipc-image'])[{index}]")

    def get_movie_image_by_index(self, index):
        try:
            if self.is_element_present(self.ROLE_ACTOR_BLOCK):
                element = self.find_element(self.actor_movie_image_by_index(index))
            else:
                element = self.find_element(self.actress_movie_image_by_index(index))
            return element.get_attribute('src')
        except:
            return "No image"

    def actor_movie_block_by_index(self, index):
        return (By.XPATH,
                (f"//div[@id='accordion-item-actor-previous-projects']/div/ul/li[{index}]//button["
                 f"@aria-label='More']"))

    def actress_movie_block_by_index(self, index):
        return (By.XPATH,
                (f"//div[@id='accordion-item-actress-previous-projects']/div/ul/li[{index}]//button["
                 f"@aria-label='More']"))

    def bio_btn(self):
        return (By.XPATH,
                "//button[text()='Accept']")

    def get_photo_url(self):
        return self.find_element(*self.PHOTO).get_attribute("src")

    def get_actor_name(self):
        return self.find_element((By.XPATH,
                                  "//span[@class='hero__primary-text']")).text

    def get_about(self):
        return self.find_element(*self.ABOUT).text.strip()

    def get_movies(self):
        movie_elements = self.find_elements(*self.MOVIES)
        movies = []
        for movie in movie_elements:
            title = movie.find_element(By.TAG_NAME, "b").text.strip()
            year = movie.find_element(By.XPATH,
                                      ".//span[contains(@class, 'year_column')]").text.strip()
            movies.append({"title": title, "year": year})
        return movies

    def open_bio_page(self):
        self.click_on(self.BIO_LINK_ELEMENT)

    def get_date_of_birth(self):
        return self.find_element(self.DATE_OF_BIRTH).text

    def get_count_of_movies(self):
        try:
            return int(self.find_element(self.COUNT_OF_ACTOR_MOVIES).text)
        except:
            return int(self.find_element(self.COUNT_OF_ACTRESS_MOVIES).text)

    def expand_list_of_movies(self):
        try:
            if self.is_element_present(self.ROLE_ACTOR_BLOCK):
                try:
                    self.find_element(self.SEE_ALL_BTN_ACTOR).click()
                except:
                    self.find_element(self.PREVIOUS_PROJECTS_ACTOR).click()
            else:
                self.find_element(self.PREVIOUS_PROJECTS_ACTOR).click()
        except:
            try:
                self.find_element(self.SEE_ALL_BTN_ACTRESS).click()
            except:
                try:
                    self.find_element(self.PREVIOUS_PROJECTS_ACTRESS).click()
                except:
                    print("No btn 'SEE ALL'")

    def click_on_movie_by_index(self, index):
        if self.is_element_present(self.ROLE_ACTOR_BLOCK):
            self.try_click(self.actor_movie_block_by_index(index))
        else:
            self.try_click(self.actress_movie_block_by_index(index))

    def click_on_close_btn_movie_block(self):
        self.find_element(self.CLOSE_MOVIE_BLOCK_BTN).click()

    def get_rating_of_movie(self):
        try:
            return float(self.find_element(self.RATING_OF_MOVIE).text)
        except:
            return "Not rated"

    def get_movie_data_by_index(self, index):

        image_link = self.get_movie_image_by_index(index)
        self.click_on_movie_by_index(index)

        title = self.find_element(self.MOVIE_TITLE).text
        try:
            year = self.find_element(self.RELEASE_YEAR).text
        except:
            year = "N/A"

        try:
            genres = self.find_elements(self.LIST_OF_GENRES)
            list_of_genres = [genre.text for genre in genres]
        except Exception:
            list_of_genres = "N/A"

        rating = self.get_rating_of_movie()

        movie_data = {
            "title": title,
            "year": year,
            "image_link": image_link,
            "rating": rating,
            "genres": list_of_genres
        }

        self.click_on(self.CLOSE_MOVIE_BLOCK_BTN)

        return movie_data

    def open_awards_page(self):
        self.try_click(self.AWARDS_LINK_ELEMENT)
