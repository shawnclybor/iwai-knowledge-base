"""
Lesson 3 Evaluation Harness
Runs test queries against the knowledge base, generates answers,
scores with Ragas metrics, and pushes traces to Langfuse.

Usage:
    cd assets/03-advanced/evaluation
    python evaluate.py
"""

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Load env vars from lesson 3 .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Validate required env vars
REQUIRED_VARS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "OPENAI_API_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_HOST",
]

missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
if missing:
    print(f"Error: Missing environment variables: {', '.join(missing)}")
    print(f"Check your .env file at: {env_path}")
    sys.exit(1)

from langfuse import Langfuse
from openai import OpenAI
from supabase import create_client

# Initialize clients
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ["LANGFUSE_HOST"],
)

EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = (
    "Answer the question based only on the provided context. "
    "If the context doesn't contain enough information to answer, say so. "
    "Be concise and specific."
)


def load_dataset() -> list[dict]:
    """Load test queries from the dataset file."""
    dataset_path = Path(__file__).parent / "datasets" / "truepoint-queries.json"
    with open(dataset_path) as f:
        return json.load(f)


def embed_query(text: str) -> list[float]:
    """Embed a query using OpenAI text-embedding-3-small."""
    response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def search_kb(query_text: str, query_embedding: list[float], match_count: int = 10) -> list[dict]:
    """Call hybrid_search RPC on Supabase."""
    result = supabase.rpc(
        "hybrid_search",
        {
            "query_text": query_text,
            "query_embedding": query_embedding,
            "match_count": match_count,
            "vector_weight": 0.7,
            "text_weight": 0.3,
        },
    ).execute()

    return result.data or []


def generate_answer(question: str, contexts: list[str]) -> str:
    """Generate an answer using GPT-4o-mini with retrieved context."""
    context_text = "\n\n---\n\n".join(contexts)

    response = openai_client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {question}",
            },
        ],
        temperature=0,
        max_tokens=500,
    )

    return response.choices[0].message.content or ""


def score_with_ragas(question: str, contexts: list[str], answer: str, ground_truth: str | None) -> dict:
    """Score a single query result with Ragas metrics."""
    try:
        from ragas import evaluate as ragas_evaluate
        from ragas.metrics import answer_relevancy, context_precision, faithfulness
        from datasets import Dataset

        eval_data = {
            "question": [question],
            "contexts": [contexts],
            "answer": [answer],
        }

        metrics = [faithfulness, answer_relevancy, context_precision]

        if ground_truth:
            eval_data["ground_truth"] = [ground_truth]

        dataset = Dataset.from_dict(eval_data)
        result = ragas_evaluate(dataset, metrics=metrics)

        return {
            "faithfulness": result["faithfulness"],
            "answer_relevancy": result["answer_relevancy"],
            "context_precision": result["context_precision"],
        }
    except Exception as e:
        print(f"  Warning: Ragas scoring failed: {e}")
        return {"faithfulness": None, "answer_relevancy": None, "context_precision": None}


