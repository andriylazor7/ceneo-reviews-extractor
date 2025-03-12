import matplotlib.pyplot as plt
import json
from collections import Counter

def load_data_from_json(filename):
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def plot_recommendation_pie(reviews):
    reviews_dicts = [review.to_dict() for review in reviews]

    recommendations = [review.get("recommendation", "No data") for review in reviews_dicts]
    count = Counter(recommendations)

    labels = count.keys()
    sizes = count.values()
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["green", "red", "gray"])
    plt.title("Recommendation Distribution")
    plt.show()

def plot_ratings_bar(reviews):
    reviews_dicts = [review.to_dict() for review in reviews]

    scores = [float(review["score"]) for review in reviews_dicts if isinstance(review["score"], (int, float))]

    if not scores:
        print("⚠️ No valid scores available for visualization.")
        return

    count = Counter(scores)

    labels = [str(key) for key in count.keys()] 
    values = list(count.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color="blue")
    plt.xlabel("Rating (Stars)")
    plt.ylabel("Number of Reviews")
    plt.title("Review Ratings Distribution")
    plt.show()
