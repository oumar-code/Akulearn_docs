# mlops

Small scaffold for Aku Platform MLOps examples. This folder contains a tiny model serving demo, a minimal Prefect dataflow, and helper scripts for quantization and packaging.

What is included (initial pass):
- `examples/fastapi_server.py` - minimal FastAPI app demonstrating a summarization endpoint using Hugging Face pipelines (for demo only).
- `pipelines/data_prep_flow.py` - a Prefect flow that would perform data ingestion / tokenization.
- `serving/quantize.py` - placeholder script with notes to convert models to ONNX/TFLite/TorchScript and quantize for Edge.
- `Dockerfile` - example container for serving the model with uvicorn.
- `requirements.txt` - pip requirements for the demo.

Run notes:
- These examples are intentionally lightweight. They illustrate structure and can be adapted to your compute environment (Super Hubs / IG-Hub / Edge).
