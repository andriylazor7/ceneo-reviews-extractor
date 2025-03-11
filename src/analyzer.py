import json
import statistics

def load_data_from_json(filename):
    """Loads extracted opinions from a JSON file."""
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def analyze_reviews(reviews):
    """Performs statistical analysis on reviews."""
    num_reviews = len(reviews)
    
    scores = [float(review["score"].replace(",", ".")) for review in reviews if review["score"].replace(",", ".").replace("/", "").isdigit()]
    avg_score = round(statistics.mean(scores), 2) if scores else 0

    num_pros = sum(1 for review in reviews if review.get("advantages") not in ["None", "", " "])
    num_cons = sum(1 for review in reviews if review.get("disadvantages") not in ["None", "", " "])


    return {
        "total_reviews": num_reviews,
        "average_score": avg_score,
        "reviews_with_pros": num_pros,
        "reviews_with_cons": num_cons,
    }
