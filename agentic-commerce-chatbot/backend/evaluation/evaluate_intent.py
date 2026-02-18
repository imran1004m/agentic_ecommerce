import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score, classification_report
from backend.agents.intent_agent import detect_intent

def predict_intent(query):
    state = {"user_input": query}
    state = detect_intent(state)
    return state.get("intent")

def evaluate():

    df = pd.read_csv("backend/evaluation/intent_test_data.csv")

    y_true = []
    y_pred = []

    for _, row in df.iterrows():
        y_true.append(row["true_intent"])
        y_pred.append(predict_intent(row["query"]))

    accuracy = accuracy_score(y_true, y_pred)

    print("Accuracy:", accuracy)
    print(classification_report(y_true, y_pred))

    # 🔥 MLflow Logging
    mlflow.set_experiment("Intent Evaluation")

    with mlflow.start_run():
        mlflow.log_metric("accuracy", accuracy)

if __name__ == "__main__":
    evaluate()