def evaluate_query(item: dict, index: int, total: int) -> dict:
    """Run the full evaluation pipeline for a single query."""
    question = item["question"]
    expected_sources = item.get("expected_sources", [])
    ground_truth = item.get("ground_truth")

    print(f"  [{index + 1}/{total}] {question[:60]}...")

    # Create a Langfuse trace for this query
    trace = langfuse.trace(
        name=f"eval-query-{index + 1}",
        input={"question": question, "expected_sources": expected_sources},
    )

    # Step 1: Embed
    embed_span = trace.span(name="embedding", input={"model": EMBEDDING_MODEL})
    start = time.time()
    query_embedding = embed_query(question)
    embed_span.end(output={"dimensions": len(query_embedding), "latency_ms": int((time.time() - start) * 1000)})

    # Step 2: Retrieve
    retrieval_span = trace.span(name="retrieval", input={"match_count": 10})
    start = time.time()
    search_results = search_kb(question, query_embedding)
    contexts = [r["content"] for r in search_results]
    source_files = [r.get("file_name", "unknown") for r in search_results]
    retrieval_span.end(
        output={
            "result_count": len(search_results),
            "source_files": source_files[:5],
            "latency_ms": int((time.time() - start) * 1000),
        }
    )

    # Step 3: Generate answer
    generation_span = trace.span(name="generation", input={"model": GENERATION_MODEL, "context_count": len(contexts)})
    start = time.time()
    answer = generate_answer(question, contexts[:5])
    generation_span.end(output={"answer": answer[:200], "latency_ms": int((time.time() - start) * 1000)})

    # Step 4: Score with Ragas
    scoring_span = trace.span(name="scoring")
    scores = score_with_ragas(question, contexts[:5], answer, ground_truth)
    scoring_span.end(output=scores)

    # Attach scores to the trace
    for metric_name, score_value in scores.items():
        if score_value is not None:
            trace.score(name=metric_name, value=score_value)

    # Check source accuracy
    found_sources = set(source_files[:5])
    expected_set = set(expected_sources)
    source_hit = bool(found_sources & expected_set) if expected_sources else None

    trace.update(
        output={
            "answer": answer[:200],
            "source_hit": source_hit,
            "scores": scores,
        }
    )

    return {
        "question": question,
        "answer": answer[:100] + "..." if len(answer) > 100 else answer,
        "result_count": len(search_results),
        "source_hit": source_hit,
        **scores,
    }


def print_summary(results: list[dict]) -> None:
    """Print a summary table of evaluation results."""
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    # Header
    print(f"\n{'#':<4} {'Question':<45} {'Faith':>7} {'Relev':>7} {'Prec':>7} {'Src':>5}")
    print("-" * 80)

    for i, r in enumerate(results):
        q = r["question"][:42] + "..." if len(r["question"]) > 42 else r["question"]
        faith = f"{r['faithfulness']:.3f}" if r.get("faithfulness") is not None else "  —  "
        relev = f"{r['answer_relevancy']:.3f}" if r.get("answer_relevancy") is not None else "  —  "
        prec = f"{r['context_precision']:.3f}" if r.get("context_precision") is not None else "  —  "
        src = "hit" if r.get("source_hit") else "miss" if r.get("source_hit") is False else " — "
        print(f"{i + 1:<4} {q:<45} {faith:>7} {relev:>7} {prec:>7} {src:>5}")

    # Averages
    print("-" * 80)
    metrics = ["faithfulness", "answer_relevancy", "context_precision"]
    avgs = {}
    for m in metrics:
        values = [r[m] for r in results if r.get(m) is not None]
        avgs[m] = sum(values) / len(values) if values else None

    avg_faith = f"{avgs['faithfulness']:.3f}" if avgs.get("faithfulness") is not None else "  —  "
    avg_relev = f"{avgs['answer_relevancy']:.3f}" if avgs.get("answer_relevancy") is not None else "  —  "
    avg_prec = f"{avgs['context_precision']:.3f}" if avgs.get("context_precision") is not None else "  —  "

    hits = sum(1 for r in results if r.get("source_hit"))
    total_src = sum(1 for r in results if r.get("source_hit") is not None)

    print(f"{'AVG':<4} {'':45} {avg_faith:>7} {avg_relev:>7} {avg_prec:>7} {hits}/{total_src}")
    print("=" * 80)


def main():
    print("Lesson 3 — Evaluation Harness")
    print(f"Langfuse host: {os.environ['LANGFUSE_HOST']}")
    print()

    # Load dataset
    dataset = load_dataset()
    print(f"Loaded {len(dataset)} test queries from truepoint-queries.json\n")

    # Run evaluations
    results = []
    for i, item in enumerate(dataset):
        result = evaluate_query(item, i, len(dataset))
        results.append(result)

    # Flush Langfuse
    langfuse.flush()

    # Print summary
    print_summary(results)

    # Print Langfuse dashboard link
    host = os.environ["LANGFUSE_HOST"].rstrip("/")
    print(f"\nView traces in Langfuse: {host}")
    print("Navigate to Traces to see detailed spans and scores for each query.\n")


if __name__ == "__main__":
    main()
