import csv
import sys
from util import Node, StackFrontier, QueueFrontier

# Data structures to store people and movie information
names = {}  # Maps names to person_ids
people = {}  # Maps person_ids to personal details
movies = {}  # Maps movie_ids to movie details

def load_data(directory):
    """
Loads data from CSV files into memory.
Processes people.csv, movies.csv, and stars.csv.
    """
    # Load people data
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies data
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load star relationships
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get source and target actors
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find shortest path
    path = shortest_path(source, target)

    # Display results
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path(source, target):
    """
Finds shortest path between two actors using BFS.
Returns list of (movie_id, person_id) pairs connecting them.
    """
    def get_path(end_node):
        """Backtracks from end node to reconstruct path."""
        current_node = end_node
        path = []
        while current_node.parent:
            path.append((current_node.action, current_node.state))
            current_node = current_node.parent
        path.reverse()
        return path

    # Initialize BFS frontier with source node
    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))
    visited = set()

    while not frontier.empty():
        current_node = frontier.remove()

        # Skip already visited nodes
        if current_node.state in visited:
            continue
        visited.add(current_node.state)

        # Check if target found
        if current_node.state == target:
            return get_path(current_node)

        # Explore neighbors (costars)
        for movie_id, person_id in neighbors_for_person(current_node.state):
            frontier.add(Node(person_id, current_node, movie_id))

    return None  # No path found

def person_id_for_name(name):
    """
Resolves name to person_id, handling ambiguous names.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            print(f"ID: {person_id}, Name: {person['name']}, Birth: {person['birth']}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """
Returns set of (movie_id, person_id) pairs for costars.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for costar_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, costar_id))
    return neighbors

if __name__ == "__main__":
    main()