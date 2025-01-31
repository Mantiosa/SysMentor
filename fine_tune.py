import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Short instruction: If there is a need to retrain the model further, install these dependancies above, update the train.csv and run this file.
# train.csv format is as follows: "Query or a question", <answer_id>. example:
# "Restarting a Linux service?",0
# "What is the way to restart a service?",0

def load_data(csv_file):
    data = pd.read_csv(csv_file)
    examples = [
        InputExample(texts=[row['query']], label=row['answer_id'])
        for _, row in data.iterrows()
    ]
    return examples

def fine_tune_sbert(train_data_file, model_name="all-MiniLM-L6-v2", output_dir="./fine_tuned_model", epochs=4, batch_size=16):
    model = SentenceTransformer(model_name)
    train_examples = load_data(train_data_file)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)
    train_loss = losses.CosineSimilarityLoss(model=model)

    # Actual training
    print("Starting training...")
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=int(0.1 * len(train_dataloader) * epochs),
        output_path=output_dir
    )
    print(f"Model fine-tuned and saved to {output_dir}.")

if __name__ == "__main__":
    train_csv_path = "train.csv" 

    fine_tune_sbert(
        train_data_file=train_csv_path,
        model_name="all-MiniLM-L6-v2",
        output_dir="./fine_tuned_model",
        epochs=4,
        batch_size=16
    )
