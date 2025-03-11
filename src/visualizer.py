import matplotlib.pyplot as plt
import json
from collections import Counter

def load_data_from_json(filename):
    """Loads extracted opinions from a JSON file."""
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def plot_recommendation_pie(reviews):
    """Generates a pie chart for recommendation distribution."""
    recommendations = [review.get("recommendation", "No data") for review in reviews]
    count = Counter(recommendations)

    labels = count.keys()
    sizes = count.values()
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["green", "red", "gray"])
    plt.title("Recommendation Distribution")
    plt.show()

def plot_ratings_bar(reviews):
    """Generates a bar chart for review ratings."""
    ratings = [review["score"] for review in reviews if review["score"]]
    count = Counter(ratings)

    labels = list(count.keys())
    values = list(count.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color="blue")
    plt.xlabel("Rating (Stars)")
    plt.ylabel("Number of Reviews")
    plt.title("Review Ratings Distribution")
    plt.show()
