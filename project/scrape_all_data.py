import json
import os

from pages.actors_list_page import ActorsListPage
from pages.awards_page import AwardsPage
from pages.actor_page import ActorPage, actor_img
from pages.biography_page import BiographyPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helper import download_img


def scrape_data(max_retries=3):
    global driver
    retries = 0

    while retries < max_retries:
        try:
            home_page_url = 'https://www.imdb.com/list/ls053501318/'

            chrome_options = Options()
            chrome_options.add_argument("--lang=en")

            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()
            driver.get(home_page_url)

            actors_page = ActorsListPage(driver)
            actors = actors_page.get_actors()
            actors_page.click_accept_cookies()

            if os.path.exists("actors_data.json"):
                with open("actors_data.json", "r", encoding="utf-8") as file:
                    actors_data = json.load(file)
            else:
                actors_data = []

            processed_actors = {actor['name'] for actor in actors_data}

            for actor in actors:
                print(actor["name"])
                if actor["name"] in processed_actors:
                    print(f"Skipping {actor['name']} (already processed)")
                    continue

                print(f"\nSTART scraping for {actor['name']}")
                actors_page.click_by_title(actor["name"])
                act_page = ActorPage(driver)

                element = act_page.find_element(actor_img(actor["name"]))
                download_img(element, actor["name"])

                date_of_birth = act_page.get_date_of_birth()
                act_page.open_bio_page()

                bio_page = BiographyPage(driver)
                bio = bio_page.get_biography()
                print("Biography get successfully")
                driver.back()

                act_page.open_awards_page()

                awards_page = AwardsPage(driver)
                awards = awards_page.get_awards()
                print("Awards get successfully")

                driver.back()

                actor_info = {
                    "name": actor["name"],
                    "photo_path": f"{actor['name'].lower().replace(' ', '_')}.jpg",
                    "date_of_birth": date_of_birth,
                    "biography": bio,
                    "awards": awards,
                    "movies": [],
                }

                act_page.expand_list_of_movies()

                number_of_movies = act_page.get_count_of_movies()
                for i in range(1, number_of_movies + 1):
                    movie_data = act_page.get_movie_data_by_index(i)

                    actor_info["movies"].append(movie_data)
                print("Movies get successfully")
                actors_data.append(actor_info)

                with open("actors_data.json", "w", encoding="utf-8") as file:
                    json.dump(actors_data, file, ensure_ascii=False, indent=4)

                print(f"END scraping for {actor['name']}\n")
                driver.back()

            driver.quit()
            break
        except Exception as e:
            retries += 1
            print(f"\nAn error occurred during data extraction (Attempt {retries} of {max_retries}): {e}")
            driver.quit()

            if retries >= max_retries:
                print("Max retries reached. Exiting...")
                break


scrape_data(max_retries=3)
