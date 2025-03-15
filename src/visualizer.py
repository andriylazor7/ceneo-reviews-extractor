import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter
import io
import base64

class Visualizer:
    def __init__(self, reviews):
        self.reviews = reviews

    def plot_recommendation_pie_base64(self):
        recommendations = [review.get("recommendation", "No data") for review in self.reviews]
        count = Counter(recommendations)

        labels = list(count.keys())
        sizes = list(count.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["green", "red", "gray"])

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{image_base64}"

    def plot_ratings_bar_base64(self):
        scores = []
        for review in self.reviews:
            score = review.get("score")
            try:
                scores.append(float(score))
            except (ValueError, TypeError):
                pass

        if not scores:
            print("⚠️ No valid scores available for visualization.")
            return None

        count = Counter(scores)
        labels = [str(key) for key in count.keys()]
        values = list(count.values())

        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color="blue")
        plt.xlabel("Rating (Stars)")
        plt.ylabel("Number of Reviews")
        plt.title("Review Ratings Distribution")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{image_base64}"

