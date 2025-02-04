import re
from datetime import datetime
import requests
import os
from PIL import Image, ImageTk


def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, "%B %d, %Y")
    today = datetime.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def parse_award_info(input_string):
    """
    Parses a string and returns the award information as a tuple.

    :param input_string: String of format '2000 Winner SFFCC Award'.
    :return: Tuple (year, award_status, award_name)
    """
    pattern = r"(\d{4})\s+(Winner|Nominee)\s+(.+)"
    match = re.match(pattern, input_string)

    if match:
        year, award_status, award_name = match.groups()
        return int(year), award_status, award_name
    else:
        raise ValueError("The string does not conform to the expected format: '2000 Winner SFFCC Award'")


def download_img(image_element, act_name):
    image_url = image_element.get_attribute('src')

    print(f"Image URL: {image_url}")

    image_data = requests.get(image_url).content

    save_dir = os.path.join(os.getcwd(), 'images')
    os.makedirs(save_dir, exist_ok=True)

    image_name = f'{act_name.lower().replace(" ", "_")}.jpg'
    image_path = os.path.join(save_dir, image_name)

    with open(image_path, 'wb') as f:
        f.write(image_data)

    print(f"Image downloaded and saved to {image_path}")
    return image_path


def safe_convert_rating(rating):
    """Attempts to convert the rating to a number, returning 0 if unsuccessful."""
    try:
        return float(rating)
    except ValueError:
        return 0


def get_unique_sorted_genres(actor):
    unique_genres = set()
    for movie in actor["movies"]:
        genres = movie.get("genres", [])

        if isinstance(genres, str):
            if genres.strip().upper() != "N/A":
                unique_genres.add(genres.strip())
        elif isinstance(genres, list):
            for genre in genres:
                if genre.strip().upper() != "N/A":
                    unique_genres.add(genre.strip())
    return sorted(unique_genres)


def group_movies_by_year(movies):
    movies_by_year = {}
    for movie in movies:
        if movie["rating"] not in ["N/A", "Not rated"]:

            year = movie["year"].replace("вЂ“", "–")
            years = year.split("–")

            if len(years) > 1:
                year = years[1].strip()
            else:
                year = years[0].strip()
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(float(movie["rating"]))

    return movies_by_year


def fetch_movie_images(movies, progress_callback):
    """Loads movie images and calls callback to update progress."""
    for idx, movie in enumerate(movies):
        if movie.get("image_link"):
            try:
                img_data = Image.open(requests.get(movie["image_link"], stream=True).raw)
                img_data = img_data.resize((90, 133), Image.Resampling.LANCZOS)
                movie["image"] = ImageTk.PhotoImage(img_data)
            except Exception as e:
                print(f"Error loading image for {movie['title']}: {e}")
        else:
            movie["image"] = None
        progress_callback(idx + 1)
    return movies
