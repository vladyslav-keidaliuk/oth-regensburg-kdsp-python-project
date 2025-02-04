# Project Overview

This project is a software that allows users to view and extract detailed information about
the Top 50 popular Hollywood actors and actresses from the IMDb list.

    http://www.imdb.com/list/ls053501318/

The application provides a user-friendly interface (via Tkinter) and well-structured outputs for various data
such as biographies,movie details,list of movies, awards, genres, and average movie ratings.

# Features:
* List all available actors and actresses
* View detailed information about a selected actor/actress:
    * Biography
    * How old is the actor/actress now (using datetime module)
    * Movies (name, thumbnail image*, year, rating and genres)
    * Awards across different years
    * Average movie rating (overall and yearly)
    * Top 5 movies (with respective years and genres)

_A thumbnail images of the movies posters are not saved to the device,
instead they are downloaded when the user wants to view a list of_ movies by a specific actor/actress.

# Installation Instructions

1. Download the ZIP file of the project and extract it.
2. Set up Python Environment
    - Ensure you have Python 3.11 or above installed on your machine.
3. Install Required Modules
    - Open a terminal/command prompt in the project directory and run:

        pip install -r requirements.txt
4. Download WebDriver
    - Install the appropriate version of the Chrome WebDriver for your browser (Chrome) from
   `https://developer.chrome.com/docs/chromedriver/downloads/version-selection?hl=en`
   
Place the WebDriver executable in your system's PATH or in the project directory.

# Usage Instructions

For run the application with GUI:
* In the terminal/command prompt, navigate to the project directory and run:
*         python main.py
* For run scraping script:
  * In the terminal/command prompt, navigate to the project directory and run:
*         python scrape_all_data.py

# #Notes

- Ensure an active internet connection while running the program (the part that's responsible for scraping data)
    as it scrapes data from the IMDb website.
- If you encounter any errors, ensure that the WebDriver and browser versions match.