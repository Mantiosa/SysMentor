from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import json

class TaskFinder:
    def __init__(self, tasks_file="tasks.json", model_dir="./fine_tuned_model"):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_dir)
        self.tasks = self.load_tasks(tasks_file)

    def load_tasks(self, tasks_file):
        with open(tasks_file, "r") as file:
            return json.load(file)

    def find_best_match(self, query):
        # Tokenize the input query
        inputs = self.tokenizer(query, return_tensors="pt", truncation=True)

        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()

        # Return the matched task
        return self.tasks[predicted_class]
