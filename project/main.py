import json
import threading
import tkinter as tk
import os
from PIL import Image, ImageTk
from helper import calculate_age, safe_convert_rating, get_unique_sorted_genres, group_movies_by_year, \
    fetch_movie_images
from tkinter import ttk


def update_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def show_actor_movies(actor_name, actor_data):
    """Opens a window with a list of the actor's movies with a progress bar."""
    actor = next((item for item in actor_data if item["name"] == actor_name), None)
    if not actor or not actor.get("movies"):
        return

    movies = actor["movies"]

    progress_window = tk.Toplevel()
    progress_window.title("Loading Movies...")

    tk.Label(progress_window, text=f"Loading movies for {actor_name}...").pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = len(movies)

    def update_progress(value):
        progress_bar["value"] = value
        if value == len(movies):
            progress_window.destroy()
            display_movies(actor_name, movies)

    def load_movies():
        fetch_movie_images(movies, progress_callback=update_progress)

    threading.Thread(target=load_movies, daemon=True).start()


def display_movies(actor_name, movies):
    """Displays a window with a list of movies after downloading."""
    movies_window = tk.Toplevel()
    movies_window.title(f"{actor_name} - Movies")

    main_frame = tk.Frame(movies_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    movie_list_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=movie_list_frame, anchor="nw")

    def update_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    movie_list_frame.bind("<Configure>", update_canvas)

    for movie in movies:
        movie_frame = tk.Frame(movie_list_frame, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        movie_frame.pack(fill=tk.X, pady=5, padx=10)

        if movie.get("image"):
            tk.Label(movie_frame, image=movie["image"]).pack(side=tk.LEFT, padx=10)
            movie_frame.image = movie["image"]

        info_frame = tk.Frame(movie_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(info_frame, text=movie["title"], font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(info_frame, text=f"Year: {movie['year']}", font=("Arial", 12)).pack(anchor="w")
        tk.Label(info_frame, text=f"Rating: {movie['rating']} / 10", font=("Arial", 12)).pack(anchor="w")
        tk.Label(info_frame, text=f"Genres: {', '.join(movie['genres'])}", font=("Arial", 12)).pack(anchor="w")


def show_actor_info(actor_name, actor_data):
    """Opens a window with information about the selected actor."""
    actor = next((item for item in actor_data if item["name"] == actor_name), None)

    if actor is None:
        return

    new_window = tk.Toplevel()
    new_window.title(actor['name'])

    tk.Label(new_window, text=f"Full name: {actor['name']}", font=("Arial", 16, 'bold')).pack(pady=10)

    tk.Label(new_window,
             text=f"Date of Birth: {actor['date_of_birth']} || Age: {calculate_age(actor['date_of_birth'])} years",
             font=("Arial", 12)).pack(pady=10)

    bio_text = tk.Text(new_window, wrap=tk.WORD, font=("Arial", 12), width=60, height=20)
    bio_text.insert(tk.END, actor['biography'])
    bio_text.config(state=tk.DISABLED)
    bio_text.pack(pady=10, padx=10)

    buttons_frame = tk.Frame(new_window)
    buttons_frame.pack(pady=10)

    tk.Button(buttons_frame, text="Movies", command=lambda: show_actor_movies(actor_name, actor_data)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Awards", command=lambda: show_actor_awards(actor_name, actor_data)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Movie Genres", command=lambda: show_actor_movie_genres(actor_name, actor_data)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Average Rating",
              command=lambda: show_actor_average_rating(actor_name, actor_data)).pack(side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Top 5 Movies", command=lambda: show_actor_top_movies(actor_name, actor_data)).pack(
        side=tk.LEFT, padx=5)

    tk.Button(new_window, text="Close", command=new_window.destroy).pack(pady=10)


def create_actor_button(actor_name, actor, parent_frame):
    image_path = f"images/{actor.get('photo_path', None)}"
    if image_path and os.path.exists(image_path):
        img_data = Image.open(image_path)
        img_data = img_data.resize((100, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img_data)

        button = tk.Button(
            parent_frame, text=actor_name, image=img, compound="top", font=("Arial", 12),
            command=lambda: show_actor_info(actor_name, actor_data)
        )
        button.image = img
        return button
    return None


def show_actors():
    columns = 5
    row = 0
    col = 0

    for actor in actor_data:
        button = create_actor_button(actor['name'], actor, actor_list_frame)
        if button:
            button.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col >= columns:
                col = 0
                row += 1


def show_actor_awards(actor_name, actor_data):
    actor = next((item for item in actor_data if item["name"] == actor_name), None)
    if not actor or not actor.get("awards"):
        return

    awards = actor["awards"]

    awards_window = tk.Toplevel()
    awards_window.title(f"{actor_name} - Awards")

    awards_window.geometry("900x600")
    awards_window.resizable(False, True)

    sort_order = tk.StringVar(value="ASC")
    group_by = tk.StringVar(value="None")

    def update_awards_list():
        sorted_awards = sorted(
            awards,
            key=lambda x: x["year"],
            reverse=(sort_order.get() == "DESC")
        )
        if group_by.get() == "Award Name":
            grouped_awards = {}
            for award in sorted_awards:
                grouped_awards.setdefault(award["award_name"], []).append(award)
        else:
            grouped_awards = {"All Awards": sorted_awards}

        for widget in awards_list_frame.winfo_children():
            widget.destroy()

        for group, group_awards in grouped_awards.items():
            if group_by.get() == "Award Name":
                tk.Label(awards_list_frame, text=group, font=("Arial", 14, "bold")).pack(anchor="w", pady=5)

            for award in group_awards:
                award_frame = tk.Frame(awards_list_frame, padx=10, pady=5, relief=tk.RIDGE, borderwidth=2)
                award_frame.pack(fill=tk.X, pady=2, padx=10)

                tk.Label(award_frame, text=f"Award: {award['award_name']}", font=("Arial", 12, "bold")).pack(anchor="w")
                tk.Label(award_frame, text=f"Status: {award['award_status']}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(award_frame, text=f"Year: {award['year']}", font=("Arial", 12)).pack(anchor="w")
                tk.Label(award_frame, text=f"Category: {award['category']}", font=("Arial", 12)).pack(anchor="w")

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    controls_frame = tk.Frame(awards_window)
    controls_frame.pack(fill=tk.X, pady=5)

    tk.Label(controls_frame, text="Sort by Year:", font=("Arial", 14, "bold")).pack(side=tk.LEFT,
                                                                                    padx=5)
    tk.Radiobutton(controls_frame, text="ASC", variable=sort_order, value="ASC", command=update_awards_list,
                   font=("Arial", 12)).pack(side=tk.LEFT)
    tk.Radiobutton(controls_frame, text="DESC", variable=sort_order, value="DESC", command=update_awards_list,
                   font=("Arial", 12)).pack(side=tk.LEFT)

    tk.Label(controls_frame, text="Group by:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(controls_frame, text="None", variable=group_by, value="None", command=update_awards_list,
                   font=("Arial", 12)).pack(side=tk.LEFT)
    tk.Radiobutton(controls_frame, text="Award Name", variable=group_by, value="Award Name", command=update_awards_list,
                   font=("Arial", 12)).pack(side=tk.LEFT)

    main_frame = tk.Frame(awards_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    awards_list_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=awards_list_frame, anchor="nw")

    def update_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    awards_list_frame.bind("<Configure>", update_canvas)

    update_awards_list()

    tk.Button(awards_window, text="Close", command=awards_window.destroy).pack(pady=10)


def show_actor_movie_genres(actor_name, actor_data):
    actor = next((item for item in actor_data if item["name"] == actor_name), None)
    if not actor or not actor.get("movies"):
        return

    sorted_genres = get_unique_sorted_genres(actor)

    genres_window = tk.Toplevel()
    genres_window.title(f"Movie Genres of {actor_name}")

    tk.Label(genres_window, text=f"Movie Genres of {actor_name}", font=("Arial", 16, "bold")).pack(pady=10)

    genres_listbox = tk.Listbox(genres_window, font=("Arial", 12), width=40, height=20)
    for genre in sorted_genres:
        genres_listbox.insert(tk.END, genre)
    genres_listbox.pack(pady=10, padx=10)

    tk.Button(genres_window, text="Close", command=genres_window.destroy).pack(pady=10)


def show_actor_average_rating(actor_name, actor_data):
    actor = next((item for item in actor_data if item["name"] == actor_name), None)
    if not actor or not actor.get("movies"):
        return

    movies = actor["movies"]

    ratings = [float(movie["rating"]) for movie in movies if movie["rating"] not in ["N/A", "Not rated"]]
    overall_average = sum(ratings) / len(ratings) if ratings else 0

    rating_window = tk.Toplevel()
    rating_window.title(f"{actor_name} - Average Ratings")

    main_frame = tk.Frame(rating_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    ratings_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=ratings_frame, anchor="nw")

    def update_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    ratings_frame.bind("<Configure>", update_canvas)

    tk.Label(ratings_frame, text=f"Overall Average Rating: {overall_average:.2f} / 10",
             font=("Arial", 14, "bold")).pack(pady=10)

    for year, year_ratings in group_movies_by_year(movies).items():
        year_average = sum(year_ratings) / len(year_ratings)
        tk.Label(ratings_frame, text=f"Year {year} - Average Rating: {year_average:.2f} / 10", font=("Arial", 12)).pack(
            anchor="w", pady=5)

    tk.Button(rating_window, text="Close", command=rating_window.destroy).pack(pady=10)


def show_actor_top_movies(actor_name, actor_data):
    """Opens a window with the actor's top 5 movies, their years and genres."""
    actor = next((item for item in actor_data if item["name"] == actor_name), None)
    if not actor or not actor.get("movies"):
        return

    sorted_movies = sorted(actor["movies"], key=lambda x: safe_convert_rating(x["rating"]), reverse=True)
    top_5_movies = sorted_movies[:5]

    top_movies_window = tk.Toplevel()
    top_movies_window.title(f"Top 5 Movies of {actor_name}")

    tk.Label(top_movies_window, text=f"Top 5 Movies of {actor_name}", font=("Arial", 16, "bold")).pack(pady=10)

    for movie in top_5_movies:
        movie_frame = tk.Frame(top_movies_window, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        movie_frame.pack(fill=tk.X, pady=5, padx=10)

        tk.Label(movie_frame, text=movie["title"], font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(movie_frame, text=f"Year: {movie['year']}", font=("Arial", 12)).pack(anchor="w")
        tk.Label(movie_frame, text=f"Rating: {movie['rating']} / 10", font=("Arial", 12)).pack(anchor="w")
        tk.Label(movie_frame, text=f"Genres: {', '.join(movie['genres'])}", font=("Arial", 12)).pack(anchor="w")

    tk.Button(top_movies_window, text="Close", command=top_movies_window.destroy).pack(pady=10)


if __name__ == "__main__":
    with open('actors_data.json', 'r') as f:
        actor_data = json.load(f)

    root = tk.Tk()
    root.title("Vladyslav Keidaliuk - Project 2. Hollywood Actors and Actresses")

    root.geometry("900x600")
    root.resizable(False, False)

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    actor_list_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=actor_list_frame, anchor="nw")

    actor_list_frame.bind("<Configure>", update_canvas)

    show_actors()

    root.mainloop()
