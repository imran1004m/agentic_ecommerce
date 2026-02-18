import mlflow
import math
from backend.services.product_service import hybrid_search
from backend.db.session import SessionLocal
from backend.evaluation.retrieval_dataset import retrieval_test_data


def compute_mrr(rank_list):
    reciprocal_ranks = []
    for rank in rank_list:
        if rank > 0:
            reciprocal_ranks.append(1 / rank)
    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def evaluate():

    db = SessionLocal()

    top1_correct = 0
    top3_correct = 0
    ranks = []

    for sample in retrieval_test_data:

        query = sample["query"]
        expected_brand = sample.get("expected_brand")
        expected_category = sample.get("expected_category")

        results = hybrid_search(db, query=query, available_only=True, top_k=5)

        found_rank = 0

        for idx, row in enumerate(results, start=1):
            brand = row[3]
            category = row[2]

            if expected_brand and brand.lower() == expected_brand.lower():
                found_rank = idx
                break

            if expected_category and category.lower() == expected_category.lower():
                found_rank = idx
                break

        if found_rank == 1:
            top1_correct += 1

        if found_rank > 0 and found_rank <= 3:
            top3_correct += 1

        ranks.append(found_rank if found_rank > 0 else 0)

    total = len(retrieval_test_data)

    top1_acc = top1_correct / total
    top3_acc = top3_correct / total
    mrr = compute_mrr(ranks)

    print("Top-1 Accuracy:", top1_acc)
    print("Top-3 Accuracy:", top3_acc)
    print("MRR:", mrr)

    # 🔥 Log to MLflow
    mlflow.set_experiment("RAG Retrieval Evaluation")

    with mlflow.start_run():
        mlflow.log_metric("top1_accuracy", top1_acc)
        mlflow.log_metric("top3_accuracy", top3_acc)
        mlflow.log_metric("mrr", mrr)

    db.close()


if __name__ == "__main__":
    evaluate()
