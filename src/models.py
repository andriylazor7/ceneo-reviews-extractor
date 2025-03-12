import json
import csv
import os

class Opinion:
    def __init__(self, opinion_id, author, score, content, helpful=0, unhelpful=0,
                 recommendation=None, advantages=None, disadvantages=None, publish_date=None, purchase_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.score = self.parse_score(score)
        self.content = content
        self.recommendation = recommendation
        self.advantages = advantages or []
        self.disadvantages = disadvantages or []
        self.helpful = int(helpful)
        self.unhelpful = int(unhelpful)
        self.publish_date = publish_date
        self.purchase_date = purchase_date

    @staticmethod
    def parse_score(score):
        try:
            return float(score.replace(",", "."))
        except (ValueError, AttributeError):
            return None

    def to_dict(self):
        return {
            "opinion_id": self.opinion_id,
            "author": self.author,
            "score": self.score,
            "content": self.content,
            "recommendation": self.recommendation,
            "advantages": self.advantages,
            "disadvantages": self.disadvantages,
            "helpful": self.helpful,
            "unhelpful": self.unhelpful,
            "publish_date": self.publish_date,
            "purchase_date": self.purchase_date
        }

    def __repr__(self):
        return f"Opinion({self.opinion_id}, {self.author}, {self.score}, {self.recommendation})"
      
      
      

class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self.opinions = []

    def add_opinion(self, opinion):
        if isinstance(opinion, Opinion):
            self.opinions.append(opinion)

    def get_statistics(self):
        if not self.opinions:
            return {}

        scores = [opinion.score for opinion in self.opinions if opinion.score is not None]
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0

        num_pros = sum(1 for o in self.opinions if o.advantages)
        num_cons = sum(1 for o in self.opinions if o.disadvantages)

        return {
            "total_reviews": len(self.opinions),
            "average_score": avg_score,
            "reviews_with_pros": num_pros,
            "reviews_with_cons": num_cons,
        }

    def save_to_json(self):
        os.makedirs("data", exist_ok=True)
        filename = f"data/{self.product_id}.json"

        data = [opinion.to_dict() for opinion in self.opinions]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"✅ Data saved to {filename}")

    def save_to_csv(self):
        """Saves the product reviews to a CSV file."""
        if not self.opinions:
            print("⚠️ No opinions to save.")
            return

        os.makedirs("data", exist_ok=True)
        filename = f"data/{self.product_id}.csv"

        keys = self.opinions[0].to_dict().keys()
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows([op.to_dict() for op in self.opinions])

        print(f"✅ Data saved to {filename}")

