from sentence_transformers import SentenceTransformer, util
import json

class TaskFinder:
    def __init__(self, tasks_file):
        # Load the SBERT model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load the tasks from the JSON file
        with open(tasks_file, "r") as f:
            self.tasks = json.load(f)

        # Precompute embeddings for all tasks (combine `question` and `tags`)
        self.task_embeddings = [
            self.model.encode(task["question"] + " " + " ".join(task["tags"]))
            for task in self.tasks
        ]

    def find_best_match(self, query):
        """
        Find the best matching task for a given query using SBERT.
        """
        try:
            # Encode the user query
            query_embedding = self.model.encode(query)

            # Compute similarity scores
            similarities = [
                util.pytorch_cos_sim(query_embedding, task_emb)[0][0]
                for task_emb in self.task_embeddings
            ]

            # Find the task with the highest similarity
            best_match_idx = similarities.index(max(similarities))
            best_task = self.tasks[best_match_idx]

            # Return the best matching task
            return best_task
        except Exception as e:
            print(f"Error finding best match: {e}")
            return None
