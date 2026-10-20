import requests

def search_movie_imdb(movie_name: str) -> dict | None:
    """
    Search for a movie title using IMDb's suggestion API.
    Returns metadata including title, release year, and IMDb ID.
    """
    sanitized_query = movie_name.strip().lower().replace(" ", "_")
    suggestion_url = f"https://v3.sg.media-imdb.com/suggestion/x/{sanitized_query}.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    
    response = requests.get(suggestion_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    items = data.get("d", [])
    if not items:
        return None
    
    for item in items:
        if item.get("qid") in ("movie", "feature", "tvMovie"):
            return item
    return items[0]

def get_imdb_rating(imdb_id: str) -> float | None:
    """
    Fetch the live IMDb rating for a given IMDb title ID.
    """
    rating_url = "https://api.agregarr.org/api/ratings"
    response = requests.get(rating_url, params={"id": imdb_id}, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("rating")
    return None

def main():
    """
    Main loop to query movie ratings from IMDb.
    """
    print("=== IMDb Movie Rating Lookup ===")
    print("Type a movie name to search, or 'exit' / 'q' to quit.\n")

    while True:
        try:
            movie_name = input("Enter movie title: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            break

        if not movie_name or movie_name.lower() in ("exit", "quit", "q"):
            print("Exiting program.")
            break

        try:
            movie_info = search_movie_imdb(movie_name)
            if not movie_info:
                print(f"Movie '{movie_name}' not found.\n")
                continue

            title = movie_info.get("l", movie_name)
            year = movie_info.get("y", "N/A")
            imdb_id = movie_info.get("id")

            rating = get_imdb_rating(imdb_id)
            rating_display = f"{rating}/10" if rating is not None else "N/A"

            print(f"-> Title:  {title} ({year})")
            print(f"   Rating: {rating_display}")
            print(f"   IMDb:   https://www.imdb.com/title/{imdb_id}/\n")

        except Exception as error:
            print(f"Error fetching movie data: {error}\n")

if __name__ == "__main__":
    main()