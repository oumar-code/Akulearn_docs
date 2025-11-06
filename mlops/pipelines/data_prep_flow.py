"""
Minimal Prefect flow example for data ingestion and tokenization.
This is a lightweight example to show structure; replace the `read_data` step with
connectors to your object store / databases.
"""
from prefect import flow, task


@task
def read_data(path: str):
    # Placeholder: read lines from a local file for demo purposes
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


@task
def tokenize(lines):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    tokens = [tokenizer.encode_plus(l, truncation=True, max_length=256) for l in lines]
    return tokens


@flow
def data_prep_flow(sample_path: str = "mlops/examples/sample_corpus.txt"):
    lines = read_data(sample_path)
    tokens = tokenize(lines)
    # Here you would write tokens to object storage and register dataset artifacts
    return len(tokens)


if __name__ == "__main__":
    # quick local run
    print("Running data_prep_flow (demo):", data_prep_flow())
